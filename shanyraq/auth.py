from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Хешируем plain текстовый пароль и возвращаем хеш
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверяем, совпадает ли plain пароль с хешем
    return pwd_context.verify(plain_password, hashed_password)
