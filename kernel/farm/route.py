# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required


from farm import app, login_manager

from farm.models import UsersModel

from farm.api.user_resource import user_api
from farm.api.marketplace_api import marketplace_api
from farm.api.chat_resource import chat_api
from farm.api.post_resource import post_api
from farm.api.dep_api import picture_api
from farm.api.admin_api import admin_api

@login_manager.user_loader
def load_user(user_id):
    return UsersModel.get_user(user_id)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        email = request.form['user']
        password = request.form['password']
        user = UsersModel.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Неправильный email пользователя или пароль', 'error')

    return render_template('login.html')



# coded by Adrian Makridenko
# @lyaguxafrog


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('login'))

# api

app.register_blueprint(user_api, url_prefix='/api/user')
app.register_blueprint(marketplace_api, url_prefix='/api/marketplace')
app.register_blueprint(chat_api, url_prefix='/api/chats')
app.register_blueprint(post_api, url_prefix='/api/post')
app.register_blueprint(picture_api, url_prefix='/api/options')
app.register_blueprint(admin_api, url_prefix='/api/admin')
