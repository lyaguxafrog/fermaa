# # -*- coding: utf-8 -*-

# from flask import Blueprint, request
# from flask_jwt_extended import get_jwt_identity, jwt_required

# from farm.services import FriendsService, UserCheckService

# friends_api = Blueprint('friends_api', __name__)



# @friends_api.route('/sub_to', methods=['POST'])
# @jwt_required()
# def sub_to():
#     """
#     API-запрос для подписки пользователя на другого пользователя.

#     Метод: POST
#     Обязательные параметры в формате JSON:
#     - "user_id": ID текущего пользователя (целое число, обязательно)
#     - "sub_to": ID пользователя, на которого подписываются (целое число, обязательно)

#     Заголовки:
#     - "Authorization: Bearer <jwt_token>"

#     Коды состояния:
#     - 201: Подписка успешно создана
#     - 400: Ошибка в запросе, возможные причины:
#         - Некорректные или отсутствующие параметры
#         - Пользователь не имеет доступа к созданию подписки
#         - Пользователь заблокирован (ban)
#         - Пользователь удален
#     - 403: Отказ в доступе, если текущий пользователь не имеет права подписываться от имени указанного пользователя
#     - 406: Подписка уже существует (пользователь уже подписан)
#     - 500: Внутренняя ошибка сервера

#     Пример API запроса:
#     curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
#         "user_id": 1,
#         "sub_to": 2
#     }' -L http://localhost:5000/api/friends/sub_to

#     Пример успешного ответа (код состояния 201):
#     {
#         "message": "User 1 sub to 2"
#     }

#     Пример ответа с ошибкой (код состояния 400, 403, 406 или 500):
#     {
#         "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "Error: user is already subscribed", "An error occurred"
#     }
#     """

#     current_phone = get_jwt_identity()

#     data = request.get_json()

#     user_id = data['user_id']



#     user_phone = UserCheckService.phone_by_id(user_id)

#     if current_phone != user_phone:
#         return {
#         "error": "You are not allowed to access send message"
#                 }, 403

#     if UserCheckService.check_ban(user_id):
#         return {"error":"User banned"}, 403

#     if UserCheckService.check_delete(user_id):
#         return {"error":"User deleted"}, 403

#     sub_to = data['sub_to']

#     try:
#         if FriendsService.subscribe_to(user_id=user_id, sub=sub_to):
#             return {"message":f"User {user_id} sub to {sub_to}"}, 201

#         else:
#             return {"error":"Error: user is already subscribed"}, 406

#     except Exception as e:
#         return {"error":str(e)}, 400


# @friends_api.route('/unsub_to', methods=['POST'])
# @jwt_required()
# def unsub_to():
#     """
#     API-запрос для отмены подписки пользователя на другого пользователя.

#     Метод: POST
#     Обязательные параметры в формате JSON:
#     - "user_id": ID текущего пользователя (целое число, обязательно)
#     - "unsub_id": ID пользователя, от которого отписываются (целое число, обязательно)

#     Заголовки:
#     - "Authorization: Bearer <jwt_token>"

#     Коды состояния:
#     - 201: Отписка успешно выполнена
#     - 400: Ошибка в запросе, возможные причины:
#         - Некорректные или отсутствующие параметры
#         - Пользователь не имеет доступа к отмене подписки
#         - Пользователь заблокирован (ban)
#         - Пользователь удален
#     - 403: Отказ в доступе, если текущий пользователь не имеет права отписываться от имени указанного пользователя
#     - 406: Отмена подписки не выполнена (пользователи не были подписаны друг на друга)
#     - 500: Внутренняя ошибка сервера

#     Пример API запроса:
#     curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
#         "user_id": 1,
#         "unsub_id": 2
#     }' -L http://localhost:5000/api/friends/unsub_to

#     Пример успешного ответа (код состояния 201):
#     {
#         "message": "User 1 unsub 2"
#     }

#     Пример ответа с ошибкой (код состояния 400, 403, 406 или 500):
#     {
#         "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "users are not subscribed", "An error occurred"
#     }
#     """

#     current_phone = get_jwt_identity()

#     data = request.get_json()

#     user_id = data['user_id']

#     user_phone = UserCheckService.phone_by_id(user_id)

#     if current_phone != user_phone:
#         return {
#         "error": "You are not allowed to access send message"
#                 }, 403

#     if UserCheckService.check_ban(user_id):
#         return {"error":"User banned"}, 403

#     if UserCheckService.check_delete(user_id):
#         return {"error":"User deleted"}, 403

#     unsub_id = data['unsub_id']

#     try:
#         if FriendsService.unsubscribe_from(user_id=user_id, sub=unsub_id):
#             return {'message':f'User {user_id} unsub {unsub_id}'}, 201

#         else:
#             return {'error':'users are not subscribed'}, 406

#     except Exception as e:
#         return {'error':str(e)}, 400


# @friends_api.route('get_followers/<int:user_id>', methods=['GET'])
# def getfollowers(user_id: int):
#     """
#     API-запрос для получения списка подписчиков пользователя.

#     Метод: GET
#     Обязательные параметры в URL:
#     - user_id: ID пользователя (целое число, обязательно)

#     Коды состояния:
#     - 200: Запрос выполнен успешно
#     - 400: Ошибка в запросе, возможные причины:
#         - Некорректные параметры
#         - Пользователь не существует или не имеет подписчиков
#         - Внутренняя ошибка сервера

#     Пример API запроса:
#     curl -X GET http://localhost:5000/api/friends/get_followers/1

#     Пример успешного ответа (код состояния 200):
#     {
#         "follower_users": "1, 3, 5",
#         "follower_count": "3"
#     }

#     Пример ответа с ошибкой (код состояния 400):
#     {
#         "error": "Invalid user ID"  # или "User does not exist" или "Internal Server Error"
#     }
#     """

#     try:
#         (follower_users,
#          follower_count) = FriendsService.get_followers(user_id=user_id)

#         return {"follower_users":f"{follower_users}",
#                 "follower_count":f"{follower_count}"}, 200

#     except Exception as e:
#         return {"error":str(e)}, 400
