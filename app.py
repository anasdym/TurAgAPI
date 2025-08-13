from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
import json
import requests
import os
import sqlite3

class TripIn(BaseModel):
    destination: str = Field(..., min_length=1)
    month: str = Field(..., min_length=1)
    price_pln: float = Field(..., ge=0)

class TripOut(TripIn):
    id: int

# Sprawdzenie plika travel.db i tworzenie tabela
DB_NAME = "travel.db"

if not os.path.exists(DB_NAME):
   with sqlite3.connect(DB_NAME) as conn:
      cur = conn.cursor()
      cur.execute('''
          CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            month TEXT NOT NULL,
            price_pln REAL NOT NULL CHECK (price_pln >= 0)      
            )
             ''')
      conn.commit()

# Funkcja dodająca nowy wpis
def insert(destination, month, price_pln):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trips (destination, month, price_pln)
            VALUES (?, ?, ?)
        ''', (destination, month, price_pln))
        conn.commit()
        trip_id = cursor.lastrowid
        return {
            "id": trip_id,
            "destination": destination,
            "month": month,
            "price_pln": price_pln
        }

# Funkcja zwracająca wszystkie wpisy
def select_all():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM trips')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd bazy danych: {str(e)}")

# Funkcja zwracająca wpisy filtrowane po destination
def select_by_destination(destination):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM trips
                WHERE LOWER(destination) = LOWER(?)
            ''', (destination,))
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd bazy danych: {str(e)}")

def exchange(currency_code: str) -> float:
    if currency_code.upper() == "PLN":
        return 1.0  # Kurs PLN do PLN to zawsze 1
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency_code.upper()}/?format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['rates'][0]['mid']
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Błąd połączenia z API NBP.")
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="Nieobsługiwany kod waluty.")

def convert_price(price_pln: float, rate: float) -> float:
    return round(price_pln / rate, 2)

app = FastAPI()

# Dodanie endpointu /health zwracającego prosty status.
@app.get("/health")
def status():
    return {"status": "ok"}

@app.post("/trips", response_model=TripOut, status_code=201)
#@app.post("/trips")
def create_trip(trip: TripIn):
    try:
        result = insert(trip.destination, trip.month, trip.price_pln)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/trips")
def list_trips(currency: Optional[str] = "PLN"):
    trips = select_all()
    rate = exchange(currency)

    for trip in trips:
        trip["price"] = str(convert_price(float(trip["price_pln"]), rate))
        trip["currency"] = currency.upper()
        del trip["price_pln"]

    return {"trips": trips}

@app.get("/trips/{destination}")
def destination_trips(destination: str, currency: Optional[str] = "PLN"):
    rows = select_by_destination(destination)
    rate = exchange(currency)
    trips = []

    for row in rows:
        trip = dict(row)
        trip["price"] = str(convert_price(float(trip["price_pln"]), rate))
        trip["currency"] = currency.upper()
        del trip["price_pln"]
        trips.append(trip)

    return {"trips": trips}
