#!/usr/bin/python3
""" 
This module defines routes for CRUD operations on User objects in a Flask application.
It imports the User class from the models.user module and the 
storage object from the models module to access the data.
It also imports the jsonify, abort, and request functions from the Flask module
for handling HTTP requests and responses.
"""

from models.user import User
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'])
def get_users():
    """"
     Retrieves all User objects from the storage and
     returns them in JSON format when route receives a GET request.
     Creates a new User object from the data received in the request
     and saves it to the storage, then returns the new object in JSON format 
     along with a 201 status code if successful.
    """
    a = storage.all(User)
    if request.method == 'GET':
        users = [o.to_dict() for o in a.values()]
        return jsonify(users)
    if request.method == 'POST':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        if sent_data.get('email') is None:
            abort(400, 'Missing email')
        if sent_data.get('password') is None:
            abort(400, 'Missing password')
        new_obj = User(**sent_data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_user_by_id(user_id=None):
    """
	GET: Returns User object in JSON.
	DELETE: Deletes User object from storage and returns empty JSON.
	PUT: Updates User object with request data, 
 	saves to storage, and returns updated object in JSON.
    """
    a = storage.get(User, user_id)
    if request.method == 'GET':
        return jsonify(a.to_dict())
    if request.method == 'DELETE':
        storage.delete(a)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        sent_data = request.get_json()
        for k, v in sent_data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(a, k, v)
        a.save()
        return jsonify(a.to_dict())
