
import datetime
import json
from trace import CoverageResults
from typing import List, Optional
import datetime
from sqlmodel import SQLModel, Field, Column, VARCHAR, TEXT, Relationship
from pydantic import BaseModel
# from app.routers.users.models import User
# from app.routers.posts.models import Post


# PostTagLink
class PostTagLink(SQLModel, table=True):
    # Удалять каскадом тоже надо
    tag_id: Optional[int] = Field(
        default=None, nullable=False, foreign_key="tag.id", primary_key=True
    )
    post_id: Optional[int] = Field(
        default=None, nullable=False, foreign_key="post.id", primary_key=True
    )


class TagBase(SQLModel):
    """ Table of Tags """
    name: str = Field(default=None)
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    tag_type: str = Field(default=None)
    color: str = Field(default=None)


class Tag(TagBase, table=True):
    """ Create table of Files """
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTagLink)


# --------------
# ---  CRUD  ---
# --------------
class TagCreate(BaseModel):
    """ Создание пользователя по email и паролю """
    # email: EmailStr - можно на стр. поменять
    # id: Optional[int]
    name: str 
    tag_type: str
    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    # pass
    

class TagRead(TagBase):
    """ Чтение одной JSON переменной """
    id: int


class TagUpdate(BaseModel): # Чисто пайдантик модель
    """ Обновление JSON переменной """
    name: Optional[str] 
    slug: Optional[str]
    title: Optional[str]
    description: Optional[str] 
    tag_type: Optional[str]
    color: Optional[str]