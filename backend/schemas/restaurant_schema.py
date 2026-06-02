from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    location: str


class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True