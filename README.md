    Программа написана на Python версии  3.10;
    Используется PostgreSQL версии 14.3;
    Использован фреймворк aiohttp;
    Работа с базой данных реализована через пакет asyncpg;
    Работа с изображениями реализована через пакет pillow;
    Логирование настроено через пакет logging с использованием 
        дополнительного файла создания логеров.

    Программа запускается из файла main.py, в котором происходи создание основных направлений работы 
    и подключени базы данных в фоновом режиме при запущенном изображении. 
    Handler импортирован внутрь основонесущей функции make_app() для избежания ошибки цикличного импорта
    при подключении логеров в файле handler.py.


    `POST` `/registration`
     Request body (JSON):
        `{"user_name":"name", "password":"pass"}`
    
        где: `user_name` - это  имя предполагаемого пользователя, 
             `password` - пароль для регистрации пользователя.
    
Response:

`True`

```json
{
  "status": 200,
  "message": "Пользователь добавлен в базу данных"
}
 ```

`False`

```json
{
  "status": 403,
  "message": "Пользователm есть в базе данных"
}
 ```
```json
{
  "status": 403,
  "message": "Логин или пароль не соответсвует стандарту"
}
 ```



    `POST` `/auth`:
     Request body (JSON):
        `{"user_name":"name", "password":"pass"}`
    
        где: `user_name` - это  имя существующего пользователя, 
             `password` - пароль для авторизации пользователя.

Response:

`True`

```json
{
  'id': user_data['id'],
  'username': user_data['username']
}
 ```

`False`

```json
{
  "status": 403,
  "message": "Пароль не верен повторите попытку"
}
 ```
```json
{
  "status": 403,
  "message": "Пользователя не сушествует в базе данных"
}
 ```


    `POST` `/img`:
     Request body (JSON):
        `{"img":"тело изображения", "x":"ширина", "y":"высота", "quality":"качество"}`

         где:   `img` - это  тело акпкданного файла, 
                `x` - ширина для компрессию изображения (не обязательный параметр),
                `y` - высота для компрессию изображения (не обязательный параметр),
                `quality` - качество для компрессию изображения (не обязательный параметр).

Response:

`True`

```json
{
  "status": 200,
  "message": "Изображение сохранено в базе данных"
}
 ```
```json
{
  "status": 200,
  "message": "Изображение изменено в формат JPEG и сохранено в базе данных"
}
 ```


`False`

```json
{
  "status": 423,
  "message": "Токен пользователя не активен"
}
 ```



    `GET` `/:id` `Autorization Bearer TOKEN`
     Request body (JSON):
        `{"id_img": **}`

         где:   `id_img` - это id изображения в базе данных.

Response:

`True`

```FileResponse
{
  `вывод изображения пользователю`
}
 ```

`False`

```json
{
  "status": 423,
  "message": "У Вас не доступа к данному изображению"
}
 ```



        `GET` `/info`

Response:

`True`

```FileResponse
{
  `вывод лога инфо пользователю из файла info.logg`
}
 ```


       `GET` `/error`

Response:

`True`

```FileResponse
{
  `вывод лога ошибок пользователю из файла error.logg`
}
 ```
