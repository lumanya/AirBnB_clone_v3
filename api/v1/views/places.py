#!/usr/bin/python3
""" Places Views"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places(city_id):
    """ Returns json of all places of a city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def places_id(place_id):
    """ Returns json of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_place():
    """search a place"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    places = storage.all(Place).values()
    if 'states' in request.get_json() and
    len(request.get_json()['states']) > 0:
        places = [place for place in places if place.city.state_id in
                  request.get_json()['states']]
    if 'cities' in request.get_json() and
    len(request.get_json()['cities']) > 0:
        places = [place for place in places if place.city_id in
                  request.get_json()['cities']]
    if 'amenities' in request.get_json() and
    len(request.get_json()['amenities']) > 0:
        places = [place for place in places if all(amenity.id in
                  [amenity.id for amenity in place.amenities] for amenity in
                  request.get_json()['amenities'])]
    return jsonify([place.to_dict() for place in places])
