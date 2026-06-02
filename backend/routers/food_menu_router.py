from fastapi import APIRouter

router = APIRouter()

menu_items = []


@router.post("/add")
def add_food_item(
    food_name: str,
    price: float,
    restaurant_id: int
):

    item = {
        "id": len(menu_items) + 1,
        "food_name": food_name,
        "price": price,
        "restaurant_id": restaurant_id
    }

    menu_items.append(item)

    return {
        "message": "Food Item Added",
        "item": item
    }


@router.get("/")
def get_menu():
    return menu_items


@router.get("/{restaurant_id}")
def get_restaurant_menu(restaurant_id: int):

    result = []

    for item in menu_items:
        if item["restaurant_id"] == restaurant_id:
            result.append(item)

    return result