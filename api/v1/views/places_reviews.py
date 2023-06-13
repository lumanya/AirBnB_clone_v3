#!/usr/bin/python3
""" Reviews Views"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews(place_id):
    """ Returns json of all reviews of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def reviews_id(review_id):
    """ Returns json of a review"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review """
    if review_id is None:
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a review"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update a review"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
