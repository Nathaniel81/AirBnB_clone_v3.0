#!/usr/bin/python3
"""
Defines Flask routes for managing Place objects associated with City objects.
It includes endpoints for retrieving, deleting, updating, and creating
Place objects, as well as endpoints for retrieving all Place objects 
associated with a City object.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def get_place(place_id=None):
    """
    Retrieves, deletes, or updates a Place object based on the provided place_id
    """
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(p.to_dict())
    if request.method == 'DELETE':
        storage.delete(p)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        for k, v in sent_data.items():
            if k not in ['id', 'name', 'city_id', 'created_at', 'updated_at']:
                setattr(p, k, v)
            p.save()
            return jsonify(p.to_dict())

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_place_by_city(city_id=None):
    """
    Retrieves all places associated with the provided city_id or creates
    a new Place object associated with the provided city and user. 
    """
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    if request.method == 'GET':
        places = [p.to_dict() for p in c.places]
        return jsonify(places)
    if request.methods == 'POST':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        if sent_data.get('user_id') is None:
            abort(400, 'Missing user_id')
        u = storage.get(User, sent_data.get('user_id'))
        if u is None:
            abort(404)
        if sent_data.get('name') is None:
            abort(400, 'Missing name')
        sent_data['city_id'] = city_id
        new_place = Place(**sent_data)
        new_place.save()
        return jsonify(new_place.to_dict), 200
