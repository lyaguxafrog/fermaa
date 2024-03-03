# API-документация 

Общий API url:
```http
api.isg.moscow/api
```

## /api/user

### /api/user/create_user

### API-запрос для создания нового пользователя.

Эндпоинт:
`/api/user/create_user`

Метод: `POST`

 Ожидаемые параметры в формате JSON:
    
 - "phone": Номер телефона пользователя (строка, обязательно)
 - "password": Пароль пользователя (строка, обязательно)
 - "role": Роль пользователя (строка, обязательно)

    Коды состояния:

    - 201: Пользователь успешно создан
    
    - 400: Ошибка в запросе, возможные причины:
      - Некорректные или отсутствующие параметры
      - Неверный формат номера телефона
      - Ошибка валидации пароля
      - Прочие ошибки при создании пользователя

Пример API запроса:
```bash
    curl -X POST -H "Content-Type: application/json" -d '{
        "phone":"+7123456789",
        "password":"pAssword123",
        "role":"user"
    }' -L http://localhost:5000/api/user/create_user

```

Пример успешного ответа (код состояния 201):   
```json
    {
        "message": "User created"
    }
```

Пример ответа с ошибкой (код состояния 400):

```json
{
    "error": "Неверный формат номера телефона"
}
```

## /api/user/get_user/

### API-запрос для получения информации о пользователе по его ID.

Эндпоинт:
`/api/user/get_user/<user_ud:int>`

Метод: `GET`

Параметры:

- user_id: ID пользователя (целое число, обязательно)

Коды состояния:

- 200: Запрос выполнен успешно
- 404: Пользователь с указанным ID не найден

Пример API запроса:
```bash
curl -H "Accept: application/json" http://localhost:5000/api/user/get_user/1
```

Пример успешного ответа (код состояния 200):

```json
{
    "id": 1,
    "phone": "+7123456789",
    "email": "user@example.com",
    "name": "John Doe",
    "description": "A user",
    "email_verified": true,
    "is_banned": false,
    "role": "user"
}
```

Пример ответа с ошибкой (код состояния 404):
```json
{
    "error": "User not found"
}
```

### /api/user/update_user

API-запрос для обновления данных о пользователе по его ID.

Эндпоинт:
`/api/user/update_user/<user_id:int>`

Метод: `PUT`

Параметры:

- user_id: ID пользователя (целое число, обязательно)

Тело запроса (в формате JSON):

- Любые поля пользователя, которые необходимо обновить

Коды состояния:

- 200: Данные пользователя успешно обновлены
- 404: Пользователь с указанным ID не найден

Пример API запроса:

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "name": "New Name",
    "gender": "Female",
    "bday": "1990-01-01",
    "description": "Updated description"
}' http://localhost:5000/api/user/update_user/1
```

Пример успешного ответа (код состояния 200):

```json
{
    "message": "User updated successfully",
    "user": {
        "id": 1,
        "phone": "+7123456789",
        "email": "user@example.com",
        "name": "New Name",
        "gender": "Female",
        "bday": "1990-01-01",
        "description": "Updated description",
        "email_verified": true,
        "is_banned": false,
        "role": "user"
    }
}
```

Пример ответа с ошибкой (код состояния 404):

```json
{
    "error": "User not found"
}
```

### /api/user/delete_user

API-запрос для удаления пользователя по его ID.

Эндпоинт:
`/api/user/delete_user/<user_id:int>

Метод: `DELETE`

Параметры:

- user_id: ID пользователя (целое число, обязательно)

Коды состояния:

- 200: Пользователь успешно удален
- 404: Пользователь с указанным ID не найден

Пример API запроса:

```bash
curl -X DELETE http://localhost:5000/api/user/delete_user/1
```

Пример успешного ответа (код состояния 200):

```json
{
    "message": "User with ID 1 deleted successfully"
}
```

Пример ответа с ошибкой (код состояния 404):

```json
{
    "error": "User not found"
}
```
### /api/user/login

API-запрос для аутентификации пользователя.

Эндпоинт:
`/api/user/login

Метод: `POST`

Параметры:

- phone: Телефон пользователя
- password: Пароль

Возвращает JSON-ответ с результатом аутентификации.

Пример запроса:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "phone":"+7123456789",
    "password":"pAssword123"
}' http://localhost:5000/api/user/login
```

Коды состояния:

- 200: Аутентификация успешна
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 401: Аутентификация не удалась

Пример успешного ответа (код состояния 200):
```json
{
    "access_token": "<JWT_TOKEN>"
}
```

Пример ответа с ошибкой (код состояния 400 или 401):
```json
{
    "error": "Login failed"  # или "User banned", "User deleted", "Missing phone or password"
}
```

-----

## /api/post

### /api/post/create_post

API-запрос для создания нового поста.

