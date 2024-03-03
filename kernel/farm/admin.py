# # -*- coding: utf-8 -*-

# from dotenv import load_dotenv, find_dotenv

# from flask_admin import Admin, AdminIndexView
# from flask_admin.menu import MenuLink
# from flask_login import current_user

# from farm import app, db, login_manager
# from farm.models import (UserModel, UserAdmin,
#                          UserPosts, UserPostsAdmin,
#                          FriendsModel, FriendsAdmin,
#                          UserComments, UserCommentsAdmin,
#                          Model3D, Models3dAdmin, Users3DModel, LotsAdmin,
#                          LotMarket, UserWarnsAdmin, UserWarns, PostWarns,
#                          PostWarnsAdmin)


# load_dotenv(find_dotenv())

# @login_manager.user_loader
# def load_user(user_id):
#     return UserModel.query.get(int(user_id))

# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_active

#     def is_visible(self):
#         return False


# admin = Admin(app, index_view=MyAdminIndexView())
# admin.add_view(UserAdmin(UserModel, db.session, name='Пользователи'))
# admin.add_view(UserPostsAdmin(UserPosts, db.session, name='Посты'))
# admin.add_view(UserCommentsAdmin(UserComments, db.session, name='Комментарии'))
# admin.add_view(FriendsAdmin(FriendsModel, db.session))
# admin.add_view(Models3dAdmin(Model3D, db.session))
# admin.add_view(LotsAdmin(LotMarket, db.session, name='Лоты'))
# admin.add_view(UserWarnsAdmin(UserWarns, db.session,
#                             name='Жалобы на пользователей'))


# from farm.models.codes import SMSAdmin, SMSCodes

# admin.add_view(SMSAdmin(SMSCodes, db.session))

# admin.add_link(MenuLink(url='https://github.com/lyaguxafrog', name='Автор'))
# admin.add_link(MenuLink(name='Выйти', url='/logout'))

# login_manager.init_app(app)
