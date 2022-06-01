
from distutils import extension
import os
import shutil
import random
from ..settings import MEDIA_ROOT, MEDIA_URL


# ---------------
# Delete post path
# ---------------
def delete_post_path(deleted_path):
    """ Удаление файла """
    path = str(MEDIA_ROOT) + str(deleted_path)
    print(path)
    if os.path.exists(path):
        print(f'Путь {path} существует - удаляем директорию и все файлы в ней')
        shutil.rmtree(path)
    else:
        print("Пути и так нет - так что все ок")
    return True