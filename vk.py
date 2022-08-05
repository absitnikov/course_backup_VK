import requests
import datetime


class VKphoto:
    url = 'https://api.vk.com/method/'
    with open('cfg.txt', 'r') as file_object:
        token = file_object.read().strip()
    version = 5.131

    def __init__(self, id):
        self.id = id

    def user_photo(self, count):
        self.count = count

        params = {'access_token': self.token,
                  'v': self.version,
                  'user_id': self.id,
                  'album_id': 'profile',
                  'count': self.count,
                  'extended': 1
                  }

        response = requests.get(self.url + 'photos.get', params).json()
        status_code = requests.get(self.url + 'photos.get', params).status_code
        if status_code == 200:
            print(f'server ok response {status_code} \n')
        elif status_code >= 400:
            print(f'Ошибка {status_code} \n')
        dict_photo = {}
        for photo in response['response']['items']:
            if str(photo['likes']['count']) not in dict_photo:
                dict_photo[str(photo['likes']['count'])] = [photo['sizes'][-1]['url']]
                dict_photo[str(photo['likes']['count'])].append(photo['sizes'][-1]['type'])
            else:
                dict_photo[f"{photo['likes']['count']}_{datetime.date.fromtimestamp(photo['date'])}"] = [
                    photo['sizes'][-1]['url']]
                dict_photo[f"{photo['likes']['count']}_{datetime.date.fromtimestamp(photo['date'])}"].append(
                    photo['sizes'][-1]['type'])
        return dict_photo