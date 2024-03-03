# -*- coding: utf-8 -*-


from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from farm.models import Pictures
from farm.services import PicturesService
from werkzeug.utils import secure_filename
from farm import db, app
import os

picture_api = Blueprint('picture_api', __name__)

@picture_api.route('/upload_picture', methods=['POST'])
def upload_picture_api():
    try:
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Check if the file is selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Securely save the filename
        filename = secure_filename(file.filename)

        # Create a new Pictures instance using the generated name
        new_picture = Pictures(
            name=filename,
            image_data=file.read(),
            image_oid=b'',
            url=f"/uploads/pictures/{filename}"
        )

        # Save the picture data to the database using the service
        picture_id = PicturesService.save_picture(new_picture.name, new_picture.image_data)

        return jsonify({"message": "Picture uploaded successfully", "picture_id": picture_id})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500




@picture_api.route('/get_picture/<int:picture_id>', methods=['GET'])
def get_picture_api(picture_id):
    try:
        # Ищем картинку в базе данных по идентификатору
        picture = Pictures.query.get(picture_id)

        if picture is None:
            return jsonify({"error": "Picture not found"}), 404

        # Формируем ответ с информацией о картинке
        response_data = {
            "picture_id": picture.id,
            "picture_url": picture.url
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    file_path = os.path.join(app.static_folder, filename)
    print(f"Trying to access file: {file_path}")
    return send_from_directory(app.static_folder, filename)
