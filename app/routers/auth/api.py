
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..users.models import User, UserRead
from app.settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from .models import Token, TokenData
from ..auth.auth import authenticate_user, create_access_token
from ..auth.auth import get_current_active_user
from app.services.avatar import change_avatar_url, change_avatars_url


auth_router = APIRouter()


# ---------------
# Token
# ---------------
@auth_router.post(
    "/token/", # Потом прибавим к нему /api
    response_model=Token # Должны вернуть ответ по этой модели пайдантика
)
async def login_for_access_token(
    # Форма авторизации
    # Принимаем данные form_data для аутентификации пользователя
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """ Аутентификация на сайте """
    print("------------------------")
    print("---   Authenticate   ---")
    print("------------------------")
    # Передаем в авторизацию логин и пароль
    user = authenticate_user(form_data.username, form_data.password)
    if not user: # Если пользователя не нашли то ошибку выдаем
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Создание токена 
    access_token = create_access_token(
        data={"sub": user.email}, # Sub - это ключ для формирования JWT
        expires_delta=access_token_expires # Время истечения токена
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------
# Users Me
# ---------------
@auth_router.get("/users/me/")
async def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_active_user)):
    """ Получение пользователя по токену """
    print("-----------------")
    print("---    Me     ---")
    print("-----------------")
    # print(current_user)
    user_data = change_avatar_url(request, current_user)
    return {"user": user_data}
