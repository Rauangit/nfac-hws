from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserUpdate
from crud.users import add_user, fetch_user_by_id, modify_user_by_id, fetch_user_by_email
from database import get_session
from auth import hash_password, verify_password
from auth_jwt import create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def show_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def process_registration(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    encrypted_pw = hash_password(password)
    new_user = UserCreate(
        email=email,
        username=username,
        hashed_password=encrypted_pw,
        full_name=full_name
    )
    await add_user(db, new_user)
    return RedirectResponse("/", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    user = await fetch_user_by_email(email, db)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверный email или пароль"
        }, status_code=401)

    token = create_access_token({"sub": str(user.id)})
    redirect_response = RedirectResponse("/", status_code=302)
    redirect_response.set_cookie(key="access_token", value=token, httponly=True)
    return redirect_response


@router.get("/users/{user_id}", response_class=HTMLResponse)
async def view_user(user_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    user_record = await fetch_user_by_id(user_id, db)
    return templates.TemplateResponse("user_info.html", {"request": request, "user": user_record})


@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(user_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    user_record = await fetch_user_by_id(user_id, db)
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user_record})


@router.post("/users/{user_id}/edit", response_class=HTMLResponse)
async def update_user_data(
    user_id: int,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    encrypted_pw = hash_password(password)
    update_info = UserUpdate(
        email=email,
        username=username,
        hashed_password=encrypted_pw,
        full_name=full_name
    )
    await modify_user_by_id(user_id, db, update_info)
    return RedirectResponse("/", status_code=302)
