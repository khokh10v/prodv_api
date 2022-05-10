
import os
from pathlib import Path

 
# ----------
# Auth
# ----------
# to get a string like this run: openssl rand -hex 32
# Секретный ключ для расчета хеша паролей
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Алгоритм хеширования паролей
ALGORITHM = "HS256"
# Время истечения токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


# ----------
# Postgres
# ----------
# Строка доступа к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jujym@localhost/prodv" 


# ----------
# Storage
# ----------
MY_URL="http://localhost:8000/"
# 1. Путь по которому будут забирать файлы с NGINX
MEDIA_URL = "media"

# 2. Путь по которому будут сохранятся файлы на ДИСК
# __file__ - путь к файлу из которого был загружен модуль
# с помощью этого можно будет использовать абсолютные пути 
# Вот наши пути в операционной системе
# /Users/sergeykhokhlov/Desktop/education_practice/prodv_api/app
# /Users/sergeykhokhlov/Desktop/education_practice/prodv_api/app/media
BASE_DIR = Path(__file__).resolve().parent.parent # Получает директорию приложения
MEDIA_ROOT = str(BASE_DIR.joinpath('media')) # Добавляем media

# On server 
# MEDIA_ROOT = '/home/www/media'