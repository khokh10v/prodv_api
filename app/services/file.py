
from ..settings import MEDIA_URL, MY_URL

def get_url(request):
    """ Создание url для получения файла """
    # if request.client.port:
    #     url = f"{request.url.scheme}://{request.client.host}:{str(request.url.port)}/"
    # else:
    url = f"{request.url.scheme}://{request.client.host}/"
    
    print(url)
    return url


def change_files_url(request, files):
    """ Change avatars url """
    # url = get_url(request) # Like a http://localhost:8000/ 
    files_list = []
    # print(type(files))
    for file in files:
        file_data = file.dict() # Преобразуем в дикт
        if file_data["file_path"]:
            file_data["file_path"] = MY_URL + file_data["file_path"] # Добавляем урл к аватарке
        files_list.append(file_data)
    return files_list