Эндпоинт:
`/api/post/create_post`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID пользователя, от имени которого создается пост (целое число, обязательно)
- "post_text": Текст поста (строка, обязательно)

Необязательный параметр:

- "file_path": Путь к файлу, прикрепленному к посту (строка)

Заголовки:

- "Authorization: Bearer <jwt_token>"

Коды состояния:

- 200: Пост успешно создан
- 400: Ошибка в запросе, возможные причины:
- Некорректные или отсутствующие параметры
- Недостаточно прав для создания поста от имени указанного пользователя
- Пользователь заблокирован (ban)
- Пользователь удален
- Неверный формат файла (если указан file_path)
- 403: Отказ в доступе, если текущий пользователь не имеет права создавать посты от имени указанного пользователя
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "post_text": "Новый пост"
}' -L http://localhost:5000/api/post/create_post
```

Пример успешного ответа (код состояния 200):

```json
{
    "message": "Post created successfully"
}
```

Пример ответа с ошибкой (код состояния 400, 403 или 500):

```json
{
    "error": "Invalid request format"  # или "User banned", "User deleted", "Access forbidden", "An error occurred"
}
```

### /api/post/set_like

API-запрос для установки лайка к посту.

Эндпоинт:
`/api/post/set_like

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID пользователя, который ставит лайк (целое число, обязательно)
- "post_id": ID поста, к которому ставится лайк (целое число, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 200: Лайк успешно установлен
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к установке лайка
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права устанавливать лайки от имени указанного пользователя
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "post_id": 123
}' -L http://localhost:5000/api/post/set_like
```

Пример успешного ответа (код состояния 200):
```json
{
    "message": "Like set successfully"
}
```

Пример ответа с ошибкой (код состояния 400, 403 или 500):
```json
{
    "error": "Invalid request format"  # или "You are not allowed to access set like", "User banned", "User deleted", "An error occurred"
}
```

### /api/post/remove_like

API-запрос для удаления лайка у поста.

Эндпоинт: 
`/api/post/remove_like`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID пользователя, который удаляет лайк (целое число, обязательно)
- "post_id": ID поста, у которого удаляется лайк (целое число, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 200: Лайк успешно удален
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к удалению лайка
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права удалять лайки от имени указанного пользователя
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "post_id": 123
}' -L http://localhost:5000/api/post/remove_like
```bash

Пример успешного ответа (код состояния 200):
```json
{
    "message": "Like removed successfully"
}
```

Пример ответа с ошибкой (код состояния 400, 403 или 500):
```json
{
    "error": "Invalid request format"  # или "You are not allowed to access remove like", "User banned", "User deleted", "An error occurred"
}
```

### /api/post/post_comment

API-запрос для добавления комментария к посту.

Эндпоинт:
`/api/post/post_comment`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID пользователя, оставляющего комментарий (целое число, обязательно)
- "post_id": ID поста, к которому оставляется комментарий (целое число, обязательно)
- "comment_text": Текст комментария (строка, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 200: Комментарий успешно добавлен
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к оставлению комментариев
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права оставлять комментарии от имени указанного пользователя
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "post_id": 123,
    "comment_text": "This is a comment."
}' -L http://localhost:5000/api/post/post_comment
```

Пример успешного ответа (код состояния 200):
```json
{
    "message": "Comment posted successfully"
}
```

Пример ответа с ошибкой (код состояния 400, 403 или 500):
```json
{
    "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "An error occurred"
}
```

### /api/post/delete_comment

API-запрос для удаления комментария к посту.

Эндпоинт:
`/api/post/delete_comment`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID пользователя, удаляющего комментарий (целое число, обязательно)
- "post_id": ID поста, к которому относится комментарий (целое число, обязательно)
- "comment_id": ID комментария, который удаляется (целое число, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 200: Комментарий успешно удален
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к удалению комментария
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права удалять комментарии от имени указанного пользователя
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "post_id": 123,
    "comment_id": 456
}' -L http://localhost:5000/api/post/delete_comment
```

Пример успешного ответа (код состояния 200):
```json
{
    "success": true,
    "message": "Comment deleted successfully"
}
```

Пример ответа с ошибкой (код состояния 400, 403 или 500):
```json
{
    "success": false,
    "message": "Permission denied or comment not found"  # или "Invalid request format", "You are not allowed to access send message", "User banned", "User deleted", "An error occurred"
}
```

## /api/friends

### /api/friends/sub_to

API-запрос для подписки пользователя на другого пользователя.

