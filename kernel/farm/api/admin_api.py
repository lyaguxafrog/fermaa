# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from farm import db
from farm.models import (Ferma, Garden, GardenCell,
                         Seeds, SeedInformation, SeedLevel)


admin_api = Blueprint('api', __name__)


@admin_api.route('/get_ferma/<int:ferma_id>/', methods=['GET'])
def get_ferma(ferma_id):
    ferma = Ferma.query.get(ferma_id)
    if ferma:
        return jsonify({
            'id': ferma.id,
            'garden_list': ferma.garden_list,
            'size': ferma.size
        })
    else:
        return jsonify({"error": "Ferma not found"}), 404

@admin_api.route('/get_garden/<int:garden_id>/', methods=['GET'])
def get_garden(garden_id):
    garden = Garden.query.get(garden_id)
    if garden:
        return jsonify({
            'id': garden.id,
            'cells_list': garden.cells_list,
            'name': garden.name,
            'user': garden.user
        })
    else:
        return jsonify({"error": "Garden not found"}), 404

@admin_api.route('/get_garden_cell/<int:garden_cell_id>/', methods=['GET'])
def get_garden_cell(garden_cell_id):
    garden_cell = GardenCell.query.get(garden_cell_id)
    if garden_cell:
        return jsonify({
            'id': garden_cell.id,
            'status': garden_cell.status,
            'seed': garden_cell.seed
        })
    else:
        return jsonify({"error": "GardenCell not found"}), 404

@admin_api.route('/get_seeds/<int:seeds_id>/', methods=['GET'])
def get_seeds(seeds_id):
    seeds = Seeds.query.get(seeds_id)
    if seeds:
        return jsonify({
            'id': seeds.id,
            'name': seeds.name,
            'pictures': seeds.pictures,
            'description': seeds.description,
            'url_pics': seeds.url_pics,
            'levels': seeds.levels,
            'seeds_list': seeds.seeds_list,
            'start': str(seeds.start),
            'information': seeds.information
        })
    else:
        return jsonify({"error": "Seeds not found"}), 404

@admin_api.route('/get_seed_information/<int:seed_info_id>/', methods=['GET'])
def get_seed_information(seed_info_id):
    seed_information = SeedInformation.query.get(seed_info_id)
    if seed_information:
        return jsonify({
            'id': seed_information.id,
            'text': seed_information.text,
            'data': seed_information.data
        })
    else:
        return jsonify({"error": "SeedInformation not found"}), 404

@admin_api.route('/get_seed_level/<int:seed_level_id>/', methods=['GET'])
def get_seed_level(seed_level_id):
    seed_level = SeedLevel.query.get(seed_level_id)
    if seed_level:
        return jsonify({
            'id': seed_level.id,
            'picture': seed_level.picture,
            'levels': seed_level.levels,
            'name': seed_level.name,
            'description': seed_level.description,
            'end_date': str(seed_level.end_date)
        })
    else:
        return jsonify({"error": "SeedLevel not found"}), 404


@admin_api.route('/create_ferma/', methods=['POST'])
def create_ferma():
    data = request.get_json()
    ferma = Ferma(**data)
    db.session.add(ferma)
    db.session.commit()
    return jsonify({"message": "Ferma created successfully", "ferma_id": ferma.id}), 201

@admin_api.route('/create_garden/', methods=['POST'])
def create_garden():
    data = request.get_json()
    garden = Garden(**data)
    db.session.add(garden)
    db.session.commit()
    return jsonify({"message": "Garden created successfully", "garden_id": garden.id}), 201

@admin_api.route('/create_garden_cell/', methods=['POST'])
def create_garden_cell():
    data = request.get_json()
    garden_cell = GardenCell(**data)
    db.session.add(garden_cell)
    db.session.commit()
    return jsonify({"message": "GardenCell created successfully", "garden_cell_id": garden_cell.id}), 201

@admin_api.route('/create_seeds/', methods=['POST'])
def create_seeds():
    data = request.get_json()
    seeds = Seeds(**data)
    db.session.add(seeds)
    db.session.commit()
    return jsonify({"message": "Seeds created successfully", "seeds_id": seeds.id}), 201

@admin_api.route('/create_seed_information/', methods=['POST'])
def create_seed_information():
    data = request.get_json()
    seed_information = SeedInformation(**data)
    db.session.add(seed_information)
    db.session.commit()
    return jsonify({"message": "SeedInformation created successfully", "seed_info_id": seed_information.id}), 201

@admin_api.route('/create_seed_level/', methods=['POST'])
def create_seed_level():
    data = request.get_json()
    seed_level = SeedLevel(**data)
    db.session.add(seed_level)
    db.session.commit()
    return jsonify({"message": "SeedLevel created successfully", "seed_level_id": seed_level.id}), 201
