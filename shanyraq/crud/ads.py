from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.ads import Ads
from schemas.ads import AdsCreate, AdsUpdate


async def add_new_ad(db: AsyncSession, ad_in: AdsCreate) -> Ads:
    ad_instance = Ads(**ad_in.dict())
    db.add(ad_instance)
    await db.commit()
    await db.refresh(ad_instance)
    return ad_instance


async def fetch_all_ads(db: AsyncSession):
    query = select(Ads)
    result = await db.execute(query)
    return result.scalars().all()


async def fetch_ad_by_id(db: AsyncSession, ad_identifier: int):
    query = select(Ads).filter(Ads.id == ad_identifier)
    result = await db.execute(query)
    return result.scalars().first()


async def modify_ad(db: AsyncSession, ad_identifier: int, ad_updates: AdsUpdate):
    query = select(Ads).filter(Ads.id == ad_identifier)
    result = await db.execute(query)
    ad_record = result.scalars().first()
    if ad_record is None:
        return None
    update_data = ad_updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ad_record, key, value)
    await db.commit()
    await db.refresh(ad_record)
    return ad_record


async def remove_ad(db: AsyncSession, ad_identifier: int):
    query = select(Ads).filter(Ads.id == ad_identifier)
    result = await db.execute(query)
    ad_record = result.scalars().first()
    if ad_record is None:
        return False
    await db.delete(ad_record)
    await db.commit()
    return True
