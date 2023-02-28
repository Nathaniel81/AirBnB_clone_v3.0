#!/usr/bin/python3
"""Defines a Flask route"""

from flask import jsonify
from api.v1.views import app_views

from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/status', methods=['GET'])
def show_status():
    """An end point to retrive "OK" status as a response"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each objects by type"""
    cls_mapper = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    res = {}
    for k, v in cls_mapper:
        res[k] = storage.count(v)
    return jsonify(res)
