
from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
from app.settings import SQLALCHEMY_DATABASE_URL


#  Настройка Alembic
#  1. pip install alembic
#  2. Create migrations files 
#     $ alembic init app/database/migrations
#  3. To .mako file ->
#     import sqlmodel
#  4. To env.py ->
#     from sqlmodel import SQLModel 
#     from app.routers.users.models import User 
#     target_metadata = SQLModel.metadata 
#  5. To alembic.ini ->
#     sqlalchemy.url = postgresql://postgres:jujym@localhost/prodv
#  6. Generate migrations 
#     $ alembic revision --autogenerate -m "init"
#  7. Upgrade db 
#     $ alembic upgrade head
#  8. Посмотреть все миграции
#     $ alembic history


# Доступ к базе SQLite 
# SQLITE_URL = f"sqlite:///database.db" 
# connect_args = {"check_same_thread": False} # Только для SQLight
# engine = create_engine(
#     SQLITE_URL, 
#     # echo=True, # Покажет полный вывод SQL Alchemy
#     connect_args=connect_args
#     )


# Доступ к базе Postgres
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # echo=True,
    )


# Создание таблиц
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Может его вынести в отдельный модуль ?
def get_session():
    """ Модуль для работы с базой данных """
    with Session(engine) as session:
        yield session
