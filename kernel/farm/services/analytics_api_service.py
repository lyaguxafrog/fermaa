# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import os
from dotenv import load_dotenv, find_dotenv


from farm.models import FarmAnalytic, PrintedAnalytic
from farm import db


load_dotenv(find_dotenv())

api_url = os.getenv("FERMA_API_URL")
time = int(os.getenv("REQUEST_TIME")) # type: ignore

def get_and_save_data():
    # Запрос к вашему API
    environmental_data_response = requests.get(f'{api_url}/environmental_data/latest/')
    printers_info_response = requests.get(f'{api_url}/3d_printers/')

    # Обработка данных
    environmental_data = environmental_data_response.json()
    printers_info = printers_info_response.json()

    # Создание объектов моделей и запись в базу данных
    farm_analytic = FarmAnalytic(
        timestamp=datetime.strptime(environmental_data['date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        co2=environmental_data['CO2'],
        air_temperature=environmental_data['air_temperature'],
        air_humidity=environmental_data['air_humidity'],
        UV_index=environmental_data['UV_index'],
        soil_humidity_1_centimeter=environmental_data['soil_humidity_1_centimeter'],
        soil_humidity_1_5_centimeter=environmental_data['soil_humidity_1_5_centimeter']
    ) # type: ignore

    printed_analytic = PrintedAnalytic(
        total_printers=printers_info['total_printers'],
        free_printers=printers_info['free_printers'],
        printers_info=printers_info['printers_info'],
        update_time=datetime.now()
    ) # type: ignore

    db.session.add(farm_analytic)
    db.session.add(printed_analytic)
    db.session.commit()



scheduler = BackgroundScheduler()
scheduler.add_job(func=get_and_save_data, trigger="interval", hours=time)
scheduler.start()
