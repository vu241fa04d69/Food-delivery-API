import base64
import hashlib
import hmac
import json
import os
import time
from urllib.parse import parse_qs

from fastapi import APIRouter
from fastapi import Request
from fastapi import status
from fastapi.responses import RedirectResponse

from database.db_connection import SessionLocal
from database.db_models import User

router = APIRouter()

SECRET_KEY = "food_delivery_secret_key"
TOKEN_EXPIRE_SECONDS = 60 * 60
PASSWORD_ITERATIONS = 120000


def _encode(data: bytes):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _decode(data: str):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PASSWORD_ITERATIONS
    )

    return "pbkdf2_sha256${}${}${}".format(
        PASSWORD_ITERATIONS,
        _encode(salt),
        _encode(digest)
    )


def verify_password(plain_password: str, stored_password: str):
    if not stored_password.startswith("pbkdf2_sha256$"):
        return plain_password == stored_password

    _, iterations, salt, digest = stored_password.split("$", 3)
    calculated_digest = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode(),
        _decode(salt),
        int(iterations)
    )

    return hmac.compare_digest(
        _encode(calculated_digest),
        digest
    )


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = int(time.time()) + TOKEN_EXPIRE_SECONDS
    payload_json = json.dumps(
        payload,
        separators=(",", ":")
    ).encode()
    encoded_payload = _encode(payload_json)
    signature = hmac.new(
        SECRET_KEY.encode(),
        encoded_payload.encode(),
        hashlib.sha256
    ).digest()

    return "{}.{}".format(
        encoded_payload,
        _encode(signature)
    )


def decode_access_token(token: str):
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
    except ValueError:
        return None

    expected_signature = hmac.new(
        SECRET_KEY.encode(),
        encoded_payload.encode(),
        hashlib.sha256
    ).digest()

    if not hmac.compare_digest(
        _encode(expected_signature),
        encoded_signature
    ):
        return None

    try:
        payload = json.loads(_decode(encoded_payload))
    except (json.JSONDecodeError, ValueError):
        return None

    if payload.get("exp", 0) < int(time.time()):
        return None

    return payload


async def get_form_data(request: Request):
    body = await request.body()
    parsed_body = parse_qs(body.decode())

    return {
        key: values[0]
        for key, values in parsed_body.items()
    }


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = decode_access_token(token)

    if not payload:
        return None

    user_id = payload.get("sub")

    if not user_id:
        return None

    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == int(user_id)).first()
    finally:
        db.close()


@router.post("/register")
async def register(request: Request):
    form_data = await get_form_data(request)
    name = form_data.get("name", "").strip()
    email = form_data.get("email", "").strip()
    password = form_data.get("password", "")

    if not name or not email or not password:
        return RedirectResponse(
            url="/register?error=All fields are required",
            status_code=status.HTTP_303_SEE_OTHER
        )

    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            return RedirectResponse(
                url="/register?error=Email already registered",
                status_code=status.HTTP_303_SEE_OTHER
            )

        user = User(
            name=name,
            email=email,
            password=hash_password(password)
        )

        db.add(user)
        db.commit()

        return RedirectResponse(
            url="/login?message=Registration successful. Please login.",
            status_code=status.HTTP_303_SEE_OTHER
        )
    finally:
        db.close()


@router.post("/login")
async def login(request: Request):
    form_data = await get_form_data(request)
    email = form_data.get("email", "").strip()
    password = form_data.get("password", "")

    if not email or not password:
        return RedirectResponse(
            url="/login?error=Please fill all fields",
            status_code=status.HTTP_303_SEE_OTHER
        )

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return RedirectResponse(
                url="/login?error=Invalid email or password",
                status_code=status.HTTP_303_SEE_OTHER
            )

        if not verify_password(password, user.password):
            return RedirectResponse(
                url="/login?error=Invalid email or password",
                status_code=status.HTTP_303_SEE_OTHER
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        response = RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax"
        )

        return response
    finally:
        db.close()


@router.get("/logout")
def logout():
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")

    return response


@router.get("/users")
def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()
