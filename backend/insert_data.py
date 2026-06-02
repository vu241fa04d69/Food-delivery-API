from database.db_connection import SessionLocal
from database.db_models import Restaurant, Menu

db = SessionLocal()

restaurant1 = Restaurant(
    name="Pizza Hut",
    location="Vadlamudi"
)

restaurant2 = Restaurant(
    name="KFC",
    location="Mahatma Gandhi center"
)

db.add(restaurant1)
db.add(restaurant2)

db.commit()

menu1 = Menu(
    food_name="Veg Pizza",
    price=299,
    restaurant_id=1
)

menu2 = Menu(
    food_name="Chicken Burger",
    price=199,
    restaurant_id=2
)

db.add(menu1)
db.add(menu2)

db.commit()

print("Data Inserted Successfully")