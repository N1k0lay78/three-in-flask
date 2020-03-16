import requests


def get_spn(*args):
    if len(args) == 1:
        toponym = args[0]
        poss = toponym['boundedBy']['Envelope']
        delta_x = str(float(str(list(map(lambda x: float(x), poss['upperCorner'].split()))[0] - list(map(float, poss['lowerCorner'].split()))[0])) / 3)
        delta_y = str(float(str(list(map(lambda x: float(x), poss['upperCorner'].split()))[1] - list(map(float, poss['lowerCorner'].split()))[1])) / 3)
    else:
        pos_1, pos_2 = args
        delta_x = str(abs(pos_1[0] - pos_2[0]))
        delta_y = str(abs(pos_1[1] - pos_2[1]))
    return delta_x, delta_y


def get_sity(sity):
    toponym_to_find = sity

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('gg')
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    # print(json.dumps(toponym, ensure_ascii=False, indent=4))
    pos = ','.join(toponym_coodrinates.split())
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(get_spn(toponym)),
        "l": "sat",
    }

    map_api_server = f"http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    return response.url
