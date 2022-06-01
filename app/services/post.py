
from ..settings import MEDIA_URL, MY_URL

def get_url(request):
    """ Создание url для получения файла """
    # if request.client.port:
    #     url = f"{request.url.scheme}://{request.client.host}:{str(request.url.port)}/"
    # else:
    url = f"{request.url.scheme}://{request.client.host}/"
    
    print(url)
    return url


# Выдать полный url обложки
def change_post_url(request, post):
    post_data = post.dict() # Преобразуем в дикт
    if post_data["cover"]:
        post_data["cover_path"] = MY_URL + post_data["cover"] # Добавляем урл к аватарке
    return post_data


def change_posts_url(request, posts):
    """ Change avatars url """
    # url = get_url(request) # Like a http://localhost:8000/ 
    posts_list = []
    # print(type(posts))
    for post in posts:
        post_data = post.dict() # Преобразуем в дикт
        if post_data["cover"]:
            post_data["cover_path"] = MY_URL + post_data["cover"] # Добавляем урл к аватарке
        posts_list.append(post_data)
    return posts_list
