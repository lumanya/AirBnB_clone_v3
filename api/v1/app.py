#!/usr/bin/python3
""" Flask api to handle objects """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
