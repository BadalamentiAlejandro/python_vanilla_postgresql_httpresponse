from src.controllers.auth_controller import register_user, get_users, login_user


def handle_register(handler):
    if handler.command == "POST":
        register_user(handler)

    else:
        handler.send_response(405)
        handler.send_header("Allow", "POST")
        handler.end_headers()


def handle_login(handler):
    if handler.command == "POST":
        login_user(handler)

    else:
        handler.send_response(405)
        handler.send_header("Allow", "POST")
        handler.end_headers()

        
def handle_users(handler):
    if handler.command == "GET":
        get_users(handler)

    else:
        handler.send_response(405)
        handler.send_header("Allow", "GET")
        handler.end_headers()

