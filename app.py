from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
import os

app = FastAPI()

@app.get("/health")
def status():
   return {"status": "ok"}

