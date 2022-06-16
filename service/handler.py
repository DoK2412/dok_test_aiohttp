import os
import jwt


from aiohttp import web
from service.images import save_images, image_output
from service.usermodel import registration, authorization, entrance_control
from main import log_error, log_info


class Handler:

    def __init__(self):
        pass

    async def token_processing(self, request):
        """
        Функция проверки валидности токена и получения данных от него.
        :param request: - получаем данные из запроса и работаем с заголовками
        :return: - после раскрытия токена возвращаем необходимые данные
                   (в нашем случае id пользователя)
        """
        try:
            token = request.headers['Authorization'].split(' ')[1]
            data_user = jwt.decode(token, os.getenv("SIKRET"),
                                   algorithms=['HS256', ])
            log_info.info(f"Функция раскодировара токен пользователя:"
                          f" {data_user['username']} и передала в работу")
            return data_user
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)

    async def handler_get_user(self, request):
        pass

    async def handler_auth_user(self, request):
        """
        Функция предназначена для входа пользователя в систему,
        при успешном входе пользователю формируется токен для
        работы на сервере.
        :param request: - входные данные от пользователя (логин, пароль)
        :return: - возвращает токен пользователя для работы
        """
        try:
            data = await request.json()
            addendum = await authorization(data)
            if addendum.get('id'):
                tokens = await entrance_control(addendum)
                log_info.info(f"Функция произвела вход пользователя "
                              f"{data['username']}вернула валидный токен")
                return web.json_response(tokens)
            else:
                log_info.info(f"Функция отклонила вход пользователя: "
                              f"{data['username']}")
                return web.json_response(addendum)
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)

    async def handler_registration_user(self, request):
        """
        Функция предназначена для регистрации пользоватеря в системе
        и записи его в базе данных.
        :param request: - получает словарь из пользовательских данных
                          (лигин, пароль)
        :return: - возвращает ответ об конечном результате программы
        """
        try:
            data = await request.json()
            reg = await registration(data)
            log_info.info(f"Функция завершила регистрационные действия "
                          f"с пользователем {data['username']}")
            return web.json_response(reg)
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)

    async def create_new_images(self, request):
        """
        Функция предназначена для получения изображения от пользователя
        и дальнейшей работе с ним
        :param request: - получает на вход файл с изображением
        :return: - возвращает ответ о ходе сохранения изображения в
        базе данных и о изменениях с ним
        """

        try:
            user_id = await self.token_processing(request)
            file = await request.post()
            saving_image = await save_images(file, user_id)
            return web.json_response(saving_image)
        except jwt.exceptions.DecodeError:
            log_error.error('Токен не валиден. Ошибка: ', exc_info=True)
            return web.json_response({'status': '423',
                                      'message': 'The user token is not'
                                                 ' active'})

    async def conclusion_log_info(self, request):
        """
        Функция предназначена для вывода логов протекающей рабты приложения
        :return: - содержимое файла info.log
        """
        try:
            log_info.info("Выведен файл логирования протекающей информации")
            return web.FileResponse(os.path.abspath(os.path.join('loggings', 'info.log')))
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)

    async def conclusion_log_error(self, request):
        """
        Функция предназначена для вывода логав ошибок программы.
        :return: - содержимое файла error.log
        """
        try:
            log_info.info("Выведен файл логирования полученных ошибок")
            return web.FileResponse(os.path.abspath(os.path.join('loggings', 'error.log')))
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)

    async def out_img(self, request):
        """
        Функция предназначена для вывода пользователю изображения
        из базы данных
        :param request: - на вход получает id необходимого изображения в базе
        :return: - возвращает изображение либо ответ о том что
                   изображение отсутствует
        """
        try:
            user = await self.token_processing(request)
            id = request.match_info['id']
            file = await image_output(id, user)
            if type(file) is not dict:
                url = os.path.relpath(file)  # путь к файлу
                log_info.info(f"Функция вернула изобрадение пользователю:"
                              f" {user['username']}")
                return web.FileResponse(url)  # вывод изображения
            else:
                log_info.info(f"Функция отклонила вывод изображения"
                              f" пользователю: {user['username']}")
                return web.json_response(file)
        except Exception:
            log_error.error('Получено исключение: ', exc_info=True)