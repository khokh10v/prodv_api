
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from .models import User, UserCreate, UserRead, UserUpdate
from app.database.database import get_session
from ..auth.password import get_password_hash, verify_password
from ..auth.auth import get_current_active_user
from app.services import storage
from app.services.avatar import change_avatar_url, change_avatars_url


user_router = APIRouter()


# ---------------
# Create User
# ---------------
@user_router.post("/users/", response_model=UserCreate
    )
def create_user(*, 
        session: Session = Depends(get_session), 
        user: UserCreate,
        # current_user: User = Depends(get_current_active_user)
    ):
    """ Create user """
    # Это по сути может быть Регистрация пользователя
    hash = get_password_hash(user.hashed_password) # Хешируем пароль
    verify_password(user.hashed_password, hash) # Проверяем что норм захешировался
    user.hashed_password = hash # Пользователю кладем только хеш
    db_user = User.from_orm(user) # Подготовка для записи в базу
    session.add(db_user)
    session.commit()
    session.refresh(db_user) # Установится уже новый Id пользователя
    return db_user # На выходе убедимся что id это число с помощью пайдантик UserRead


# ---------------
# Read One User
# ---------------
@user_router.get("/users/{user_id}", response_model=UserRead)
def read_user(*, 
        session: Session = Depends(get_session), 
        user_id: int,
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Заменить путь к аватарке
    user_data = change_avatar_url(request, user)
    return user_data


# ---------------
# Read All Users
# ---------------
@user_router.get("/users/", response_model=List[UserRead])
def read_users( *,
        session: Session = Depends(get_session),
        offset: int = 0, limit: int = Query(default=100, lte=100),
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    # Заменить пути к файлам
    users_data = change_avatars_url(request, users) 
    return users_data


# ---------------
# Update Avatar User
# ---------------
@user_router.patch("/users/avatars/{user_id}")
def update_user_avatar(*,
        user_id: int, 
        file: UploadFile = File(...),
        session: Session = Depends(get_session),
    ):
    db_user = session.get(User, user_id) # Получаем пользователя
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        full_file_path = storage.save_file(
            # Тут путь относительно папки media
            f'/users/avatars/{user_id}', # Путь к директории
            "user_avatar", # Имя файла
            file # Файл для записи
            )
    except:
        raise HTTPException(status_code=404, detail="File not saved")
    setattr(db_user, "avatar", full_file_path) # Путь к айлу
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
      

# ---------------
# Update User
# ---------------
@user_router.patch("/users/{user_id}", response_model=UserRead)
def update_user(
        *, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        user_id: int, 
        user: UserUpdate,
        # ... - обязательное поле
    ):
    # Если придет пароль то надо его будет - захешировать
    print("Обновление пользователя") 
    if user.hashed_password:
        print("Пришел пароль")
        print(user)
        hash = get_password_hash(user.hashed_password) # Хешируем пароль
        verify_password(user.hashed_password, hash) # Проверяем что норм захешировался
        user.hashed_password = hash # Пользователю кладем только хеш
    else:
        print("Данные без пароля")       
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Успешно получили пользователя {type(db_user)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    user_data = user.dict(exclude_unset=True) 

    print(f"Преобразовали в dict {type(user_data)}")
    for key, value in user_data.items():
        print(f"Обрабатываем {key} {value}")
        # более менее эквивалентно db_user.key = value 
        setattr(db_user, key, value) # Обновление в базе данных
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# ---------------
# Delete User
# ---------------
@user_router.delete("/users/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    storage.delete_file(f"/users/avatars/{user_id}") # Удаляем аватарку
    session.delete(user)
    session.commit()
    return {"ok": True}