Эндпоинт: 
`/api/friends/sub_to`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID текущего пользователя (целое число, обязательно)
- "sub_to": ID пользователя, на которого подписываются (целое число, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 201: Подписка успешно создана
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к созданию подписки
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права подписываться от имени указанного пользователя
- 406: Подписка уже существует (пользователь уже подписан)
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "sub_to": 2
}' -L http://localhost:5000/api/friends/sub_to
```

Пример успешного ответа (код состояния 201):
```json
{
    "message": "User 1 sub to 2"
}
```

Пример ответа с ошибкой (код состояния 400, 403, 406 или 500):
```json
{
    "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "Error: user is already subscribed", "An error occurred"
}
```
###  /api/friends/unsub_to

API-запрос для отмены подписки пользователя на другого пользователя.

Эндпоинт: 
` /api/friends/unsub_to`

Метод: `POST`

Обязательные параметры в формате JSON:

- "user_id": ID текущего пользователя (целое число, обязательно)
- "unsub_id": ID пользователя, от которого отписываются (целое число, обязательно)

Заголовки:

- "Authorization: Bearer `<jwt_token>`"

Коды состояния:

- 201: Отписка успешно выполнена
- 400: Ошибка в запросе, возможные причины:
    - Некорректные или отсутствующие параметры
    - Пользователь не имеет доступа к отмене подписки
    - Пользователь заблокирован (ban)
    - Пользователь удален
- 403: Отказ в доступе, если текущий пользователь не имеет права отписываться от имени указанного пользователя
- 406: Отмена подписки не выполнена (пользователи не были подписаны друг на друга)
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
    "user_id": 1,
    "unsub_id": 2
}' -L http://localhost:5000/api/friends/unsub_to
```

Пример успешного ответа (код состояния 201):
```json
{
    "message": "User 1 unsub 2"
}
```

Пример ответа с ошибкой (код состояния 400, 403, 406 или 500):
```json
{
    "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "users are not subscribed", "An error occurred"
}
```
### /api/friends/get_followers

API-запрос для получения списка подписчиков пользователя.

Эндпоинт: 
`/api/friends/get_followers<user_id:int>`

Метод: `GET`

Обязательные параметры в URL:

- user_id: ID пользователя (целое число, обязательно)

Коды состояния:

- 200: Запрос выполнен успешно
- 400: Ошибка в запросе, возможные причины:
    - Некорректные параметры
    - Пользователь не существует или не имеет подписчиков
    - Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X GET http://localhost:5000/api/friends/get_followers/1
```

Пример успешного ответа (код состояния 200):
```json
{
    "follower_users": "1, 3, 5",
    "follower_count": "3"
}
```

Пример ответа с ошибкой (код состояния 400):
```json
{
    "error": "Invalid user ID"  # или "User does not exist" или "Internal Server Error"
}
```


-----

## /api/chat

### /api/chat/send_message

API-запрос для отправки личного сообщения.

Эндпоинт:
`/api/chat/send_message`

Метод: `POST
`
Обязательные параметры в JSON-запросе:

- sender_id: ID отправителя (целое число, обязательно)
- receiver_id: ID получателя (целое число, обязательно)
- content: Текст сообщения (строка, обязательно)

Заголовки:

- Authorization: Bearer `<jwt>`

Коды состояния:

- 201: Сообщение успешно отправлено
- 400: Ошибка в запросе, возможные причины:
    - Некорректные параметры
    - Пользователь не имеет право отправлять сообщения
- 401: Пользователь не авторизован/удален/забанен
- 403: Отправитель не имеет права отправлять сообщения
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Привет, как дела?"
}' -H "Authorization: Bearer <token>" -L http://localhost:5000/api/chat/send_message
```

Пример успешного ответа (код состояния 201):
```json
{
    "message": "Message sent"
}
```

Пример ответа с ошибкой (код состояния 400):
```json
{
    "error": "Missing required fields"  # или другие возможные ошибки
}
```
### /api/chat/history

API-запрос для получения истории чата между двумя пользователями.

Эндпоинт:
`/api/chat/history/<user_id: int>/<user_id: int>`

Метод: `GET`

Обязательные параметры:

- sender_id: ID отправителя (целое число, обязательно)
- receiver_id: ID получателя (целое число, обязательно)

Заголовки:

- Authorization: Bearer `<jwt>`

Коды состояния:

- 200: Запрос выполнен успешно, возвращает историю чата в формате JSON
- 400: Ошибка в запросе, возможные причины:
    - Некорректные параметры
    - Ошибка при получении истории чата
- 403: Пользователь не имеет право доступа к истории данного чата
- 500: Внутренняя ошибка сервера

Пример API запроса:
```bash
curl -H "Authorization: Bearer <token>" -L http://localhost:5000/api/chat/history/1/2
```

Пример успешного ответа (код состояния 200):
```json
[
    {"sender_id": 1, "receiver_id": 2, "content": "Привет, как дела?", "timestamp": "2023-12-15 12:30:45"},
    {"sender_id": 2, "receiver_id": 1, "content": "Привет! я заебался", "timestamp": "2023-12-15 12:35:22"},
    ...
]
```

Пример ответа с ошибкой (код состояния 403):
```json
{
    "error": "You are not allowed to access this chat history"
}
```
