import requests
import json
import configparser


def config_data(need_token):
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config['VK'][need_token]



def get_photo():
    user_id = input('Введите id ')
    token = config_data('vk_token')
    access_token = config_data('vk_access_token')
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
    if user_id.isdigit() != True:
        url = 'https://api.vk.com/method/users.get'
        params_screen = {'user_ids': user_id, 'fields': "user_id", 'name_case': "Nom", 'v': '5.81'}
        screen_name = requests.get(url=url, params=params_screen, headers=headers).json()
        user_id = screen_name.get('response')[0].get('id')
    amount_photo = input('Введите колличество фото ')
    photos_dict = {}
    url = 'https://api.vk.com/method/photos.get'
    params = {f"owner_id": user_id, 'album_id': 'profile', 'access_token': access_token, 'v': '5.81', 'extended': '1', 'count': amount_photo, 'photo_sizes': '1'}
    response = requests.get(url, params=params)
    for photo_max_size in response.json()['response']['items']:
        if photo_max_size.get('date') in photos_dict.values():
            photos_dict[photo_max_size['sizes'][-1]['url']] = [{"file_name": photo_max_size['likes']['count'] + '.' + photo_max_size.get('date'), "size": photo_max_size['sizes'][-1]['type']}]
        else:
            photos_dict[photo_max_size['sizes'][-1]['url']] = [{"file_name": photo_max_size['likes']['count'], "size": photo_max_size['sizes'][-1]['type']}]
    for photo_upload_folder in photos_dict:
        img = requests.get(photo_upload_folder, allow_redirects=True)
        photo_name = photos_dict.get(photo_upload_folder)[0]['file_name']
    with open("photo.json", "w") as write_json:
        write_json.write(json.dumps(photos_dict))
    return photos_dict

def post_ydisk():
    photo_path = input('Введите имя папки ')
    token = config_data('vk_token')
    y_url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
    y_url_add_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
    photos_dict = get_photo()
    params_add_folder = {'path': f"/{photo_path}"}
    add_folder = requests.put(url=y_url_add_folder, params=params_add_folder, headers=headers)
    for photo_post in photos_dict:
        print(photo_post)
        name_photo_post = photos_dict.get(photo_post)[0]['file_name']
        params = {'path': f"{photo_path}/{name_photo_post}", 'url': photo_post}
        put_resource = requests.post(url=y_url, params=params, headers=headers)
    return

post_ydisk()