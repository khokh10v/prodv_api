
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from .models import Tag, TagRead, TagUpdate
from app.database.database import get_session
from ...auth.auth import get_current_active_user
from app.services import storage_post
from app.services.post import change_post_url, change_posts_url


tag_router = APIRouter()


# ---------------
# Create Tag
# ---------------
@tag_router.post("/tags/", response_model=Tag)
def create_tag_my(*, 
        session: Session = Depends(get_session),
        tag: Tag,
        # current_value: ValueBase = Depends(get_current_active_user)
    ):
    tag = tag.from_orm(tag) # Подготовка для записи в базу (pydantic)
    session.add(tag)
    session.commit()
    session.refresh(tag) # Установится уже новый Id пользователя
    return tag # Выдаем созданный пост


# ---------------
# Read One Tag
# ---------------
@tag_router.get("/tags/{tag_id}", response_model=TagRead)
def read_tag(*, 
        session: Session = Depends(get_session), 
        tag_id: int,
        # current_user: User = Depends(get_current_active_user)
    ):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


# ---------------
# Read All Tags
# ---------------
@tag_router.get("/tags/", response_model=List[TagRead])
def read_posts(*,
        session: Session = Depends(get_session),
        offset: int = 0, limit: int = Query(default=100, lte=100),
        # current_user: User = Depends(get_current_active_user)
    ):
    query = select(Tag)
    query = query.offset(offset).limit(limit) # Полюбому включаем
    posts = session.exec(query).all()
    return posts
      

# ---------------
# Update Tag
# ---------------
@tag_router.patch("/tags/{tag_id}")
def update_tag(*, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        tag_id: int, 
        tag: TagUpdate,
        # ... - обязательное поле
    ):
    # Если придет пароль то надо его будет - захешировать
    print("Обновление переменной")     
    print(tag)    
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    print(f"Успешно получили пользователя {type(db_tag)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    tag_data = tag.dict(exclude_unset=True) 
    print(f"Преобразовали в dict {type(tag_data)}")
    for key, tag in tag_data.items():
        print(f"Обрабатываем {key} {tag}")
        # более менее эквивалентно db_tag.key = tag 
        setattr(db_tag, key, tag) # Обновление в базе данных
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


# ---------------
# Delete Post
# ---------------
@tag_router.delete("/tags/{tag_id}")
def delete_tag(*, session: Session = Depends(get_session), tag_id: int):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag) # Удаляем тег из базы данных
    session.commit()
    return {"ok": True}

