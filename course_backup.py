import requests
import json
import datetime


class VKphoto:
    url = 'https://api.vk.com/method/'
    with open('cfg.txt', 'r') as file_object:
        token = file_object.read().strip()
    version = 5.131

    def __init__(self, id):
        self.id = id

    def user_photo(self):
        params = {'access_token': self.token,
                  'v': self.version,
                  'user_id': self.id,
                  'album_id': 'profile',
                  'extended': 1,
                  'count': count
                  }
        response = requests.get(self.url + 'photos.get', params).json()
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


class YAuploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def json_file(self, file):
        json_file = list()
        for info in file:
            json_file.append(dict([('file_name', info), ('size', file[info][1])]))
        with open('json-файл', 'w') as folder:
            json.dump(json_file, folder)
        return json_file

    def ya_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': 'photos'}
        response = requests.put(url, headers=headers, params=params)
        return response.json()

    def get_upload(self, file):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.ya_folder()
        headers = self.get_headers()
        progress_bar = 1
        for photo in file:
            params = {'url': file[photo][0], 'path': f'photos/{photo}.jpg'}
            response = requests.post(upload_url, headers=headers, params=params)
            print(
                f'upload {progress_bar} photo from {len(file)} ****** response from server ****** {response.status_code}')
            progress_bar += 1
        print('photos uploaded \n')
        return self.json_file(file)


if __name__ == '__main__':
    id = VKphoto(str(input('id пользователя VK: ')))
    count = int(input('Введите количество фото: '))
    token = YAuploader(str(input('токен с Полигона Яндекс Диска: ')))
    print(token.get_upload(id.user_photo()))