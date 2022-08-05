from ya import *
from vk import *


if __name__ == '__main__':

    id = VKphoto(str(input('id пользователя VK: ')))
    count = int(input('Введите количество фото: '))
    token = YAuploader(str(input('токен с Полигона Яндекс Диска: ')))
    print(token.get_upload(id.user_photo(count)))