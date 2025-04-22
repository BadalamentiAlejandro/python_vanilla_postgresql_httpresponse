from src.config.settings import BCRYPT_SALT_ROUNDS
import bcrypt


def hash_password(password, rounds: int = int(BCRYPT_SALT_ROUNDS)) -> str:

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt(rounds)

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def verify_password(password, hashed_password) -> bool:

    password_bytes = password.encode("utf-8")

    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)