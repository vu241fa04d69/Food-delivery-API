from fastapi import FastAPI, Request
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db_connection import SessionLocal
from database.db_models import Restaurant, Menu

# Database
from database.db_connection import engine
from database.db_models import Base

# Routers
from routers.authentication_router import get_current_user
from routers.authentication_router import router as auth_router
from routers.restaurant_router import router as restaurant_router
from routers.food_menu_router import router as menu_router
from routers.shopping_cart_router import router as cart_router
from routers.order_router import router as order_router

# Create Database Tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title="Food Delivery Management System",
    version="1.0.0"
)

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="../frontend/static"),
    name="static"
)

# Templates Folder
templates = Jinja2Templates(
    directory="../frontend/templates"
)

# ==================================
# Include Routers
# ==================================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    restaurant_router,
    prefix="/restaurants",
    tags=["Restaurants"]
)

app.include_router(
    menu_router,
    prefix="/menu",
    tags=["Food Menu"]
)

app.include_router(
    cart_router,
    prefix="/cart",
    tags=["Shopping Cart"]
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"]
)

# ==================================
# HTML Pages
# ==================================
@app.get("/search")
def search_food(request: Request, q: str = ""):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    db = SessionLocal()

    foods = db.query(Menu).filter(
        Menu.food_name.ilike(f"%{q}%")
    ).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "foods": foods,
            "query": q,
            "user": user
        }
    )
@app.get("/")
def home(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    db = SessionLocal()
    

    restaurants = db.query(Restaurant).all()
    menu_items = db.query(Menu).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="home_page.html",
        context={
            "restaurants": restaurants,
            "menu_items": menu_items,
            "user": user
        }
    )


@app.get("/login")
def login_page(
    request: Request,
    error: str = "",
    message: str = ""
):
    if get_current_user(request):
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="user_login.html",
        context={
            "error": error,
            "message": message
        }
    )


@app.get("/register")
def register_page(request: Request, error: str = ""):
    if get_current_user(request):
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="user_register.html",
        context={"error": error}
    )


@app.get("/restaurants-page")
def restaurants_page(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="restaurant_list.html",
        context={"user": user}
    )


@app.get("/menu-page")
def menu_page(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="food_menu.html",
        context={"user": user}
    )


@app.get("/cart-page")
def cart_page(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="shopping_cart.html",
        context={"user": user}
    )


@app.get("/orders-page")
def orders_page(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="order_history.html",
        context={"user": user}
    )


@app.get("/admin")
def admin_dashboard(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={"user": user}
    )


# ==================================
# Health Check
# ==================================

@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "Food Delivery API Running Successfully"
    }
