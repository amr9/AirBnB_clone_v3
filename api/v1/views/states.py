#!/usr/bin/python3
"""view for State objects that handles all
default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """retrives the list of all state objects"""
    state_list = []
    states = storage.all(State)
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def state(state_id):
    """retrives a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("states/<string:state_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state object"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
