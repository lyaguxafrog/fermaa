# -*- coding: utf-8 -*-


from typing import Any
from flask import Response, jsonify

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from farm import db
from farm.models import UsersModel


def user_exists(phone: str) -> bool:
    """Check if a user with the given phone number already exists."""
    return UsersModel.query.filter_by(phone=phone).first() is not None

class InvalidPasswordException(Exception):
    """ Класс для райза ошибок """
    pass

def is_good_password(password: str) -> bool:
    """
    Функция проверки пароля

    :param password: Пароль пользователя

    :return: bool значение
    """

    if len(password) < 8:
        return False

    if not any(char.isalpha() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    return True



class UserService():
    """
    Сервис взаимодействия с пользователем


    * new_user - создание пользователя
    * get_user_info - информация о пользователе
    * update_user - обновление пользователя
    * delete_user - удаление пользователя
    * login - логин пользователя

    """

    @staticmethod
    def new_user(phone: str, name: str, email: str,
                 password: str, role: str) -> int:
        """
        Функция создания нового пользователя

        :param phone: Номер телефона пользователя в виде `+7123456789`
        :param email: Email пользователя
        :param name: Имя пользователя
        :param password: Пароль пользователя(пароль должен содержать 8 символов
        одну заглавну и однустрочную)
        :param role: Роль пользователя `super-admin`,
        `admin-farm`, `admin-3d`, `user`

        :return: id пользователя
        """

        if not is_good_password(password):
            raise InvalidPasswordException("Invalid password")

        if user_exists(phone):
            raise ValueError("User with this phone number already exists")

        # Хэширование пароля перед сохранением в базу данных
        hashed_password = generate_password_hash(password, method='sha256')

        # Создание пользователя
        user = UsersModel(
            phone=phone,
            email=email,
            name=name,
            password=hashed_password,
            role=role,
        )

        # Добавление пользователя в сессию
        db.session.add(user)

        # Фиксация изменений в базе данных
        db.session.commit()

        # Возвращение id нового пользователя
        return user.id

# coded by Adrian Makridenko
# @lyaguxafrog

    @staticmethod
    def get_user_info(user_id: int, private: bool) -> Response:
        """
        Функция получения всей информации о пользователе

        :param user_id: ID пользователя
        :param private: Bool значение на вывод всей информации или только
        публичной

        :return: Информация в виде JSON
        """

        user = UsersModel.query.get(user_id)

        if user is not None:

            if private:
                user_info = {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "subs": user.sub_level,
                "achievements": user.achievements,
                "icoins": user.icoins,
                "name": user.name,
                "descriprion": user.description,
                "username": user.username,
                "gender": user.gender,
                "bday": user.bday,
                "friends": user.friends,
                "followers": user.followers,
                "follwing": user.following,
                "posts": user.user_posts,
                "chats": user.chats,
                "farms": user.farms,
                "3Dmodels": user._3d_models,
                "3d_gifts": user.gifts_3d,
                "seeds": user.seeds,
                "farm_gifts": user.farm_gifts,
                "reviews": user.reviews

            }

            else:
                user_info = {
                    "id": user.id,
                    "role": user.role,
                    "subs": user.sub_level,
                    "achievements": user.achievements,
                    "name": user.name,
                    "descriprion": user.description,
                    "username": user.username,
                    "gender": user.gender,
                    "friends": user.friends,
                    "followers": user.followers,
                    "follwing": user.following,
                    "posts": user.user_posts,
                }

            return jsonify(user_info)
        else:
            return jsonify({"error": "User not found"}), 404  # type: ignore


    @staticmethod
    def update_user(user_id, data) -> Any:
        """
        Функция обновления данных о пользователе

        :param user_id: ID пользователя
        :param data: Словарь с данными для обновления
        :return: Обновленная информация о пользователе или сообщение об ошибке
        """

        # Проверяем, существует ли пользователь с указанным ID
        user = UsersModel.query.get(user_id)

        if not user:
            # Обработка случая, если пользователь с заданным user_id не найден
            return None

        # Обновление всех полей модели на основе данных из запроса
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        # Если в данных есть поле 'bday', преобразовать его в объект DateTime
        if 'bday' in data and data['bday']:
            user.bday = datetime.strptime(data['bday'], '%Y-%m-%d')

        # Сохранение изменений в базе данных
        db.session.commit()

        return user


    @staticmethod
    def delete_user(user_id: int):
        """
        Функция удаления пользователя по ID

        :param user_id: ID пользователя
        """

        try:
            user = UsersModel.query.get(user_id)

            if user:
                # Устанавливаем is_deleted в True
                user.is_deleted = True

                # Сохраняем изменения в базе данных
                db.session.commit()

                return jsonify({
                    "message": f"User with ID {user_id} deleted successfully"
                    }), 200
            else:
                return jsonify({"error": "User not found"}), 404

        except Exception as e:
            # Обработка ошибок
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def login(phone: str, password: str) -> bool:
        """
        Функция аутентификации пользователя.

        :param phone: Номер телефона пользователя.
        :param password: Введенный пароль.

        :return: True, если аутентификация успешна, False в противном случае.
        """

        # Находим пользователя в базе данных по номеру телефона
        user = UsersModel.query.filter_by(phone=phone).first()

        # Если пользователь не найден, возвращаем False
        if not user:
            return False

        # Проверяем хэшированный пароль
        if check_password_hash(user.password, password):
            return True
        else:
            return False

    @staticmethod
    def ban_user(user_id: int) -> bool:
        """
        Функция бана пользователя

        :param user_id: ID пользователя

        :return: True - забанен, False - пользователь не найден
        """


        user = UsersModel.query.get(user_id)


        if not user:
            return False

        user.is_banned = True


        db.session.commit()

        return True
