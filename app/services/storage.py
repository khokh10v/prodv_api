
from distutils import extension
import os
import shutil
import random
from ..settings import MEDIA_ROOT, MEDIA_URL


# Надо передать файл куда сохранять файл
def create_dir(path, file_name):
    """ Создание директории для записи файла """
    print('Путь к директории файла ' + path)
    print("Проверяем нужно ли удалять старую директорию вместе с файлом")
    if os.path.exists(path):
        print(f'Путь {path} существует - удаляем директорию и все файлы в ней')
        shutil.rmtree(path)
    else:
        print("Не удалось удалить старую директорию")
    # Создаем директории для записи файла
    try:
        os.makedirs(path)
    except OSError:
        print ("Создать директорию не удалось")
    else:
        print ("Успешно создана новая директория ")
    
    # Надо сформировать 2 пути 
    # 1. URL path 
    # 2. ROOT path

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
    file_name = f"{random.randint(0, 1000)}_{file_name}.{file_extension}" 
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
def delete_file(path):
    """ Удаление файла """
    path = str(MEDIA_ROOT) + path
    if os.path.exists(path):
        print(f'Путь {path} существует - удаляем директорию и все файлы в ней')
        shutil.rmtree(path)
    else:
        print("Пути и так нет - так что все ок")
    return True