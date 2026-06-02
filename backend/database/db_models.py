from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from database.db_connection import Base


# =====================
# USER TABLE
# =====================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    email = Column(
        String(100),
        unique=True
    )

    password = Column(
        String(255)
    )


# =====================
# RESTAURANT TABLE
# =====================

class Restaurant(Base):

    __tablename__ = "restaurants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    location = Column(
        String(200)
    )


# =====================
# FOOD MENU TABLE
# =====================

class Menu(Base):

    __tablename__ = "menu"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    food_name = Column(
        String(100)
    )

    price = Column(
        Float
    )

    restaurant_id = Column(
        Integer
    )


# =====================
# CART TABLE
# =====================
class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    total_amount = Column(Float)

    status = Column(String(50))

    delivery_otp = Column(String(10))

class CartItem(Base):

    __tablename__ = "cart_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    food_name = Column(
        String(100)
    )

    quantity = Column(
        Integer
    )

    price = Column(
        Float
    )

    total = Column(
        Float
    )


# =====================
# ORDERS TABLE
# =====================

 