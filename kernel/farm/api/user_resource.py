# -*- coding: utf-8 -*-

from flask import Blueprint, Response, jsonify, request

from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity)
from datetime import datetime, timedelta

from flask_migrate import current


from farm.services import UserService, CheckService
from sqlalchemy.exc import IntegrityError
from farm import db

user_api = Blueprint("user_api", __name__)


class InvalidPasswordException(Exception):
    pass

@user_api.route('/create_user', methods=['POST'])
def create_user_api():
    """
    API-запрос для создания нового пользователя.

    Метод: POST
    Ожидаемые параметры в формате JSON:
    - "phone": Номер телефона пользователя (строка, обязательно)
    - "email": Почта пользователя (строка, обязательно)
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
    curl -X POST -H "Content-Type: application/json" -d '{
        "phone":"+7123456789",
        "email":"test@mail.test",
        "name":"Text",
        "password":"pAssword123",
        "role":"user"
    }' -L http://localhost:5000/api/user/create_user

    Пример успешного ответа (код состояния 201):
    {
        "message": "User created",
        "user_id": 123
    }

    Пример ответа с ошибкой (код состояния 400):
    {
        "error": "Неверный формат номера телефона"
    }
    """

    data = request.get_json()

    phone = data.get('phone')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    role = data.get('role')

    try:
        user_id = UserService.new_user(phone=phone, email=email,
                                       password=password, name=name,
                                       role=role)
        return {"message": "User created", "user_id": user_id}, 201
    except ValueError as ve:
        return {"error": f"Validation Error: {str(ve)}"}, 400
    except InvalidPasswordException as ipe:
        return {"error": f"Invalid Password: {str(ipe)}"}, 400
    except IntegrityError as ie:
        db.session.rollback()  # Rollback the transaction to avoid leaving the database in a partially committed state
        return {"error": f"Email already exists: {str(ie)}"}, 400
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}, 400


# coded by Adrian Makridenko
# @lyaguxafrog


@user_api.route('/get_user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id: int) -> Response:
    """
    API-запрос для получения информации о пользователе по его ID.

    Метод: GET

    Параметры:
    - user_id: ID пользователя (целое число, обязательно)

    Заголовок JWT (пример):
    - Authorization: Bearer <token>

    Коды состояния:
    - 200: Запрос выполнен успешно
    - 404: Пользователь с указанным ID не найден

    Пример API запроса:
    curl -H "Accept: application/json" -H "Authorization: Bearer <token>" http://localhost:5000/api/user/get_user/1

    Пример успешного ответа (код состояния 200):
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

    Пример ответа с ошибкой (код состояния 404):
    {
        "error": "User not found"
    }
    """
    current_phone = get_jwt_identity()

    if current_phone == CheckService.get_phone_by_user_id(user_id):
        return UserService.get_user_info(user_id=user_id, private=True)

    else:
        return UserService.get_user_info(user_id=user_id, private=False)


@user_api.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_api(user_id: int):
    """
    API-запрос для обновления данных о пользователе по его ID.

    Метод: PUT

    Параметры:
    - user_id: ID пользователя (целое число, обязательно)

    Тело запроса (в формате JSON):
    - Любые поля пользователя, которые необходимо обновить

    Заголовок JWT (пример):
    - Authorization: Bearer <token>

    Коды состояния:
    - 200: Данные пользователя успешно обновлены
    - 404: Пользователь с указанным ID не найден

    Пример API запроса:
    curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
        "name": "New Name",
        "gender": "Female",
        "bday": "1990-01-01",
        "description": "Updated description"
    }' http://localhost:5000/api/user/update_user/1

    Пример успешного ответа (код состояния 200):
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

    Пример ответа с ошибкой (код состояния 404):
    {
        "error": "User not found"
    }
    """
    current_user_id = get_jwt_identity()

    # Проверяем, что пользователь существует
    if not CheckService.user_exists(user_id=user_id):
        return jsonify({"error": "User not found"}), 404

    # Проверяем валидность JWT
    if current_user_id != user_id:
        return jsonify({"error": "Invalid JWT"}), 401

    # Получаем данные для обновления из тела запроса
    data = request.get_json()

    # Вызываем функцию update_user
    updated_user = UserService.update_user(user_id, data)

    if updated_user:
        # Возвращаем обновленные данные
        return jsonify({"message": "User updated successfully", "user": updated_user}), 200
    else:
        # Возвращаем сообщение об ошибке, если что-то пошло не так
        return jsonify({"error": "Failed to update user"}), 500


# NOTE: пернести в admin api
# @user_api.route('/delete_user/<int:user_id>', methods=['DELETE'])
# def delete_user_api(user_id: int):
#     """
#     API-запрос для удаления пользователя по его ID.

#     Метод: DELETE

#     Параметры:
#     - user_id: ID пользователя (целое число, обязательно)

#     Коды состояния:
#     - 200: Пользователь успешно удален
#     - 404: Пользователь с указанным ID не найден

#     Пример API запроса:
#     curl -X DELETE http://localhost:5000/api/user/delete_user/1

#     Пример успешного ответа (код состояния 200):
#     {
#         "message": "User with ID 1 deleted successfully"
#     }

#     Пример ответа с ошибкой (код состояния 404):
#     {
#         "error": "User not found"
#     }
#     """

#     result = UserService.delete_user(user_id)

#     return result


@user_api.route('/login', methods=['POST'])
def login_api():
    """
    API-запрос для аутентификации пользователя.

    Метод: POST
    Ожидаемые параметры в формате JSON: phone и password.

    Возвращает JSON-ответ с результатом аутентификации.

    Пример запроса:
    curl -X POST -H "Content-Type: application/json" -d '{
        "phone":"+7123456789",
        "password":"pAssword123"
    }' http://localhost:5000/api/user/login

    Коды состояния:
    - 200: Аутентификация успешна
    - 400: Ошибка в запросе, возможные причины:
        - Некорректные или отсутствующие параметры
        - Пользователь заблокирован (ban)
        - Пользователь удален
    - 401: Аутентификация не удалась

    Пример успешного ответа (код состояния 200):
    {
        "access_token": "<JWT_TOKEN>"
    }

    Пример ответа с ошибкой (код состояния 400 или 401):
    {
        "error": "Login failed"  # или "User banned", "User deleted", "Missing phone or password"
    }
    """

    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')


    expires_delta = timedelta(days=365)


    if not phone or not password:
        return jsonify({"error": "Missing phone or password"}), 400


    if UserService.login(phone, password):
        # Аутентификация успешна

        access_token = create_access_token(identity=phone,
                                           expires_delta=expires_delta)
        return jsonify({"access_token": access_token}), 200
    else:
        # Аутентификация не удалась
        return jsonify({"error": "Login failed"}, 401)
