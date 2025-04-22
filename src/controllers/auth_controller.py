import json
import re
from src.models.user_model import User
from src.config.settings import BCRYPT_SALT_ROUNDS, EMAIL_REGEX_PATTERN
from src.utils.auth.hashing import hash_password, verify_password
from src.views.api_response import send_error_response, send_json_response
from src.utils.auth.jwt import create_jwt, get_jwt_from_response, verify_jwt

def register_user(handler):
    try:
        content_length = int(handler.headers.get("Content-Length", 0))
        post_data = handler.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return send_error_response(handler, "E-mail y password requeridos.", 400)
            
        
        if not re.match(EMAIL_REGEX_PATTERN, email):
            return send_error_response(handler, "Formato de e-mail inválido.", 400)
        
        hashed_password = hash_password(password, BCRYPT_SALT_ROUNDS)

        # Creation of the user
        user = User(email, hashed_password)

        if user.save():
            return send_json_response(handler, {"success": "Usuario creado exitosamente", "user_id": user.id}, 201)
        else:
            return send_error_response(handler, "Error al registrar un usuario.", 500)

    except Exception as e:
        print("Error en register_user:", e)
        return send_error_response(handler, "Ha ocurrido un error en el servidor.", 500)


def login_user(handler):
    try:
        content_length = int(handler.headers.get("Content-Length", 0))
        post_data = handler.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))
        email = data.get("email")
        password = data.get("password")

        if not email or not password: # Verify user added email and password.
            return send_error_response(handler, "E-mail y password requeridos.", 400)

        user_record = User.get_by_email(email)
        if not user_record: # Verify user exists with this email.
            return send_error_response(handler, "Credenciales inválidas.", 401)

        if not verify_password(password, user_record["password"]):
            return send_error_response(handler, "Password incorrecto", 401)

        token = create_jwt(user_record["id"])        
        return send_json_response(handler, {"token": token}, 200) # Returns token as response.
    
    except Exception as e:
        print("Error en login_user:", e)
        return send_error_response(handler, "Error en el servidor", 500)


def get_users(handler):
    token = get_jwt_from_response(handler)
    if token is None:
        return
    
    try:
        payload = verify_jwt(token)

    except Exception as e:
        print("Error en get_users:", e)
        return send_error_response(handler, "Token inválido.", 500)

    users = User.get_all_users()
    return send_json_response(handler, users, 200) # Returns the users as a response.