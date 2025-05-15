import hashlib

class UsersRepository:
    _users = []
    _id_counter = 1

    @classmethod
    def add(cls, user):
        user.id = cls._id_counter
        cls._id_counter += 1
        cls._users.append(user)
    
    @classmethod
    def find_by_email(cls, email):
        return next((u for u in cls._users if u.email == email), None)
    
    @classmethod
    def get_by_id(cls, user_id):
        return next((u for u in cls._users if u.id == user_id), None)


class FlowersRepository:
    _flowers = []
    _id_counter = 1

    @classmethod
    def add(cls, flower):
        flower.id = cls._id_counter
        cls._id_counter += 1
        cls._flowers.append(flower)
    
    @classmethod
    def all(cls):
        return cls._flowers
    
    @classmethod
    def get(cls, flower_id):
        return next((f for f in cls._flowers if f.id == flower_id), None)


class PurchasesRepository:
    _purchases = []

    @classmethod
    def add(cls, purchase):
        cls._purchases.append(purchase)

    @classmethod
    def for_user(cls, user_id):
        return [p for p in cls._purchases if p.user_id == user_id]
