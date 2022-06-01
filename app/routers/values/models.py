
import json
from typing import List, Optional
import datetime
from sqlmodel import SQLModel, Field, Column, VARCHAR, TEXT
from pydantic import BaseModel


class ValueBase(SQLModel):
    """ Table for Values """
    title: str = Field() # VARCHAR by default
    description: str = Field(default=None) 
    key: str = Field(index=True)
    subkey: str = Field(index=True) 
    value: str = Field(sa_column=Column("value", TEXT, default=None)) # Text Field
    avatar: str = Field(default=None)
    avatar_type: str = Field(default=None)


class Value(ValueBase, table=True):
    """ Create table of Values """
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


# --------------
# ---  CRUD  ---
# --------------
class ValueCreate(ValueBase):
    """ Создание JSON переменной """
    # Сюда попадает id !!!
    # Надо как то это убрать)
    pass


class ValueRead(ValueBase):
    """ Чтение одной JSON переменной """
    id: int


class ValueUpdate(BaseModel): # Чисто пайдантик модель
    """ Обновление JSON переменной """
    title: Optional[str] = None
    description: Optional[str] = None
    key: Optional[str] = None
    subkey: Optional[str] = None
    value: Optional[str] = None
    # avatar: Optional[str] = None