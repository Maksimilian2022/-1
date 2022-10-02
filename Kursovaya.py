import configparser
import requests
import os
#access_token = 'vk1.a.FOPeogRotD8mxzUyIs1li1ENNH19zPZRy1nWnJHcR8Bj6nHOQSyraeCCtgNEJbZc4a1ZZVaAQVq7TYIM37R-VIKGMJ59PBLMbodtOhflLfv_r7iPM8R0DZukNT6fe6fCqu_oBnUXz0v_v25EgT9z_ofRhJfBq1Oeub81djXC0cs6dINYLX3OJ5OSUDCXQTCv'
config = configparser.ConfigParser()
config.read("person.ini")
access_token = config['access_token']["token"]


def get_photo():
    global user_id
    user_id = input('Введите id ')
    amount_photo = input('Введите колличество фото ')
    photo_path = input('Введите путь для загрузки фото ')
    photos_dict = {}
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': user_id, 'album_id': 'wall', 'v': '5.81', 'access_token': access_token, 'extended': '1', 'count': amount_photo, 'photo_sizes':'1'}
    response = requests.get(url, params=params)
    for photo_max_size in response.json()['response']['items']:
        if photo_max_size.get('date') in photos_dict.values():
            photos_dict[photo_max_size['sizes'][-1]['url']] = [{"file_name": photo_max_size['likes']['count'] + '.' + photo_max_size.get('date'), "size": photo_max_size['sizes'][-1]['type']}]
        else:
            photos_dict[photo_max_size['sizes'][-1]['url']] = [{"file_name": photo_max_size['likes']['count'], "size": photo_max_size['sizes'][-1]['type']}]

    for photo_upload_folder in photos_dict:
        img = requests.get(photo_upload_folder, allow_redirects=True)
        photo_name = photos_dict.get(photo_upload_folder)[0]['file_name']
        if os.path.exists(photo_path):
            with open(photo_path + str(photo_name) + '.jpg', 'wb') as file:
                file.write(img.content)
                print(photo_path)
        else:
            add_file = os.mkdir(photo_path)
            with open(photo_path + str(photo_name) + '.jpg', 'wb') as file:
                file.write(img.content)
    return photos_dict

def post_ydisk():
    token = 'AQAAAABR6sW2AADLW-hiYhDRWkXIgVyXB5LPvQQ'
    y_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
    photos_dict = get_photo()
    for photo_post in photos_dict:
        name_photo_post = photos_dict.get(photo_post)[0]['file_name']
        params = {'path': name_photo_post, 'url': photo_post}
        put_resource = requests.post(url=y_url, params=params, headers=headers)
    return put_resource

#post_ydisk()

