from typing import Optional
from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, Field
import functions

class TripIn(BaseModel):
    destination: str = Field(..., min_length=1)
    month: str = Field(..., min_length=1)
    price_pln: float = Field(..., ge=0)

class TripOut(TripIn):
    id: int


functions.db_create()

app = FastAPI()

# Dodanie endpointu /health zwracającego prosty status.
@app.get("/health")
def status():
    return {"status": "ok"}

@app.post("/trips", response_model=TripOut, status_code=201)
#@app.post("/trips")
def create_trip(trip: TripIn):
    try:
        result = functions.insert(trip.destination, trip.month, trip.price_pln)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/trips")
def list_trips(currency: Optional[str] = "PLN"):
    trips = functions.select_all()
    rate = functions.exchange(currency)

    for trip in trips:
        trip["price"] = str(functions.convert_price(float(trip["price_pln"]), rate))
        trip["currency"] = currency.upper()
        del trip["price_pln"]

    return {"trips": trips}

@app.get("/trips/{destination}")
def destination_trips(destination: str, currency: Optional[str] = "PLN"):
    rows = functions.select_dest(destination)
    rate = functions.exchange(currency)
    trips = []

    for row in rows:
        trip = dict(row)
        trip["price"] = str(functions.convert_price(float(trip["price_pln"]), rate))
        trip["currency"] = currency.upper()
        del trip["price_pln"]
        trips.append(trip)

    return {"trips": trips}
