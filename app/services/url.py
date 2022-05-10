

def get_url(request):
    """ Создание url для записи файла """
    url = request.url.scheme + '://' + request.client.host +':' + str(request.url.port) + '/'
    print(url)
    return url
