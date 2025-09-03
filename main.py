from typing import List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml
from pydantic import BaseModel

app = FastAPI()
@app.get("/ping")
def ping():
    return {"message": "pong"}

class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

cars: List[Car] = []

@app.post("/cars", status_code=201)
def create_car(car: Car):
    cars.append(car)
    return car

@app.get("/cars")
def get_cars():
    return cars

@app.get("/cars/{car_id}")
def get_car(car_id: str):
    for car in cars:
        if car.identifier == car_id:
            return {f"status": 200, "data":{car}}
    return {f"status": 404, "message": "le car comportant l'id fourni n'existe pas ou n'a pas ete trouve"}

