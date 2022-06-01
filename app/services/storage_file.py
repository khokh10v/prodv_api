
from distutils import extension
import os
import shutil
import random
from pathlib import Path
from ..settings import MEDIA_ROOT, MEDIA_URL


# Надо передать файл куда сохранять файл
def create_dir(path, file_name):
    """ Создание директории для записи файла """
    print("Проверяем нужно ли удалять старую директорию вместе с файлом")
    if os.path.exists(path):
        print(f'Путь {path} существует')
    else:
        try:
            os.makedirs(path) # Создаем директории для записи файла
        except OSError:
            print ("Создать директорию не удалось")
        else:
            print ("Успешно создана новая директория ")
    file_path = f'{path}/{file_name}'
    return file_path


def save_file_to_path(file_path, file):
    """ Сохранить файл в созданную директорию """
    print(f"Cохраняем файл {file_path}")
    if file.content_type == 'svg' or 'jpeg' or 'jpg':
        print(f"Разрешение файла в порядке :)")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Файл успешно записан")


# ---------------
# Save file
# ---------------
def save_file(path, file_name, file): 
    """ Полная функция записи файла """
   
    print("--------------------")
    print("---  Save file   ---")
    print("--------------------")
    # Full file name 
    file_extension = os.path.splitext(file.filename)[1][1:]
    file_name = f"{file_name}_{random.randint(0, 10000)}.{file_extension}" 
    print(f"1. Имя файла: {file_name}")
    # Путь для веб сервера NGINX
    url_path = f"media{path}/{file_name}"
    print(f"2. url_path = {url_path}")
    print(f"3. Создаем директории и удаляем старые файлы")
    root_path = f"{MEDIA_ROOT}{path}"
    
    # Create dir
    file_path = create_dir(
        root_path, # Dir
        f"{file_name}" # File name
    )
    print(f"4. root_path = {file_path}")
    # Save file
    save_file_to_path(file_path, file)
    full_file_path = path
    return url_path


# ---------------
# Delete file
# ---------------
def delete_file(deleted_file):
    """ Удаление файла """
    print(deleted_file.file_path)
    print(deleted_file.post_id)
    path = str(MEDIA_ROOT)[0:len(MEDIA_ROOT)-5] + str(deleted_file.file_path)
    print(path)
    if os.path.exists(path):
        print(f'Путь {path} существует - удаляем директорию и все файлы в ней')
        os.remove(path)
    else:
        print("Пути и так нет - так что все ок")
    return True