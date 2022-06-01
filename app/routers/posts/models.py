
import datetime
import json
from trace import CoverageResults
from typing import List, Optional
import datetime
from sqlmodel import SQLModel, Field, Column, VARCHAR, TEXT, Relationship
from pydantic import BaseModel
from app.routers.users.models import User
from app.routers.posts.files.models import File 
from app.routers.posts.tags.models import PostTagLink, Tag
from app.routers.posts.categorys.models import Category


class PostBase(SQLModel):
    slug: str = Field( # ЧПУ страницы, по умолчанию nullable = True
        index=True,
        sa_column=Column("slug", VARCHAR, unique=True, nullable=False))
    slug_title: str = Field(default=None) # Title страницы
    slug_description: str = Field(default=None) # Description страницы
    title: str = Field(default=None) # Название статьи
    description: str = Field(default=None) # Краткое описание статьи
    post_type: str = Field(default=None) # Типа тега только строкой
    body: str = Field(sa_column=Column("body", TEXT, default=None)) # JSON Body
    published: datetime.datetime = Field(default=datetime.datetime.now()) # Дата публикации
    is_write: bool = Field(default=False) # Статья написана ?
    is_publish: bool = Field(default=False) # Статья опубликована ?

    # Аватар тоже бы удалить каскадно) - но это в апишке сделаем
    # Может тут своя апишка которая установит путь к файлу
    cover: str = Field(default=None) # Путь к файлу (по выбору или запись с фрона)
    cover_id: Optional[int] = Field(default=None) # Запись id напрямую )

    # Post.author_id ----> User.id
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Post.category_id ----> Category.id
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    author: Optional[User] = Relationship(back_populates="posts")
    category: Optional[Category] = Relationship(back_populates="posts")
     # File.posts ----> Post.id 
    files: List[File] = Relationship(
        # Каскадное удаление файлов поста при удалении поста
        sa_relationship_kwargs={"cascade": "delete"},
        back_populates="post",
    )
    tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)
    






# --------------
# ---  CRUD  ---
# --------------
class PostCreate(BaseModel):
    """ Создание пользователя по email и паролю """
    # email: EmailStr - можно на стр. поменять
    # id: Optional[int]
    slug: str # Email *
    body: Optional[str]
    author_id: int
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    # pass
# class PostCreate(PostBase):
#     """ Создание JSON поста """
#     # Сюда попадает id !!!
#     # Надо как то это убрать)
#     # slug: str
#     # author_id: int
#     # class Config:
#     #     orm_mode = True
#     pass
    


class PostRead(PostBase):
    """ Чтение одной JSON переменной """
    id: int
    cover_path: Optional[str]
    tags: Optional[List[Tag]]
    category: Optional[Category] = None


class PostUpdate(BaseModel): # Чисто пайдантик модель
    """ Обновление JSON переменной """
    slug: Optional[str] = None
    slug_title: Optional[str] = None
    slug_description: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    post_type: Optional[str] = None
    body: Optional[str] = None
    cover: Optional[str] = None
    cover_id: Optional[int] = None
    category_id: Optional[int] = None
    tags: Optional[List] = None
    # avatar: Optional[str] = None


    # Вариант с обратными связями 
    # Post.cover_id ----> File.id 
    # cover_id: Optional[int] = Field(default=None, foreign_key="file.id")
    # cover: Optional[File] = Relationship(
    #     sa_relationship_kwargs={
    #         "primaryjoin": "Post.cover_id==File.id", 
    #         "uselist": False, # Один к одному
    #         "lazy": "joined",
    #     }
    # )
    # files: List[File] = Relationship(
    #     back_populates="post",
    #     sa_relationship_kwargs={
    #         "foreign_keys": "File.post_id", # Потому что 2 ключа на таблицу файлов
    #     }
    # )


# class Post(PostBase, table=True):
#     """ Create table of Posts """
#     id: Optional[int] = Field(default=None, nullable=False, primary_key=True)

#     # Исходящая связь на таблицу Пользователей
#     # Post.author_id -----> User.id
#     # Post.author - получить автора поста
#     # User.posts - получить все посты пользователя
#     author: Optional[User] = Relationship(back_populates="posts")

#     # Исходящая связь на таблицу Файлов
#     # Post.cover_id -----> File.id
#     # Post.cover - получить файл на обложке
#     # File.posts - получить все посты файла - хотя только один пост
#     # cover: Optional["File"] = Relationship(back_populates="posts")

#     # Входящая связь из таблицы Файлов
#     # Post.id <----- File.post_id
#     # Post.files - получить все фалы поста
#     # File.post - получить пост который относится к файлу
#     files: List[File] = Relationship(back_populates="post",
#         # sa_relationship_kwargs={
#         #     "primaryjoin": "Power.hero_id==Hero.id", 
#         #     "lazy": "joined"
#         # }
#     )
#     # sa_relationship_kwargs={
#     #         "primaryjoin": "Hero.id==HeroPowerLink.hero_id",
#     #         "secondaryjoin": "HeroPowerLink.power_id==Power.id",
#     #     },

#     # Линк-связь с таблицей PostTagLink
#     # А тут еще надо разобраться как будут поля называться)
#     # Post.
#     # tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)