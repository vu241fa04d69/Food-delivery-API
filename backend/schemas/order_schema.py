from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    total_amount: float


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True