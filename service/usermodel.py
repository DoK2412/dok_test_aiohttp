import hashlib  # хэширование паролей
import asyncpg  # sql база
import os  # пути в env
import codecs  # кодирование
import jwt  # токены
import datetime  # даты

from main import log_error, log_info


async def withdrawal_request(data: dict) -> dict:
    """
    Функция предназначена для запроса данных о пользователе и возврате
    данных о нем.
    :param data: - данные полученные от пользователя
    :return: - возврат полученных данных о пользователе в виде словаря:
    """
    try:
        current_date = datetime.datetime.now()
        async with asyncpg.create_pool(database=os.getenv("DATA"),
                                       user=os.getenv("USER"),
                                       password=os.getenv("PASSWORD")) as pool:
            result = await pool.fetchrow("SELECT id, username, password, salt"
                                         " FROM pipels WHERE username = '{0}'"
                                         .format(data['username'].lower()))
            await pool.execute("UPDATE pipels SET dt_last_login = '{0}'"
                               .format(current_date))
            log_info.info(f"Функция проверила наличие пользователя"
                          f" {data['username']} в базы данных")
            return result
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def request_to_add(data: dict) -> None:
    """
    Функция предназначена для создания пользователя в базе данных.
    :param data: - данные полученные от пользователя:
    :return - функция не производит возврата данных:
    """

    current_date = datetime.datetime.now()
    async with asyncpg.create_pool(database=os.getenv("DATA"),
                                   user=os.getenv("USER"),
                                   password=os.getenv("PASSWORD")) as pool:
        await pool.execute("INSERT INTO pipels(username, password, salt,"
                           " dt_created, dt_updated, dt_last_login) VALUES"
                           "  ('{0}', '{1}', '{2}', (TIMESTAMP '{3}'),  "
                           "(TIMESTAMP '{4}'), (TIMESTAMP '{5}'))"
                           .format(data['username'].lower(),
                                   data['password']['newkey'],
                                   data['password']['salt'],
                                   current_date,
                                   current_date,
                                   current_date))



async def registration(data: dict) -> dict:
    """
    Функция предназначена для проверки наличия пользователя в базе данных,
    а так же его регистрации при необходимости.
    При регистрации происходит проверка логина на наличие символов,
    и уникальность логина пользователя.
    Так же проверяется пароль на
    :param data: - словарь полученный от post запроса для работы:
    :return:
    """
    try:
        user_data = await withdrawal_request(data)
        if user_data:
            if user_data['username'] or user_data['username'] == data['username']:
                log_info.info(f"Пользователь {data['username']} уже"
                              f" есть в базе данных")
                return {'status': 403, 'message': 'The user is in the'
                                                  ' database'}
        else:
            if data['username'].isalpha() and data['password'].isalnum():
                salt = os.urandom(32)
                newkey = hashlib.pbkdf2_hmac(
                    'sha256',
                    data['password'].encode('utf-8'),
                    salt,
                    100000
                )
                decode_salt = codecs.decode(salt, 'CP866')
                decode_new_key = codecs.decode(newkey, 'CP866')

                data['password'] = {"salt": decode_salt,
                                    "newkey": decode_new_key}
                await request_to_add(data)
                log_info.info(f"Пользователь {data['username']} добавлен"
                              f" в базу")
                return {'status': 200, 'message': 'The user has been added'
                                                  ' to the database'}
            else:
                log_info.info(f"Ошибка стандартов логина/пароля у"
                              f"  {data['username']}")
                return {'status': 403, 'message': 'Login or password does'
                                                  ' not meet the standard'}
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def authorization(data: dict) -> dict:
    """
    Функуия проверяет уникальный логин пользователя, сообщает если
    пользователя нет в базе данных. При положительной проверке логина
    происходит проверка пароля и вход в систему либо отклонение входа
    :param data: данные от пользователя на вход в систему:
    :return: возвращает данные о свормированном пользователе в базе
    """
    try:
        user_data = await withdrawal_request(data)
        if user_data:
            encode_salt = codecs.encode(user_data['salt'], 'CP866')
            encode_new_key = codecs.encode(user_data['password'], 'CP866')

            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                data['password'].encode('utf-8'),
                encode_salt,
                100000
            )

            if new_key == encode_new_key:
                log_info.info(f"Функция разрешила вход пользователя"
                              f" {data['username']}")
                return {'id': user_data['id'],
                        'username': user_data['username']}
            else:

                log_info.info(f"Функция запрелита вход пользователя"
                              f" {data['username']} пароль"
                              " не верн")
                return {'status': 403, 'message': 'The password is incorrect'
                                                  ' try again'}

        else:
            log_info.info(f"Функция не обнаружила пользователя"
                          f" {data['username']} базе"
                          " данных, в доступе отказано")
            return {'status': 403, 'message': 'The user does not exist in'
                                              ' the database'}
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def entrance_control(data: dict) -> str:
    """
    функция генерирует токен для пользователя и возвращает
    его при успешном входе
    :param data: словарь данных о пользователе из базы данных
    :return: возарацает готовый токен
    """
    try:
        tokens = jwt.encode(payload=data, key=os.getenv("SIKRET"))
        log_info.info(f"Функция сформировала токен для пользователя:"
                      f" {data['username']}")
        return tokens
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)
