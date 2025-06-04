from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from crud.ads import fetch_ads, add_ad, fetch_ad_by_id, modify_ad, remove_ad
from schemas.ads import AdsCreate, AdsUpdate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: AsyncSession = Depends(get_session)):
    ads_list = await fetch_ads(db)
    return templates.TemplateResponse("index.html", {"request": request, "ads": ads_list})


@router.get("/ads/new", response_class=HTMLResponse)
async def ad_creation_form(request: Request):
    return templates.TemplateResponse("create_ad.html", {"request": request})


@router.post("/ads/new", response_class=HTMLResponse)
async def submit_new_ad(
    title: str = Form(...),
    descr: str = Form(...),
    price: int = Form(...),
    poster: str = Form(None),
    db: AsyncSession = Depends(get_session)
):
    new_ad = AdsCreate(title=title, descr=descr, price=price, poster=poster)
    await add_ad(db, new_ad)
    return RedirectResponse(url="/", status_code=302)


@router.get("/ads/{ad_id}", response_class=HTMLResponse)
async def view_ad(ad_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    ad_item = await fetch_ad_by_id(ad_id, db)
    return templates.TemplateResponse("full_page.html", {"request": request, "ad": ad_item})


@router.get("/ads/{ad_id}/edit", response_class=HTMLResponse)
async def edit_ad_form(ad_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    ad_item = await fetch_ad_by_id(ad_id, db)
    return templates.TemplateResponse("edit.html", {"request": request, "ad": ad_item})


@router.post("/ads/{ad_id}/edit", response_class=HTMLResponse)
async def submit_ad_edit(
    ad_id: int,
    title: str = Form(...),
    descr: str = Form(...),
    price: int = Form(...),
    poster: str = Form(None),
    db: AsyncSession = Depends(get_session)
):
    update_data = AdsUpdate(title=title, descr=descr, price=price, poster=poster)
    await modify_ad(ad_id, db, update_data)
    return RedirectResponse(url="/", status_code=303)


@router.post("/ads/{ad_id}/remove", response_class=HTMLResponse)
async def delete_advertisement(ad_id: int, db: AsyncSession = Depends(get_session)):
    await remove_ad(ad_id, db)
    return RedirectResponse(url="/", status_code=303)
