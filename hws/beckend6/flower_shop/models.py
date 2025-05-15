class User:
    def __init__(self, email, full_name, password_hash, photo):
        self.id = None  
        self.email = email
        self.full_name = full_name
        self.password_hash = password_hash
        self.photo = photo

class Flower:
    def __init__(self, name, quantity, price):
        self.id = None
        self.name = name
        self.quantity = quantity
        self.price = price

class Purchase:
    def __init__(self, user_id, flower_id):
        self.user_id = user_id
        self.flower_id = flower_id
