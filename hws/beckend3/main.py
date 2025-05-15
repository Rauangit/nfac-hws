from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import List
import uvicorn

app = FastAPI()

# Подключаем шаблоны
templates = Jinja2Templates(directory="templates")

# Временная база данных (список машин)
cars_db = [
    {"id": 1, "name": "Toyota Camry", "year": "2020"},
    {"id": 2, "name": "Ford Mustang", "year": "2021"},
    {"id": 3, "name": "Tesla Model S", "year": "2022"},
    {"id": 4, "name": "Honda Civic", "year": "2019"},
]

### 📌 1. Поиск машин (GET /cars/search)
@app.get("/cars/search")
async def search_cars(request: Request, car_name: str = ""):
    # Фильтруем машины по названию
    filtered_cars = [car for car in cars_db if car_name.lower() in car["name"].lower()]
    return templates.TemplateResponse("cars/search.html", {"request": request, "cars": filtered_cars, "car_name": car_name})

### 📌 2. Форма для добавления машины (GET /cars/new)
@app.get("/cars/new")
async def new_car_form(request: Request):
    return templates.TemplateResponse("cars/new.html", {"request": request})

### 📌 3. Добавление машины через POST (POST /cars/new)
@app.post("/cars/new")
async def add_car(name: str = Form(...), year: str = Form(...)):
    new_id = len(cars_db) + 1
    cars_db.append({"id": new_id, "name": name, "year": year})
    return RedirectResponse(url="/cars", status_code=303)

### 📌 4. Список машин (GET /cars)
@app.get("/cars")
async def list_cars(request: Request):
    return templates.TemplateResponse("cars/search.html", {"request": request, "cars": cars_db, "car_name": ""})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
