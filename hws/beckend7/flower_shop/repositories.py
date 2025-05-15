# repositories.py
from models import User, Flower, Purchase
from typing import List

class UsersRepository:
    users: List[User] = []

    @classmethod
    def create_user(cls, email: str, password: str, name: str, surname: str, photo: str = None) -> User:
        new_user = User(id=len(cls.users)+1, email=email, password=password, name=name, surname=surname, photo=photo)
        cls.users.append(new_user)
        return new_user

    @classmethod
    def get_user_by_email(cls, email: str) -> User:
        return next((user for user in cls.users if user.email == email), None)

class FlowersRepository:
    flowers: List[Flower] = []

    @classmethod
    def create_flower(cls, name: str, quantity: int, price: float) -> Flower:
        new_flower = Flower(id=len(cls.flowers)+1, name=name, quantity=quantity, price=price)
        cls.flowers.append(new_flower)
        return new_flower

    @classmethod
    def get_all_flowers(cls) -> List[Flower]:
        return cls.flowers

class PurchasesRepository:
    purchases: List[Purchase] = []

    @classmethod
    def add_purchase(cls, user_id: int, flower_id: int) -> Purchase:
        new_purchase = Purchase(user_id=user_id, flower_id=flower_id)
        cls.purchases.append(new_purchase)
        return new_purchase

    @classmethod
    def get_purchases_by_user(cls, user_id: int) -> List[Purchase]:
        return [purchase for purchase in cls.purchases if purchase.user_id == user_id]
