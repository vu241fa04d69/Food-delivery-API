from fastapi import APIRouter
from core.email_otp import send_delivery_otp


router = APIRouter()

orders = []


@router.post("/place")
def place_order(
    user_id: int,
    total_amount: float
):

    order = {
        "order_id": len(orders) + 1,
        "user_id": user_id,
        "total_amount": total_amount,
        "status": "Pending"
    }

    orders.append(order)

    return {
        "message": "Order Placed Successfully",
        "order": order
    }


@router.get("/")
def get_orders():
    return orders
@router.post("/send-delivery-otp")
def send_order_otp(email: str):

    otp = send_delivery_otp(email)

    if otp:

        return {
            "message": "OTP sent successfully",
            "otp": otp
        }

    return {
        "message": "Failed to send OTP"
    }


@router.put("/update-status/{order_id}")
def update_status(
    order_id: int,
    status: str
):

    for order in orders:

        if order["order_id"] == order_id:

            order["status"] = status

            return {
                "message": "Order Updated",
                "order": order
            }

    return {
        "message": "Order Not Found"
    }