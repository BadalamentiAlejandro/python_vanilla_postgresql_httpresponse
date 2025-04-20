from src.config.settings import BCRYPT_SALT_ROUNDS
import bcrypt


def hash_password(password, rounds: int = BCRYPT_SALT_ROUNDS) -> str:

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt(rounds)

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")