from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(passowrd):
    return pwd_context.hash(passowrd)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)
