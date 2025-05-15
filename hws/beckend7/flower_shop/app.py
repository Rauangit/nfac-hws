# app.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import JWTError, jwt
from repositories import UsersRepository, FlowersRepository, PurchasesRepository
from schemas import UserCreate, Login, Token, FlowerCreate

# Настройки для JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# OAuth2PasswordBearer для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Функции для создания и проверки токенов
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Регистрация нового пользователя
@app.post("/signup")
def signup(user: UserCreate):
    existing_user = UsersRepository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UsersRepository.create_user(user.email, user.password, user.name, user.surname, user.photo)
    return {"message": "User created successfully", "user": new_user}

# Авторизация пользователя
@app.post("/login", response_model=Token)
def login(user: Login):
    db_user = UsersRepository.get_user_by_email(user.email)
    if db_user is None or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Информация о пользователе
@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UsersRepository.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return {"user": user}

# Получение списка цветов
@app.get("/flowers")
def get_flowers():
    flowers = FlowersRepository.get_all_flowers()
    return {"flowers": flowers}

# Добавление нового цветка
@app.post("/flowers")
def add_flower(flower: FlowerCreate):
    new_flower = FlowersRepository.create_flower(flower.name, flower.quantity, flower.price)
    return {"flower_id": new_flower.id}

# Добавление цветка в корзину (через куки)
@app.post("/cart/items")
def add_to_cart(flower_id: int):
    # Для простоты, корзина будет храниться в куках
    return {"message": "Flower added to cart", "flower_id": flower_id}

# Получение содержимого корзины
@app.get("/cart/items")
def get_cart_items():
    # Получение данных из куков и возвращение корзины (заглушка)
    return {"message": "Cart items", "items": []}

# Добавление покупок
@app.post("/purchased")
def purchase_items(token: str = Depends(oauth2_scheme)):
    # Получение данных корзины и добавление в покупки
    return {"message": "Items purchased"}

# Получение списка купленных цветов
@app.get("/purchased")
def get_purchased_items(token: str = Depends(oauth2_scheme)):
    return {"message": "Purchased items", "items": []}
