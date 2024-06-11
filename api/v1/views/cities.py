#!/usr/bin/python3
"""view for City objects that handles all
default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """retrives the list of all city objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = []
    cities = state.cities
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def city(city_id):
    """retrives a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city object"""
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates a new city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    date = request.get_json()
    if not date:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in date:
        return jsonify({"error": "Missing name"}), 400
    date['state_id'] = state_id
    new_city = City(**date)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city object"""
    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
