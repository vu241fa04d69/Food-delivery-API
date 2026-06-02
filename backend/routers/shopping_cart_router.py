from fastapi import APIRouter

router = APIRouter()

cart = []


@router.post("/add")
def add_to_cart(
    food_name: str,
    quantity: int,
    price: float
):

    item = {
        "food_name": food_name,
        "quantity": quantity,
        "price": price,
        "total": quantity * price
    }

    cart.append(item)

    return {
        "message": "Added To Cart",
        "item": item
    }


@router.get("/")
def view_cart():

    grand_total = sum(
        item["total"] for item in cart
    )

    return {
        "cart": cart,
        "grand_total": grand_total
    }


@router.delete("/clear")
def clear_cart():

    cart.clear()

    return {
        "message": "Cart Cleared"
    }