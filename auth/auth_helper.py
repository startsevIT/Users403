from uuid import UUID
from fastapi import Request
from auth.auth import decode_token

def get_token(request: Request) -> str:
    token = request.headers.get("authorization")
    if not token:
        raise ValueError('Токен не найден')
    return token

def token_validation(request : Request) -> None:
    get_user_id(request)
    
def get_user_id(request : Request) -> UUID:
    token : str = get_token(request)
    try:
        payload = decode_token(token)
    except ValueError as e:
        raise ValueError(e)

    user_id = payload.get('id')
    if not user_id:
        raise ValueError("Не найден ID пользователя")
    
    return UUID(user_id)