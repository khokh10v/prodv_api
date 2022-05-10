
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
# Import from our files
from app.database.database import engine
from ..users.models import User
from app.settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from .models import Token, TokenData
from ..auth.password import get_password_hash, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def get_user(email: str):
    """ Получение пользователя по Email """
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        print(f"Получили пользователя {user.email}")
        return user


def authenticate_user(email: str, password: str):
    """ Сравнение пароля и хеша пользователя """
    user = get_user(email) # Получаем пользователя
    if not user:
        return False
    # print(password)
    # print(user.hashed_password)
    if not verify_password(password, user.hashed_password):
        return False
    print(f"Пользователь {user.email}, успешно авторизован")
    return user 


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ Создание токена  """
    to_encode = data.copy() # Глубокое копирование
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire}) # Добавляем к дикту время истечения
    # Формируем токен на основе: email, expire, SECRET_KEY, алгоритм шифрования
    # Encode - зашифрован
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    sub = to_encode.get('sub')
    print(f"JWT Токен для {sub} успешно выписан")
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Получение текущего пользователя по токену 
    это похоже и будет авторизация при заходе на урл """
    print("Получить текущего пользователя")
    # Ошибка если в токене не будет почты
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Получить токен")
        # print(token)
        # Декодируем токен чтобы получить из него данные
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # Получаем sub из токена
        if email is None:
            raise credentials_exception # Если не получили почту - то ошибка
        token_data = TokenData(email=email) # TokenData - это пайдантик модель
        print(f"Email полученный из токена: {token_data}")
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email) # Получаем токен по email
    if user is None:
        raise credentials_exception
    print(f"Выдаем полученного пользователя: {user.email}")
    return user


# Эта функция потребуется в рутах
# Иерархия зависимостей:
# 1. get_current_active_user ->
# 2. get_current_user ->
# 3. oauth2_scheme
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """ Получение текущего активного пользователя """
    print("Получить активного пользователя")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user