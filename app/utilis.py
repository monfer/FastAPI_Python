from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(pasword:str):
    return pwd_context.hash(pasword)


def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)