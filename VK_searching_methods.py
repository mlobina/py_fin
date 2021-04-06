import json
from vk_api.exceptions import ApiError
from VK_DB_connections import VKUserConnection
vk_user = VKUserConnection().vk_session

def search_dating_users(sex, age_from, age_to, city, status):
    all_dating_users = []
    link_profile = 'https://vk.com/id'
    response = vk_user.method('users.search',
                              {'sort': 1,
                               'sex': sex,
                               'age_from': age_from,
                               'age_to': age_to,
                               'hometown': city,
                               'status': status,
                               'has_photo': 1,
                               'count': 25,
                               'online': 1})

    for item in response['items']:
        dating_user = [
            item['first_name'],
            item['last_name'],
            link_profile + str(item['id']),
            item['id']]

        all_dating_users.append(dating_user)
    return all_dating_users


def get_photo(owner_id, photo_count=25):
    version = '5.130'
    try:
        response = vk_user.method('photos.get',
                                  {'access_token': VKUserConnection().token,
                                   'v': version,
                                   'owner_id': owner_id,
                                   'album_id': 'profile',
                                   'count': photo_count,
                                   'extended': 1,
                                   'photo_sizes': 1,
                                   'has_photo': 1,
                                   })
    except ApiError:
        return 'Доступ к фото пользователя закрыт'

    dating_users_photos = []
    for i in range(photo_count):
        try:
            dating_users_photos.append(
                [response['items'][i]['likes']['count'], 'https://vk.com/' +
                 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
        except IndexError:
            dating_users_photos.append(['Фото отсутствует.'])

    return dating_users_photos


def sort_photos_by_likes(photos):
    result = []
    for item in photos:
        if item != ['Фото отсутствует.'] and photos != 'Доступ к фото пользователя закрыт':
            result.append(item)

    return sorted(result)

def json_create(lst, photos):
   res = {}
   res_list = []

   while len(res_list) < 10:

       for i, item in enumerate(lst):
           res['first_name'] = item[0]
           res['last_name'] = item[1]
           res['link'] = item[2]
           res['id'] = item[3]
           res['photos'] = photos
           res_list.append(res.copy())


       with open('result.json', 'a', encoding='UTF-8') as file:
           json.dump(res_list, file, ensure_ascii=False)

       print('Информация об отобранных пользователях загружена в json-файл')
       break
