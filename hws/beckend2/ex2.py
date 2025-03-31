from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel

app = FastAPI()

cars = [
    {"id": i, "name": f"Car {i}", "year": str(2000 + (i % 20))} for i in range(1, 101)
]

users = [
    {"id": i, "email": f"user{i}@example.com", "first_name": f"First{i}", "last_name": f"Last{i}", "username": f"user{i}"}
    for i in range(1, 51)
]

class Car(BaseModel):
    name: str
    year: str

class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str

@app.get("/cars", response_model=List[dict])
async def get_cars(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]

@app.post("/cars")
async def add_car(car: Car):
    new_car = {"id": len(cars) + 1, "name": car.name, "year": car.year}
    cars.append(new_car)
    return new_car

@app.get("/cars/{car_id}")
async def get_car_by_id(car_id: int):
    car = next((car for car in cars if car["id"] == car_id), None)
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    return car

@app.get("/users", response_class=HTMLResponse)
async def get_users(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    paginated_users = users[start:end]
    
    user_rows = "".join(
        f'<tr><td>{user["username"]}</td><td><a href="/users/{user["id"]}">{user["first_name"]} {user["last_name"]}</a></td></tr>'
        for user in paginated_users
    )
    
    pagination_links = "".join(
        f'<a href="/users?page={p}&limit={limit}">{p}</a> ' for p in range(1, (len(users) // limit) + 2)
    )
    
    return f"""
    <html>
    <body>
        <table border="1">
            <tr><th>Username</th><th>Name</th></tr>
            {user_rows}
        </table>
        <br>
        {pagination_links}
    </body>
    </html>
    """

@app.post("/users")
async def add_user(user: User):
    new_user = {"id": len(users) + 1, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "username": user.username}
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user_by_id(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    
    return f"""
    <html>
    <body>
        <h1>{user["first_name"]} {user["last_name"]}</h1>
        <p>Email: {user["email"]}</p>
        <p>Username: {user["username"]}</p>
    </body>
    </html>
    """
