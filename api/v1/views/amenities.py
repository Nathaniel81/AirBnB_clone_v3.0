#!/usr/bin/python3
""" 
This module defines routes for CRUD operations on Amenity objects in a Flask application.
It imports the Amenity class from the models.amenity module and the 
storage object from the models module to access the data.
It also imports the jsonify, abort, and request functions from the Flask module
for handling HTTP requests and responses.
"""

from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def get_amenities():
    """"
     Retrieves all Amenity objects from the storage and
     returns them in JSON format when route receives a GET request.
     Creates a new Amenity object from the data received in the request
     and saves it to the storage, then returns the new object in JSON format 
     along with a 201 status code if successful.
    """
    a = storage.all(Amenity)
    if a is None:
        abort(404)
    if request.method == 'GET':
        amenities = [o.to_dict() for o in a.values()]
        return jsonify(amenities)
    if request.method == 'POST':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        if sent_data.get('name') is None:
            abort(400, 'Missing name')
        new_obj = Amenity(**sent_data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_amenity_by_id(amenity_id=None):
    """
	GET: Returns Amenity object in JSON.
	DELETE: Deletes Amenity object from storage and returns empty JSON.
	PUT: Updates Amenity object with request data, 
 	saves to storage, and returns updated object in JSON.
    """
    a = storage.get(Amenity, amenity_id)
    if request.method == 'GET':
        return jsonify(a.to_dict())
    if request.method == 'DELETE':
        storage.delete(a)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        for k, v in sent_data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(a, k, v)
        a.save()
        return jsonify(a.to_dict())
