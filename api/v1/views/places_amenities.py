#!/usr/bin/python3
""" Places Amenities Views"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def places_amenities(place_id):
    """ Returns json of all amenities of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False)
def places_amenities_id(place_id, amenity_id):
    """ Returns json of a amenity"""
    place = storage.get(Place, place_id)
    if place:
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """ Deletes a amenity """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_places_amenities(place_id, amenity_id):
    """create a amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
