
from passlib.context import CryptContext # Хеширование паролей


password_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password, hashed_password): # plain - простой
    """ Проверка пароля и хеша """
    is_verify = password_context.verify(plain_password, hashed_password)
    if is_verify:
        print("Пароль и хеш совпадают :)")
    else:
        print("Пароль и хеш несовпадают !!!")
    return is_verify


def get_password_hash(password):
    """ Получение хеша пользователя """
    return password_context.hash(password)