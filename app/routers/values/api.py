
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from .models import Value, ValueBase, ValueCreate, ValueRead, ValueUpdate
from app.database.database import get_session
from ..auth.auth import get_current_active_user
from app.services import storage
from app.services.avatar import change_avatar_url, change_avatars_url


value_router = APIRouter()


# ---------------
# Create Value
# ---------------
@value_router.post("/values/", response_model=Value)
def create_value(*, 
        session: Session = Depends(get_session), # Полюбому передается -
        # значит надо вынести в отдельный модуль
        value: Value,
        # current_value: ValueBase = Depends(get_current_active_user)
    ):
    """ Create value """
    db_value = value.from_orm(value) # Подготовка для записи в базу
    session.add(db_value)
    session.commit()
    session.refresh(db_value) # Установится уже новый Id пользователя
    return db_value # На выходе убедимся что id это число с помощью пайдантик UserRead


# ---------------
# Read One Value
# ---------------
@value_router.get("/values/{value_id}", response_model=ValueRead)
def read_value(*, 
        session: Session = Depends(get_session), 
        value_id: int,
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    value = session.get(Value, value_id)
    if not value:
        raise HTTPException(status_code=404, detail="Value not found")
    print(type(value.dict()))
    value_data = change_avatar_url(request, value)
    return value_data


# ---------------
# Read All Values
# ---------------
@value_router.get("/values/", response_model=List[ValueRead])
def read_values(*,
        session: Session = Depends(get_session),
        offset: int = 0, limit: int = Query(default=100, lte=100),
        key: Optional[str] = Query(None), 
        subkey: Optional[str] = Query(None),
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    query = select(Value)
    if key: # Filtring by key
        print("Фильтруем по ключу")
        query = query.where(Value.key == key)
    if subkey: # Filtering by subkey
        print("Фильтруем по подключу")
        query = query.where(Value.subkey == subkey)
    query = query.offset(offset).limit(limit) # Полюбому включаем
    values = session.exec(query).all()   
    values_data = change_avatars_url(request, values) 
    return values_data


# ---------------
# Update Avatar Value
# ---------------
@value_router.patch("/values/avatars/{value_id}")
def update_value_avatar( 
        *,
        value_id: int, 
        file: UploadFile = File(...),
        session: Session = Depends(get_session),
        request: Request
    ):
    db_value = session.get(Value, value_id)
    if not db_value:
        raise HTTPException(status_code=404, detail="Value not found")
    try:
        full_file_path = storage.save_file(
            f'/values/avatars/{value_id}', # Путь к директории
            "value_avatar",# Имя файла
            file # Файл для записи
            )
    except:
        raise HTTPException(status_code=404, detail="File not saved")
    setattr(db_value, "avatar", full_file_path) # Обновление в базе данных
    session.add(db_value)
    session.commit()
    session.refresh(db_value)
    return db_value
      

# ---------------
# Update Value
# ---------------
@value_router.patch("/values/{value_id}"
    # , response_model=ValueUpdate
    )
def update_value(*, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        value_id: int, 
        value: ValueUpdate,
        # ... - обязательное поле
    ):
    # Если придет пароль то надо его будет - захешировать
    print("Обновление переменной")     
    print(value)    
    db_value = session.get(Value, value_id)
    if not db_value:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Успешно получили пользователя {type(db_value)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    value_data = value.dict(exclude_unset=True) 

    print(f"Преобразовали в dict {type(value_data)}")
    for key, value in value_data.items():
        print(f"Обрабатываем {key} {value}")
        # более менее эквивалентно db_value.key = value 
        setattr(db_value, key, value) # Обновление в базе данных
    session.add(db_value)
    session.commit()
    session.refresh(db_value)
    return db_value


# ---------------
# Delete User
# ---------------
@value_router.delete("/values/{value_id}")
def delete_value(*, session: Session = Depends(get_session), value_id: int):
    value = session.get(Value, value_id)
    if not value:
        raise HTTPException(status_code=404, detail="value not found")
    storage.delete_file(f"/values/avatars/{value_id}") # Удаляем аватарку
    session.delete(value) # Удаляем переменную из базы данных
    session.commit()
    return {"ok": True}


