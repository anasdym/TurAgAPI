from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
import os
import sqlite3

app = FastAPI()

# Dodanie endpointu /health zwracającego prosty status.
@app.get("/health")
def status():
   return {"status": "ok"}

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

# Funkcja zwracająca wszystkie wpisy
def select_all():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trips')
        return cursor.fetchall()

# Funkcja zwracająca wpisy filtrowane po destination
def select_by_destination(destination):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM trips
            WHERE LOWER(destination) = LOWER(?)
        ''', (destination,))
        return cursor.fetchall()
