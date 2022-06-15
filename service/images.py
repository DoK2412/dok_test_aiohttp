import asyncpg
import datetime
import os


from PIL import Image
from main import log_error, log_info


async def db_save_img(path: str, user: dict) -> None:
    """
    Функция получает путь к месту хранения файла и сохраняет его в базе данных
    :param path: - путь к месту хранения файла
    :return: - возврат не производится
    """
    try:
        current_date = datetime.datetime.now()
        async with asyncpg.create_pool(database=os.getenv("DATA"),
                                       user=os.getenv("USER"),
                                       password=os.getenv("PASSWORD")) as pool:

            await pool.fetchrow("INSERT INTO images (user_id, slug, dt_created, dt_updated,"
                                " is_delete) VALUES ('{0}', '{1}', '{2}', '{3}', 'True')"
                                .format(user['id'], path, current_date, current_date))
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)

async def image_search(img_id: int, user: int) -> str:
    """
    Функция служит для поиска изображения в базе данных и вывода
    находжения его пути.
    :param img_id: - id изображения в базе данных для поиска
    :return: - путь к месту хланения файла
    """
    try:
        async with asyncpg.create_pool(database=os.getenv("DATA"),
                                       user=os.getenv("USER"),
                                       password=os.getenv("PASSWORD")) as pool:
            path = await pool.fetchrow("SELECT slug FROM images WHERE "
                                       "id = '{0}' and user_id = '{1}' "
                                       .format(img_id, user))
        log_info.info(f"Функция вернула изображение из базы")
        return path

    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)

async def save_images(imege, user: dict) -> dict:
    """
    Функция предназначена на получения изображения, первочной проверки формата
    сохранения изображения на сервере и сохранения пути к изображению
    в базе данных.
    Так же функция проверяет наличие параметров необходимых для изменения
    изображения и производит ее компрессию.
    :param imege: - тело полученное из запроса
    :return: - возврат данных при успешном сохранении
    """
    try:
        filename = imege['img'].filename
        img_file = imege['img'].file

        original_image = Image.open(img_file)

        if imege.get('x') and imege.get('y') and imege.get('quality'):

            resized_image = original_image.resize((int(imege.get('x')),
                                                   int(imege.get('y'))),
                                                  Image.ANTIALIAS)
        else:
            resized_image = original_image

        if filename.endswith('.jpeg'):
            if imege.get('quality'):
                resized_image.save(filename, optimize=True,
                                   quality=int(imege.get('quality')))
            else:
                resized_image.save(filename)
            file_path = os.path.relpath(filename)
            await db_save_img(file_path, user)
            log_info.info(f"Пользователь {user['username']} добавил"
                          f" изобрадение в базу")
            return {'status': 200, 'message': 'Изображение сохранено '
                                              'в базе данных'}
        else:
            new_file = filename.split('.')[0] + '.jpeg'
            if imege.get('quality'):
                resized_image.save(new_file, optimize=True,
                                   quality=int(imege.get('quality')))
            else:
                resized_image.save(new_file)
            file_path = os.path.relpath(new_file)
            await db_save_img(file_path, user)
            log_info.info(f"Пользователь {user['username']} добавил"
                          f" измененное изобрадение в базу")
            return {'status': 200, 'message': 'Изображение изменено в формат '
                                              'JPEG и сохранено в базе'
                                              ' данных'}
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def image_output(data: dict, user: dict) -> str | dict[str, str | int]:
    """
    Функция предназначена для проверки наличия необходимого изображения в базе
    и выводе его пользователю
    :param data: - содержит данные необходимого изображения
    :return: - возвращает данные об изображении, а в случае если его нет
               возвращиет словарь с ответом о отсутствии изображения
    """
    try:
        image_path = await image_search(data['id_img'], user['id'])
        if image_path:
            log_info.info(f"пользователю {user['username']} "
                          f"отправлено изобрадение")
            return image_path['slug']
        else:
            log_info.info(f"пользователю {user['username']} отказано"
                          f" в доступе к изображению")
            return {'status': 403, 'message': 'У Вас не доступа'
                                              ' к данному изображению'}
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)
