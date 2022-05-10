
from ..settings import MEDIA_URL

def get_url(request):
    """ Создание url для получения файла """
    # if request.client.port:
    #     url = f"{request.url.scheme}://{request.client.host}:{str(request.url.port)}/"
    # else:
    url = f"{request.url.scheme}://{request.client.host}/"
    
    print(url)
    return url


def change_avatar_url(request, user):
    """ Change avatar url  """
    url = get_url(request) # Like a http://localhost:8000/ - текущий урл
    # print(type(user))
    user_data = user.dict() # Преобразуем в дикт
    if user_data["avatar"]:
        user_data["avatar"] = url + user_data["avatar"] # Добавляем урл к аватарке
    return user_data


def change_avatars_url(request, users):
    """ Change avatars url """
    url = get_url(request) # Like a http://localhost:8000/ 
    users_list = []
    # print(type(users))
    for user in users:
        user_data = user.dict() # Преобразуем в дикт
        if user_data["avatar"]:
            user_data["avatar"] = url + user_data["avatar"] # Добавляем урл к аватарке
        users_list.append(user_data)
    return users_list
