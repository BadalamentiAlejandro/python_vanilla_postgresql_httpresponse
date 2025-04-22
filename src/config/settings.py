import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
DB_URL = os.getenv("DB_URL")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION"))

BCRYPT_SALT_ROUNDS = int(os.getenv("BCRYPT_SALT_ROUNDS"))

EMAIL_REGEX_PATTERN = os.getenv("EMAIL_REGEX_PATTERN")