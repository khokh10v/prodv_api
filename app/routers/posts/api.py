
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import relationship
from .models import Post, PostBase, PostCreate, PostRead, PostUpdate
from .tags.models import Tag, PostTagLink
from app.database.database import get_session
from ..auth.auth import get_current_active_user
from app.services import storage_post
from app.services.post import change_post_url, change_posts_url
from app.settings import MEDIA_URL, MY_URL
import copy


post_router = APIRouter()


# ---------------
# Create Post
# ---------------
@post_router.post("/posts/", response_model=Post)
def create_post_my(*, 
        session: Session = Depends(get_session),
        post: Post,
        # current_value: ValueBase = Depends(get_current_active_user)
    ):
    post = post.from_orm(post) # Подготовка для записи в базу (pydantic)
    session.add(post)
    session.commit()
    session.refresh(post) # Установится уже новый Id пользователя
    print(post)
    return post # Выдаем созданный пост


# ---------------
# Read One Post
# ---------------
@post_router.get("/posts/{post_id}", response_model=PostRead)
def read_post(*, 
        session: Session = Depends(get_session), 
        post_id: int,
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # post_data = change_post_url(request, post) 
    post_data = post.dict() # Преобразуем в дикт
    if post_data["cover"]:
        post_data["cover_path"] = MY_URL + post_data["cover"] # Добавляем урл к аватарке
    post_data["tags"] = post.tags # Добавляем теги
    post_data["category"] = post.category # Добавляем категории
    return post_data


# ---------------
# Read All Posts
# ---------------
# response_model=List[PostRead]
@post_router.get("/posts/", )
def read_posts(*,
        session: Session = Depends(get_session),
        search: str = None,
        tags: str = None,
        category: int = None,
        offset: int = 0, limit: int = Query(default=100, lte=100),
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):


    # Парсим пришедшую строку тегов 
    if tags:
        print(f'Строка фильтрации тегов = {tags}')
        tags_count = tags.count("-")+1
        print(f'Количество тегов = {tags_count}')
        tags_list = [] # Массив тегов для выборки
        start = 0
        if tags_count > 1: # Если несколько тегов
            for number in range(tags_count):
                if number < tags_count-1:
                    end = tags.find('-', start)
                    tags_list.append(tags[start:end])
                    start = end+1
                else:
                    tags_list.append(tags[start:])
        if tags_count == 1: # Если один тег
            tags_list.append(tags)


        # Формируем фильтр по тегам
        tags_filters = []
        for tag in tags_list:
            print(tag)
            tags_filters.append(PostTagLink.tag_id == tag)
            print(tags_filters)
        print(tags_list)
        

    # Запрос к базе данных
    query = session.query(Post)
    if tags:
        query = query.select_from(PostTagLink, Post).join(PostTagLink)
        query = query.filter(or_(*tags_filters))
    if category:
        query = query.filter(Post.category_id == category)
    query = query.offset(offset).limit(limit) 
    query = query.all()
    
    
    # Добавление тегов к постам
    posts_list = []
    for post in query:
        post_data = post.dict()
        if post_data["cover"]:
            post_data["cover_path"] = MY_URL + post_data["cover"]
        post_data["tags"] = post.tags # Добавляем теги
        post_data["category"] = post.category # Добавляем категории
        posts_list.append(post_data)
    return posts_list








    # Всякий шлак старый - запросы в базу)))
    # query = session.query(Post)
    # if search:
    #     query = query.filter(Post.title.ilike(f'%{search}%'))
    # query = query.filter(Post.description.ilike(f'%Портфолио%'))
    # query = query.offset(offset).limit(limit)    
    # query = query.all()
    # 
    # 
    # Парсить будем строку
    #tags_filters = []
    # if tags:
    #     for tag in tags_list:
    #         print(tag)
    #         filters = tags_filters.append(PostTagLink.tag_id == tag)
    #         print(tags_filters)
    # query = query.filter(and_(*not_null_filters))
    # query = query.filter(*tags_filters)
    # query = query.join(PostTagLink)
    # 
    # query = query.filter(PostTagLink.tag_id == tag_id)
    # query = query.filter(
    #     or_(
    #         PostTagLink.tag_id == tag_id, 
    #         PostTagLink.tag_id == tag_id_2))
    # query = query.filter(or_(PostTagLink.tag_id == 19, PostTagLink.tag_id == 16))
    # if tags:
    #     for tag in tags_list:
    #         query = query.filter(PostTagLink.tag_id == tag)
    # query = query.filter(or_(PostTagLink.tag_id == 20))
    # if tags:
    #     for tag in tags_list:
    #         query = query.filter(PostTagLink.tag_id == tag)
    # query = query.filter(PostTagLink.tag_id == 19)  
      

# ---------------
# Update Post
# ---------------
@post_router.patch("/posts/{post_id}"
    # , response_model=postUpdate
    )
def update_post(*, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        post_id: int, 
        post: PostUpdate,
        # ... - обязательное поле
    ):
    # Если придет пароль то надо его будет - захешировать
    print("Обновление переменной")     
    print(post)    
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    print(f"Успешно получили пользователя {type(db_post)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    post_data = post.dict(exclude_unset=True) 
    print(f"Преобразовали в dict {type(post_data)}")
    for key, post in post_data.items():
        if key != 'tags':
            setattr(db_post, key, post) # Обновление в базе данных
        if key == 'tags':
            tags = post # Теги которые получили с фронта
            # Удаление всех тегов в посте
            if db_post.tags:
                tmp = copy.deepcopy(db_post.tags) # Глубокое копирование
                for tag in tmp:
                    print(f'Удаляем тег {tag.id}')
                    db_post.tags.remove(tag)
                session.commit()  
            # Запись новых тегов пришедших с фронта
            if tags:
                for tag in tags:
                    print(f'Добавляем тег {tag["id"]}') 
                    db_tag = session.get(Tag, tag['id'])
                    db_post.tags.append(db_tag)
         
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# ---------------
# Delete Post
# ---------------
@post_router.delete("/posts/{post_id}")
def delete_post(*, session: Session = Depends(get_session), post_id: int):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # При удалении поста удаляем все файлы поста
    storage_post.delete_post_path(f"/posts/{post_id}") 
    session.delete(post) # Удаляем переменную из базы данных
    session.commit()
    return {"ok": True}

