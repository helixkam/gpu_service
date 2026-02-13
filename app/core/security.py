from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_passwd(passwd: str) -> str:
    return passwd_context.hash(passwd)
