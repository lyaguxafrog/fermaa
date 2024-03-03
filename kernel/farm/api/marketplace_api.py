from crypt import methods
from re import U
from types import new_class
from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from farm.services import MarketPlaceService, CheckService

marketplace_api = Blueprint('makrketplace_api', __name__)


@marketplace_api.route('/admin/create_category', methods=['POST'])
@jwt_required()
def create_category_api():

    current_phone = get_jwt_identity()

    data = request.get_json()

    user_id = data['user_id']

    if current_phone != CheckService.get_phone_by_user_id(user_id):
        return jsonify({"error":"Invalid token"}), 403

    cat_name = data['category']

    try:
        new_category = MarketPlaceService.create_category(cat_name)
        return jsonify(
            {
                'message':'Category created',
                'category_id': new_category.id
            }
                ), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@marketplace_api.route('/admin/create_lot', methods=['POST'])
@jwt_required()
def create_lot_api():

    current_phone = get_jwt_identity()

    data = request.get_json()

    user_id = data['user_id']

    if current_phone != CheckService.get_phone_by_user_id(user_id):
        return jsonify({"error":"Invalid token"}), 403

    name = data['name']
    picture_id = data['picture_id']
    category_id = data['category_id']
    sum = data['sum']


    try:
        new_lot = MarketPlaceService.create_lot(
            name=name,
            picture_id=picture_id,
            category_id=category_id,
            summ=sum,
            review=None,
            reviews_list=None
        )

        return jsonify(
            {
                "message":"Lot created",
                "lot_id": new_lot.id
                }
            ), 201

    except Exception as e:
        return jsonify(
            {
                "error":str(e)
            }
        ), 500


@marketplace_api.route('/admin/create_description', methods=['POST'])
@jwt_required()
def create_description_api():

    current_phone = get_jwt_identity()

    data = request.get_json()

    user_id = data['user_id']

    if current_phone != CheckService.get_phone_by_user_id(user_id):
        return jsonify({"error":"Invalid token"}), 403

    lot_id = data['lot_id']
    text_1 = data['text_1']
    text_2 = data['text_2']

    try:
        new_description = MarketPlaceService.create_lot_description(
            lot_id=lot_id,
            text_1=text_1,
            text_2=text_2
        )

        return jsonify(
            {
                "message":"Description created",
                "description_id":new_description.id
            }
        ), 201

    except Exception as e:
        return jsonify(
            {
                "error":str(e)
            }
        ), 500
