
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from .models import Category, CategoryRead, CategoryUpdate
from app.database.database import get_session
from ...auth.auth import get_current_active_user
from app.services import storage
from app.services.avatar import change_avatar_url, change_avatars_url


category_router = APIRouter()


# ---------------
# Create Category
# ---------------
@category_router.post("/categorys/", response_model=Category)
def create_category(*, 
        session: Session = Depends(get_session),
        category: Category
    ):
    db_category = category.from_orm(category) # Подготовка для записи в базу
    session.add(db_category)
    session.commit()
    session.refresh(db_category) # Установится уже новый Id категории
    return db_category


# ---------------
# Read One Category
# ---------------
@category_router.get("/categorys/{category_id}", response_model=CategoryRead)
def read_category(*, 
        session: Session = Depends(get_session), 
        category_id: int
    ):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ---------------
# Read All Categorys
# ---------------
@category_router.get("/categorys/", response_model=List[CategoryRead])
def read_categorys(*,
        session: Session = Depends(get_session),
        offset: int = 0, limit: int = Query(default=100, lte=100)
    ):
    query = select(Category)
    query = query.offset(offset).limit(limit) # Полюбому включаем
    categorys = session.exec(query).all()
    # categorys_list = []
    # for category in query:
    #     category_data = category.dict()
    #     if category_data["category_id"]:
    #         # category_data["cover_path"] = MY_URL + category_data["cover"]
    #         category_data["category"] = category. # Добавляем теги
    #     categorys_list.append(category_data)
    # return categorys_list
    return categorys
      

# ---------------
# Update Category
# ---------------
@category_router.patch("/categorys/{category_id}", response_model=CategoryUpdate)
def update_category(*, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        category_id: int, 
        category: CategoryUpdate,
        # ... - обязательное поле
    ):    
    print(category)    
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Успешно получили пользователя {type(db_category)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    category_data = category.dict(exclude_unset=True) 

    print(f"Преобразовали в dict {type(category_data)}")
    for key, category in category_data.items():
        print(f"Обрабатываем {key} {category}")
        # более менее эквивалентно db_category.key = category 
        setattr(db_category, key, category) # Обновление в базе данных
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


# ---------------
# Delete Category
# ---------------
@category_router.delete("/categorys/{category_id}")
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    storage.delete_file(f"/categorys/avatars/{category_id}") # Удаляем аватарку
    session.delete(category) # Удаляем переменную из базы данных
    session.commit()
    return {"ok": True}

