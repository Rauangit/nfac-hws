from typing import List

class User:
    def __init__(self, id: int, email: str, password: str, name: str, surname: str, photo: str = None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.photo = photo

class Flower:
    def __init__(self, id: int, name: str, quantity: int, price: float):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

class Purchase:
    def __init__(self, user_id: int, flower_id: int):
        self.user_id = user_id
        self.flower_id = flower_id
