from typing import List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml
from pydantic import BaseModel

app = FastAPI()

with open("main.yml", "r") as f:
    main_yaml = yaml.safe_load(f)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = main_yaml
    return app.openapi_schema

app.openapi = custom_openapi


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

