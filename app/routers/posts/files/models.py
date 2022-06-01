
#from sqlalchemy.orm import 
from typing import List, Optional
import datetime
from sqlalchemy import delete
from sqlmodel import SQLModel, Field, Column, VARCHAR, TEXT, Relationship
from pydantic import BaseModel


class FileBase(SQLModel):
    file_path: str = Field(default=None)
    file_type: str = Field(default=None)
    
    # File.post_id -----> Post.id 
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    

class File(FileBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    # File.post - получаем пост к которому принадлежит этот файл
    post: Optional["Post"] = Relationship(back_populates="files") 




    

# class File(FileBase, table=True):
#     """ Create table of Files """
#     id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    
#     # Исходящая связь на таблицу Постов
#     # File.post_id -----> Post.id 
#     # File.post - получить пост файла
#     # Post.files - получить все файлы поста
#     post: Optional["Post"] = Relationship(back_populates="files") 

#     # Входящая связь из таблицы Постов (Обложка)
#     # File.id <----- Post.cover_id
#     # File.postscover - получить все посты файла
#     # Post.files - получить все фалы поста
#     # posts: List[Post] = Relationship(back_populates="files") # Cover


# --------------
# ---  CRUD  ---
# --------------
class FileCreate(BaseModel):
    """ Создание пользователя по email и паролю """
    # email: EmailStr - можно на стр. поменять
    # id: Optional[int]
    # slug: str # Email *
    # body: str
    # author_id: int
    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    pass
# class FileCreate(FileBase):
#     """ Создание JSON поста """
#     # Сюда попадает id !!!
#     # Надо как то это убрать)
#     # slug: str
#     # author_id: int
#     # class Config:
#     #     orm_mode = True
#     pass
    


class FileRead(FileBase):
    """ Чтение одной JSON переменной """
    id: int


class FileUpdate(BaseModel): # Чисто пайдантик модель
    """ Обновление JSON переменной """
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    post_id: Optional[int] = None






    # Можно так конечно попробовать сделать
    # Но так оч много гемора в плане что непонятно как забирать обложку
    # is_cover: bool = Field(default=False)


    # Файл из примера Алхимии
    # parent_id = Column(Integer, ForeignKey('parent.id', ondelete="CASCADE"))
    # parent = relationship("Parent", back_populates="children")
    # У файла один пост
    
    
    # Вариант с обратными связями
    # post: Optional["Post"] = Relationship(
    #     sa_relationship_kwargs={
    #         "primaryjoin": "File.post_id==Post.id", 
    #         "lazy": "joined"
    #     },
    #     back_populates="files",
    # ) 
    # post: Optional["Post"] = Relationship(back_populates="files")
    # to_account: Account = Relationship(
    #     sa_relationship=RelationshipProperty("Account", foreign_keys=[to_account_id]))