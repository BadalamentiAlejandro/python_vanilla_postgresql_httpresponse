import jwt
import datetime
from src.config.settings import JWT_EXPIRATION, JWT_SECRET
from src.views.api_response import send_error_response


def create_jwt(user_id: int) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=JWT_EXPIRATION)

    payload = {
        "sub": user_id,
        "exp": expire
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm = "HS256")
    return token


def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms = ["HS256"])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise

    except jwt.InvalidTokenError:
        raise


def get_jwt_from_response(handler) -> str:
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        send_error_response(handler, "Formato inválido. Bearer esperado", 401)
        return None

    try:
        token = auth.split("", 1)[1]
        return token
    
    except IndexError:
        send_error_response(handler, "Token no proporcionado luego de Bearer.", 401)
        return None