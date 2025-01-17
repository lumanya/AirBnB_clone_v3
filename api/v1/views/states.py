#!/usr/bin/python3
""" create states view"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False)
def states():
    """ Returns json of all states"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_id(state_id):
    """ Returns json of a state"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a state """
    if state_id is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
