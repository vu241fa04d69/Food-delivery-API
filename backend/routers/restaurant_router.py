from fastapi import APIRouter

router = APIRouter()

restaurants = []


@router.post("/add")
def add_restaurant(name: str, location: str):

    restaurant = {
        "id": len(restaurants) + 1,
        "name": name,
        "location": location
    }

    restaurants.append(restaurant)

    return {
        "message": "Restaurant Added",
        "restaurant": restaurant
    }


@router.get("/")
def get_restaurants():
    return restaurants


@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int):

    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    return {"message": "Restaurant Not Found"}