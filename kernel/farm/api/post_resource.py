# -*- coding: utf-8 -*-

from symbol import return_stmt
from flask import Blueprint, current_app, jsonify, request

from werkzeug.utils import secure_filename


from flask_jwt_extended import jwt_required, get_jwt_identity

from farm.services import PostsService, CheckService
from farm.models import Posts
from datetime import datetime

post_api = Blueprint("post_api", __name__)



@post_api.route('/create_post', methods=['POST'])
@jwt_required()
def create_post_api():

    data = request.get_json()

    current_phone = get_jwt_identity()

    owner_id = data['owner_id']
    text = data['text']
    picture_data = request.files.get('picture_data')

    if current_phone != CheckService.get_phone_by_user_id(owner_id):
        return jsonify({"error": "Invalid token"}), 401

    if CheckService.check_ban(owner_id):
        return jsonify({"error":"User banned"}), 423

    try:
        post_id = PostsService.create_post(owner_id, text,
                            picture_data.read() if picture_data else None)

        return jsonify({'post_id': post_id}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_api.route('/get_post/<int:user_id>/<int:post_id>/', methods=['GET'])
@jwt_required()
def get_post_api(post_id, user_id):
    post = PostsService.get_post(post_id)

    current_phone = get_jwt_identity()

    if current_phone != CheckService.get_phone_by_user_id(user_id):
        return jsonify({"error": "Invalid token"}), 401

    if CheckService.check_ban(user_id):
        return jsonify({"error":"User banned"}), 423

    if post:
        return jsonify({
            'id': post.id,
            'owner_id': post.owner_id,
            'user': {
                'id': post.user.id,
                'username': post.user.username
            },
            'timestamp': post.timestamp,
            'post_text': post.post_text,
            'picture': post.picture,
            'views': post.views,
            'likes': post.likes,
            'comments': post.comments
        })
    else:
        return jsonify({'error': 'Post not found'}), 404

@post_api.route('/get_posts/', methods=['GET'])
def get_posts():
    try:
        # Получаем параметры запроса
        page = int(request.args.get('page', 1))
        user_id = int(request.args.get('user_id', 0))

        # Количество постов на одной странице
        posts_per_page = 10

        # Вычисляем смещение для выборки постов
        offset = (page - 1) * posts_per_page

        # Запрос в базу данных для получения постов
        if user_id:
            # Если указан user_id, получаем посты только для этого пользователя
            posts = Posts.query.filter_by(owner_id=user_id).offset(offset).limit(posts_per_page).all()
        else:
            # В противном случае получаем все посты
            posts = Posts.query.offset(offset).limit(posts_per_page).all()

        # Преобразуем результат в JSON
        result = []
        for post in posts:
            result.append({
                'id': post.id,
                'owner_id': post.owner_id,
                'timestamp': str(post.timestamp),
                'post_text': post.post_text,
                'picture': post.picture,
                'views': post.views,
                'likes': post.likes,
                'comments': post.comments
            })

        return jsonify({"posts": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@post_api.route('/set_like', methods=['POST'])
@jwt_required()
def set_like_api():
    """
    API-запрос для установки лайка к посту.

    Метод: POST
    Обязательные параметры в формате JSON:
    - "user_id": ID пользователя, который ставит лайк (целое число, обязательно)
    - "post_id": ID поста, к которому ставится лайк (целое число, обязательно)

    Заголовки:
    - "Authorization: Bearer <jwt_token>"

    Коды состояния:
    - 200: Лайк успешно установлен
    - 400: Ошибка в запросе, возможные причины:
      - Некорректные или отсутствующие параметры
      - Пользователь не имеет доступа к установке лайка
      - Пользователь заблокирован (ban)
      - Пользователь удален
    - 403: Отказ в доступе, если текущий пользователь не
        имеет права устанавливать лайки от имени указанного пользователя
    - 500: Внутренняя ошибка сервера

    Пример API запроса:
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
        "user_id": 1,
        "post_id": 123
    }' -L http://localhost:5000/api/post/set_like

    Пример успешного ответа (код состояния 200):
    {
        "message": "Like set successfully"
    }

    Пример ответа с ошибкой (код состояния 400, 403 или 500):
    {
        "error": "Invalid request format"  # или "You are not allowed to access set like", "User banned", "User deleted", "An error occurred"
    }
    """
    try:

        current_user_phone = get_jwt_identity()


        data = request.get_json()

        user_id = data['user_id']
        post_id = data['post_id']

        user_phone = CheckService.get_phone_by_user_id(user_id)

        if current_user_phone != user_phone:
            return {"error":"You are not allowed to access set like"}, 403

        if CheckService.check_ban(user_id):
            return {"error":"User banned"}, 403

        PostsService.like_post(user_id, post_id)

        return {"message": "Like set successfully"}

    except KeyError:
        return {"error": "Invalid request format. Make sure you provide jwt, user_id, and post_id in the request."}, 400

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500



@post_api.route('/remove_like', methods=['POST'])
@jwt_required()
def remove_like_api():
    """
    API-запрос для удаления лайка у поста.

    Метод: POST
    Обязательные параметры в формате JSON:
    - "user_id": ID пользователя, который удаляет лайк (целое число, обязательно)
    - "post_id": ID поста, у которого удаляется лайк (целое число, обязательно)

    Заголовки:
    - "Authorization: Bearer <jwt_token>"

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
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
        "user_id": 1,
        "post_id": 123
    }' -L http://localhost:5000/api/post/remove_like

    Пример успешного ответа (код состояния 200):
    {
        "message": "Like removed successfully"
    }

    Пример ответа с ошибкой (код состояния 400, 403 или 500):
    {
        "error": "Invalid request format"  # или "You are not allowed to access remove like", "User banned", "User deleted", "An error occurred"
    }
    """
    try:

        current_user_phone = get_jwt_identity()


        data = request.get_json()

        user_id = data['user_id']

        user_phone = CheckService.get_phone_by_user_id(user_id)

        if current_user_phone != user_phone:
            return {
            "error": "You are not allowed to access remove like"
                    }, 403

        if CheckService.check_ban(user_id):
            return {"error":"User banned"}, 403

        post_id = data['post_id']

        PostsService.unlike_post(user_id, post_id)

        return {"message": "Like removed successfully"}

    except KeyError:
        return {"error": "Invalid request format. Make sure you provide jwt, user_id, and post_id in the request."}, 400

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500



@post_api.route('/post_comment', methods=['POST'])
@jwt_required()
def post_comment_api():
    """
    API-запрос для добавления комментария к посту.

    Метод: POST
    Обязательные параметры в формате JSON:
    - "user_id": ID пользователя, оставляющего комментарий (целое число, обязательно)
    - "post_id": ID поста, к которому оставляется комментарий (целое число, обязательно)
    - "comment_text": Текст комментария (строка, обязательно)

    Заголовки:
    - "Authorization: Bearer <jwt_token>"

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
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
        "user_id": 1,
        "post_id": 123,
        "comment_text": "This is a comment."
    }' -L http://localhost:5000/api/post/post_comment

    Пример успешного ответа (код состояния 200):
    {
        "message": "Comment posted successfully"
    }

    Пример ответа с ошибкой (код состояния 400, 403 или 500):
    {
        "error": "Invalid request format"  # или "You are not allowed to access send message", "User banned", "User deleted", "An error occurred"
    }
    """
    try:

        current_phone = get_jwt_identity()

        data = request.get_json()

        user_id = data['user_id']

        user_phone = CheckService.get_phone_by_user_id(user_id)

        if current_phone != user_phone:
            return {
            "error": "You are not allowed to access send message"
                    }, 403

        if CheckService.check_ban(user_id):
            return {"error":"User banned"}, 403


        post_id = data['post_id']
        comment_text = data['comment_text']

        PostsService.create_comment(comment_owner=user_id, post_id=post_id,
                            text=comment_text)

        return {"message": "Comment posted successfully"}

    except KeyError:
        return {"error": "Invalid request format. Make sure you provide jwt, user_id, post_id, and comment_text in the request."}, 400

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500



@post_api.route('/delete_comment', methods=['POST'])
@jwt_required()
def delete_comment_api():
    """
    API-запрос для удаления комментария к посту.

    Метод: POST
    Обязательные параметры в формате JSON:
    - "user_id": ID пользователя, удаляющего комментарий (целое число, обязательно)
    - "post_id": ID поста, к которому относится комментарий (целое число, обязательно)
    - "comment_id": ID комментария, который удаляется (целое число, обязательно)

    Заголовки:
    - "Authorization: Bearer <jwt_token>"

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
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{
        "user_id": 1,
        "post_id": 123,
        "comment_id": 456
    }' -L http://localhost:5000/api/post/delete_comment

    Пример успешного ответа (код состояния 200):
    {
        "success": true,
        "message": "Comment deleted successfully"
    }

    Пример ответа с ошибкой (код состояния 400, 403 или 500):
    {
        "success": false,
        "message": "Permission denied or comment not found"  # или "Invalid request format", "You are not allowed to access send message", "User banned", "User deleted", "An error occurred"
    }
    """
    try:

        current_phone = get_jwt_identity()

        data = request.get_json()

        user_id = data['user_id']

        user_phone = CheckService.get_phone_by_user_id(user_id)

        if current_phone != user_phone:
            return {
            "error": "You are not allowed to access send message"
                    }, 403

        if CheckService.check_ban(user_id):
            return {"error":"User banned"}, 403

        post_id = data['post_id']
        comment_id = data['comment_id']

        success = PostsService.delete_comment(comment_id=comment_id,
                                    user_id=user_id, post_id=post_id)

        if success:
            return {"success": True, "message": "Comment deleted successfully"}
        else:
            return {"success": False, "message": "Permission denied or comment not found"}

    except KeyError:
        return {"error": "Invalid request format. Make sure you provide  user_id, post_id, and comment_id in the request."}, 400

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
