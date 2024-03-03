# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Tuple, Union
from sqlalchemy.orm import joinedload

from farm import db
from farm.models import Posts, PostComment, LikesToPosts
from farm.services import PicturesService

class PostsService():
    """
    Сервис для работы с постами

    * `create_post` - создание поста
    * `delete_post` - удаления постов
    * `like_post` - лайк поста
    * `unlike_post` - убрать лайк с поста
    * `create_comment` - написать комментария
    * `delete_comment` - удаления комментария
    """

    @staticmethod
    def create_post(owner_id: int, text: str,
                    picture_data: Optional[bytes]) -> int:
        """
        Функция создания поста

        :param owner_id: ID автора поста
        :param text: Текст поста
        :param picture_data: картинка

        :return: ID поста
        """

        if picture_data:


            pic_id = PicturesService.save_picture(picture_data=picture_data)

            new_post = Posts(
                owner_id=owner_id,
                timestamp=datetime.now(),
                post_text=text,
                picture=pic_id
                ) # type: ignore

        else:
           new_post = Posts(
                owner_id=owner_id,
                timestamp=datetime.now(),
                post_text=text
                ) # type: ignore

        db.session.add(new_post)
        db.session.commit()

        return new_post.id


    @staticmethod
    def get_post(post_id: int) -> Optional[Posts]:
        """
        Получение поста по идентификатору.

        :param post_id: Идентификатор поста.

        :return: Объект поста или None, если не найден.
        """

        post: Optional[Posts] = Posts.query.options(joinedload(
            Posts.user)).get(post_id)

        return post

    @staticmethod
    def delete_post(post_id: int) -> bool:
        """
        Функция удаления поста

        :param post_id:

        :return: True - пост удален, False - пост не найдем
        """
        post = Posts.query.get(post_id)


        if not post:
            return False

        db.session.delete(post)
        db.session.commit()

        return True

    @staticmethod
    def like_post(like_owner: int, post_id: int) -> bool:
        """
        Функция лайка поста

        :param like_owner: ID пользователя, который лайкает пост
        :param post_id: ID поста

        :return: True - лайк поставлен, False - ошибка
        """

        post = Posts.query.get(post_id)

        if not post:
            return False


        like = LikesToPosts(
            like_owner=like_owner,
            post_id=post_id,
            timestamp=datetime.now()
        ) # type: ignore


        db.session.add(like)
        db.session.commit()

        post.likes += 1
        db.session.commit()

        return True


    @staticmethod
    def unlike_post(unlike_owner: int, post_id: int) -> bool:
        """
        Функция снятия лайка с поста

        :param unlike_owner: ID пользователя, который снимает лайк с поста
        :param post_id: ID поста

        :return: True - лайк снят, False - ошибка
        """

        like = LikesToPosts.query.filter_by(like_owner=unlike_owner,
                                        post_id=post_id).first()

        if not like:
            return False

        try:
            db.session.delete(like)
            db.session.commit()

            post = Posts.query.get(post_id)
            if post:
                post.likes -= 1
                db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            return False


    @staticmethod
    def create_comment(comment_owner: int,
                post_id: int, text: str) -> Tuple[bool, str]:
        """
        Функция создания пользователя

        :param comment_owner: ID автора комментария
        :param post_id: ID поста
        :param text: Текст комментария

        :return: Bool оп операции и комментарий к этой операции
        """
        new_comment = PostComment(
            comment_owner=comment_owner,
            post=post_id, text=text) # type: ignore

        try:
            db.session.add(new_comment)
            db.session.commit()
            return True, 'Comment created successfully'
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to create comment. Error: {str(e)}'


    @staticmethod
    def delete_comment(comment_id: int,
            user_id: int, post_id: int) -> Tuple[bool, str]:
        """
        Функция удаления комментария

        :param comment_id: ID комментария
        :param user_id: ID пользователя (автора поста/комментария)
        :param post_id: ID поста, к которому относится комментарий

        :return: Bool на успешность, комментарий к операции
        """

        comment = PostComment.query.get(comment_id)

        if comment:
            # Проверка, является ли комментарий комментарием к нужному посту
            if post_id == comment.post:
                # Проверка, является ли пользователь автором комментария или поста
                if user_id == comment.comment_owner or user_id == comment.post:
                    try:
                        db.session.delete(comment)
                        db.session.commit()
                        return True, 'Comment deleted successfully'
                    except Exception as e:
                        db.session.rollback()
                        return False, f'Failed to delete comment. Error: {str(e)}'
                else:
                    return (False, 'User does not have permission to delete this comment')
            else:
                return False, 'Comment does not belong to the specified post'
        else:
            return False, 'Comment not found'
