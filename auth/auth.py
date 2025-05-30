from typing import Any
from datetime import datetime, timedelta, timezone
import jwt

def get_key() -> str:
    return "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt"

def get_algorithm() -> str:
    return "HS256"

def create_token(payload: dict[str, Any]) -> str:
    expire : datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expire})
    encode_jwt : str = jwt.encode(payload, get_key(), get_algorithm()) # type: ignore
    return encode_jwt

def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, get_key(), get_algorithm()) # type: ignore
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Токен умер")
    except jwt.InvalidTokenError:
        raise ValueError("Некорректный токен")


