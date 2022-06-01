
from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, VARCHAR, Relationship
from pydantic import BaseModel


class CategoryBase(SQLModel):
    # Fields like a tag
    name: str = Field( # Имя категории уникально
        index=True,
        sa_column=Column("name", VARCHAR, unique=True, nullable=False))
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    category_type: str = Field(default=None)
    color: str = Field(default=None)


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    posts: List['Post'] = Relationship(back_populates="category")


# --------------
# ---  CRUD  ---
# --------------


class CategoryRead(CategoryBase):
    id: int
    name: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category_type: Optional[str] = None
    color: Optional[str] = None


class CategoryUpdate(BaseModel): 
    name: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category_type: Optional[str] = None
    color: Optional[str] = None