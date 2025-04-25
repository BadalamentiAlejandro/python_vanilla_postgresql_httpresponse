from http.server import BaseHTTPRequestHandler, HTTPServer
print("--- >>> El script app.py ha comenzado a ejecutarse dentro del contenedor <<< ---")
from urllib.parse import urlparse
from src.routes import auth_routes
from src.config.settings import HOST, PORT


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.route_request()


    def do_POST(self):

        self.route_request()


    def route_request(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        method = self.command

        print(f"Recibida peticion {method} para la ruta {path}")

        if path.startswith("/register"):            
            auth_routes.handle_register(self)

        elif path.startswith("/users"):
            auth_routes.handle_users(self)

        elif path.startswith("/login"):
            auth_routes.handle_login(self)

        else:
            self.response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada.")


def run_server():
    server_adress = (HOST, int(PORT))
    httpd = HTTPServer(server_adress, SimpleHTTPRequestHandler)

    print(f"Iniciando servidor HTTP en {HOST}: {PORT}...")

    httpd.serve_forever()


if __name__ == "__main__":    
    run_server()