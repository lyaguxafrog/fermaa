# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash

from farm import db, app
from farm.models import UsersModel


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


dbname = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")

app.app_context().push()

email = input("email: ")
password = input('passowrd: ')

role_num = int(input('''1 - Супер-админ\n
2 - Админ-ферма\n
3 - Админ-3D\n
4 - Пользователь\n
: '''))



if role_num == 1:
    role = 'super-admin'
elif role_num == 2:
    role = 'admin-farm'
elif role_num == 3:
    role = 'admin-3d'
elif role_num == 4:
    role = 'user'
else:
    print('Неверная роль')
    exit()

password_hash = generate_password_hash(password)

username = f"TestUser2_{role}"
name = username

user = UsersModel(email=email,
                  password=password_hash,
                  role=role,
                  phone="TEST2",
                  username=username,
                  name=name)


db.session.add(user)
db.session.commit()

db.create_all()
