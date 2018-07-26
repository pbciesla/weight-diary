import json

from flask import Flask, jsonify, abort, request, make_response, Response
# from flask_httpauth import HTTPBasicAuth

from weight_storage import *
from user_storage import *

app = Flask(__name__)

date_format = '%Y-%m-%d'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'resource not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.route('/<int:user_id>/weight')
def get_weight_list(user_id):
    weight_data = fetch_all_weight(user_id)
    if weight_data:
        return jsonify(weight_data)
    else:
        abort(404)


@app.route('/<int:user_id>/weight', methods=['POST'])
def add_actual_weight(user_id):
    if not request.json and 'value' not in request.json:
        abort(400)
    user = fetch_by_id(user_id)
    if user:
        weight_id = save_weight(request.json['value'], user_id)
        weight = fetch_weight_by_id(user_id, weight_id)
        return jsonify(weight)
    else:
        abort(404)


@app.route('/<int:user_id>/weight/<int:weight_id>', methods=['PUT'])
def update_weight_by_id(user_id, weight_id):
    if not request.json and 'value' not in request.json:
        abort(400)
    weight = fetch_weight_by_id(user_id, weight_id)
    if weight:
        new_weight = update_weight(user_id, weight_id, request.json['value'])
        return jsonify(new_weight)
    else:
        abort(404)


@app.route('/<int:user_id>/weight/<int:weight_id>', methods=['DELETE'])
def delete_weight_by_id(user_id, weight_id):
    weight = fetch_weight_by_id(user_id, weight_id)
    if weight:
        delete_weight(user_id, weight_id)
    else:
        abort(404)


@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or (
            'name' not in request.json or 'height' not in request.json
            or 'weight' not in request.json):
        abort(400)
    user = User(request.json['name'], request.json['height'],
                request.json['weight'])
    user_id = save_user(user)
    user = fetch_by_id(user_id)
    return jsonify(user.serialize())


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    if not request.json:
        abort(400)
    user = fetch_by_id(user_id)
    if user:
        user.height = request.json.get('height', user.height)
        user.weight = request.json.get('weight', user.weight)
        new_user = update_user(user)
        return jsonify(new_user.serialize())
    else:
        abort(404)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = fetch_by_id(user_id)
    if user:
        delete_user(user_id)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
