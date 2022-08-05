import requests
import json


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
                f'upload {progress_bar} photo from {len(file)} *** response from server *** {response.status_code}')
            progress_bar += 1
            if 200 <= response.status_code < 400:
                print('photos uploaded \n')
            elif response.status_code >= 400:
                print(f'Ошибка {response.status_code}')
        return self.json_file(file)