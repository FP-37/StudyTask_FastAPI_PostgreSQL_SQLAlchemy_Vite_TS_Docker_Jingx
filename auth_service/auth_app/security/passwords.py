from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_BYTES = 72

def _check_length(password: str) -> None:
    if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
        raise ValueError("Password is too long for bcrypt (max 72 bytes). Use a shorter password.")

def hash_password(password: str) -> str:
    _check_length(password)
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
        return False
    return pwd_context.verify(password, password_hash)
