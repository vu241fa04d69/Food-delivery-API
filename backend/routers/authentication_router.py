from fastapi import APIRouter

router = APIRouter()

users = []

@router.post("/register")
def register(name: str, email: str, password: str):

    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": password
    }

    users.append(user)

    return {
        "message": "User Registered Successfully",
        "user": user
    }


@router.post("/login")
def login(email: str, password: str):

    for user in users:
        if user["email"] == email and user["password"] == password:
            return {
                "message": "Login Successful"
            }

    return {
        "message": "Invalid Email or Password"
    }


@router.get("/users")
def get_users():
    return users