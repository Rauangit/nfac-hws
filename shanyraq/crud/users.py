from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserCreate, UserUpdate
from auth import hash_password


async def register_user(db: AsyncSession, new_user: UserCreate) -> User:
    encrypted_password = hash_password(new_user.password)
    user_instance = User(
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        hashed_password=encrypted_password
    )
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)
    return user_instance


async def fetch_user_by_id(db: AsyncSession, uid: int):
    query = select(User).filter(User.id == uid)
    result = await db.execute(query)
    return result.scalars().first()


async def fetch_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def modify_user(db: AsyncSession, uid: int, user_updates: UserUpdate):
    query = select(User).filter(User.id == uid)
    result = await db.execute(query)
    user_obj = result.scalars().first()

    if not user_obj:
        return None

    updates = user_updates.dict(exclude_unset=True)

    if "password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("password"))

    for attr, val in updates.items():
        setattr(user_obj, attr, val)

    await db.commit()
    await db.refresh(user_obj)
    return user_obj
