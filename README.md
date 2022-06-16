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
  "message": "The user has been added  to the database"
}
 ```

`False`

```json
{
  "status": 403,
  "message": "The user is in the database"
}
 ```
```json
{
  "status": 403,
  "message": "Login or password does  not meet the standard"
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
  "message": "The password is incorrect try again"
}
 ```
```json
{
  "status": 403,
  "message": "The user does not exist in the database"
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
  "message": "The image is saved in the  database"
}
 ```
```json
{
  "status": 200,
  "message": "The image has been changed to JPEG format and saved in the database"
}
 ```


`False`

```json
{
  "status": 423,
  "message": "The user token is not  active"
}
 ```



    `GET` `/:id` `Autorization Bearer TOKEN`
     Request body (JSON):
        http://0.0.0.0:8080/{id}

         где:  {id} - это id изображения в базе данных.

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
  "message": "You do not have access  to this image"
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
