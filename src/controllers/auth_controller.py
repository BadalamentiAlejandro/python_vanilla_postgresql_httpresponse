import json
import re
from src.models.user_model import User
from src.config.settings import BCRYPT_SALT_ROUNDS, EMAIL_REGEX_PATTERN
from src.utils.auth.hashing import hash_password

def register_user(handler):

    try:

        content_length = int(handler.headers.get("Content_Length", 0))

        post_data = handler.rfile.read(content_length)

        data = json.loads(post_data.decode("utf-8"))

        email = data.get("email")

        password = data.get("password")


        if not email or not password:

            handler.send_response(400)

            handler.send_header("Content-Type", "application/json")

            handler.end_headers()

            error_msg = {"error": "E-mail y password requeridos."}

            handler.wfile.write(json.dumps(error_msg).encode("utf-8"))

            return
        

        if not re.match(EMAIL_REGEX_PATTERN, email):

            handler.send_response(400)

            handler.send_header("Content-Type", "application/json")

            handler.end_headers()

            error_msg = {"error": "Formato de e-mail inválido."}

            handler.wfile.write(json.dumps(error_msg).encode("utf-8"))

            return
        

        hashed_password = hash_password(password, BCRYPT_SALT_ROUNDS)

        # Creation of the user
        user = User(email, hashed_password)


        if user.save():

            handler.send_response(201)

            handler.send_header("Content-Type", "application/json")

            handler.end_headers()

            succ_msg = {"success": "Usuario creado exitosamente.", "user_id": user.id}

            handler.wfile.write(json.dumps(succ_msg).encode("utf-8"))

        else:

            handler.send_response(500)

            handler.send_header("Content-Type", "application/jason")

            handler.end_headers()

            error_msg = {"error": "Error al registrar un usuario."}

            handler.wfile.write(json.dumps(error_msg).encode("utf-8"))


    except Exception as e:

        print("Error en register_user:", e)

        handler.send_response(500)

        handler.send_header("Content-Type", "application/json")

        handler.end_headers()

        error_msg = {"error": "Ha ocurrido un error en el servidor"}

        handler.wfile.write(json.dumps(error_msg).encode("utf-8"))



def get_users(handler):

    try:

        users = User.get_all_users()

        handler.send_response(200)

        handler.send_header("Content-Type", "application/json")

        handler.end_headers()

        # Returns the users as a response.
        handler.wfile.write(json.dumps(users).encode("utf-8"))

    except Exception as e:

        print("Error en get_users:", e)

        handler.send_response(500)

        handler.send_header("Content-Type", "application/json")

        handler.end_headers()

        error_msg = {"error": "Ha ocurrido un error al obtener los usuarios"}

        handler.wfile.write(json.dumps(error_msg).encode("utf-8"))