from pydantic import BaseModel


class FoodItemCreate(BaseModel):
    food_name: str
    price: float
    restaurant_id: int


class FoodItemResponse(BaseModel):
    id: int
    food_name: str
    price: float
    restaurant_id: int

    class Config:
        from_attributes = True