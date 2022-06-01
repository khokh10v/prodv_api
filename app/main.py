
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database.database import create_db_and_tables
from app.routers.auth.api import auth_router # Авторизация
from app.routers.users.api import user_router # Пользователи
from app.routers.values.api import value_router # Пользователи
from app.routers.posts.api import post_router
from app.routers.posts.files.api import file_router
from app.routers.posts.tags.api import tag_router
from app.routers.posts.categorys.api import category_router
from .settings import MEDIA_URL


# Руты + Настройка документации
app = FastAPI(
    title="prodv api",
    description="Бэкенд-сервер компании «Продвижение» 🚀",
    version="0.0.1",
    version_stamp="sss",
)


# CORS политика
origins = [
    "http://localhost:4000",
    "http://localhost:4000/api/users/me/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Урлы с которых мы будем принимать запросы
    allow_credentials=True, # Поддержка файлов Cookie для запросов cross-origin
    allow_methods=["*"], # Методы для которых разрешены перекрестные запросы
    allow_headers=["*"],
    expose_headers=['Access-Control-Allow-Origin']
)


# Создание таблиц при запуске сервера
# @app.on_event("startup")
# def on_startup():
#     """ События при старте системы """
#     create_db_and_tables()


# Медиа файлы - картинки, видео, пдф
# 1. Url пути, пример = media/users/avatars/1/66_user_avatar.jpg
# Должен начинаться с media - это приложение Starlett
# 2. Root пути для сервера NGINX
# Это пути на диске где хранятся файлы
# /Users/Desktop/prodv_api/media/values/avatars/3/101_value_avatar.jpg
app.mount("/media", StaticFiles(directory=MEDIA_URL), name="media")


# Категории
app.include_router(
    category_router,
    prefix="/api",
    tags=["Category"],
    )


# Теги
app.include_router(
    tag_router,
    prefix="/api",
    tags=["Tags"],
    )


# Файлы
app.include_router(
    file_router,
    prefix="/api",
    tags=["Files"],
    )


# Посты
app.include_router(
    post_router,
    prefix="/api",
    tags=["Posts"],
    )


# Авторизация  
app.include_router(
    auth_router,
    prefix="/api",
    tags=["Auth"], # Групиировка в документации
    ) # импортим роуты из api.py 


# Пользователи
app.include_router(
    user_router,
    prefix="/api",
    tags=["Users"],
    )


# Переменные
app.include_router(
    value_router,
    prefix="/api",
    tags=["Values"],
    )


