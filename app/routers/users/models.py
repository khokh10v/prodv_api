
from typing import List, Optional
import datetime
from sqlmodel import SQLModel, Field, Column, VARCHAR, UniqueConstraint, Relationship
from pydantic import BaseModel, EmailStr
# Если раскоментарить то циклический импорт получится)
# from app.routers.posts.models import UserPostLink


# UserPostLink
class UserPostLink(SQLModel, table=True):
    # Удалять каскадом тоже надо
    user_id: Optional[int] = Field(
        default=None, nullable=False, foreign_key="user.id", primary_key=True
    )
    post_id: Optional[int] = Field(
        default=None, nullable=False, foreign_key="post.id", primary_key=True
    )
    # Добавить поля для взаимотношений пользователя с постом
    # Например прохождение поста - пользователь прочитал и ответил на вопросы
    completed: bool = Field(default=False) # Выполнил ли задание
    like: bool = Field(default=False) # Лайкнул пост
    dislike: bool = Field(default=False) # Дислайкнул пост
    bookmark: bool = Field(default=False) # Дислайкнул пост


class UserBase(SQLModel):
    """ Table for users """
    # email: EmailStr - можно на стр. поменять
    # А можно и не менять) типа tel отдельным сделать полем
    # И на входе потом анализировать почта или телефон ввели
    # tel: str = Column("tel", VARCHAR, unique=True, nullable=True, default=None) 
    # по умолчанию default = NULL, если можно конечно
    # Получается что у такого email, nullable=True
    # по умолчанию default = NULL,
    email: EmailStr = Field(
        index=True,
        sa_column=Column("email", VARCHAR, unique=True))
        # по умолчанию nullable=True, default = None
    # Чтобы по умолчанию создавать уникальные имена то надо 
    # UniqueConstraint('name', name='uq_user_account_name')
    tel: str = Field(
        index=True,
        sa_column=Column("tel", VARCHAR, unique=True))
        # по умолчанию nullable=True, default = None
    # hashed_password: str = Field() # Не нужен на чтении
    first_name: str = Field(default=None, index=True)
    last_name: str = Field(default=None, index=True) 
    middle_name: str = Field(default=None, index=True)
    avatar: str = Field(default=None)
    disabled: bool = Field(default=False)
    created: datetime.datetime = Field(default=datetime.datetime.now())
    # Права доступа ...
    # Может тут сделать типа таблицу Groups
    is_superuser: bool = Field(default=False) # Он такой один)
    is_staff: bool = Field(default=False) # Это администратор
    is_redactor: bool = Field(default=False) # Доступ для редактора блога
    is_writer: bool = Field(default=False) # Доступ для блогеров
    is_manager: bool = Field(default=False) # Доступ для наших менеджеров
    is_designer: bool = Field(default=False) # Доступ для партнерки
    is_student: bool = Field(default=False) # Доступ для студентов
    


 # !!! Надо поставить nullable=False - то алембик не добавлял id в каждую миграцию
class User(UserBase, table=True):
    """ Create table of users """
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    hashed_password: str = Field() # Для аутентификации
    posts: List["Post"] = Relationship(back_populates="author")


    #tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)
    userpostlink_posts: List["Post"] = Relationship(back_populates="userpostlink_users", link_model=UserPostLink)



# --------------
# ---  CRUD  ---
# --------------
class UserCreate(BaseModel):
    """ Создание пользователя по email и паролю """
    # email: EmailStr - можно на стр. поменять
    email: EmailStr # Email *
    hashed_password: str # Пароль пользователя *
    first_name: str # Имя
    tel: Optional[str] = None
    # class Config:
    #     orm_mode = True
    #     # allow_population_by_field_name = True


class UserRead(UserBase):
    """ Чтение одного пользователя и нескольких пользователей """
    id: int
    #email: Optional[str] # Если email = null
    tel: Optional[str] # Если email = null


class UserUpdate(BaseModel):
    """ Обновление пользователя 
    id -> нельзя обновлять
    emil -> нельзя обновлять 
    avatar -> тоже отдельно правится"""
    hashed_password: Optional[str] = None # Пароль
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    is_superuser: Optional[bool] = False # Администратор
    is_staff: Optional[bool] = False # Администратор
    is_manager: Optional[bool] = False # Доступ для наших менеджеров
    is_designer: Optional[bool] = False # Доступ для партнерки
