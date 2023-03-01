#!/usr/bin/python3
"""
This module contains Flask routes for handling CRUD operations on State and City objects in a RESTful API.
The routes support GET, POST, PUT, and DELETE requests to retrieve, create, update, and delete State and City resources. 
The module also imports and registers the app_views Blueprint to associate the routes with the Flask app.
 """
 
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_cities_by_state(state_id=None):
    """
    Returns a list of all cities in a state if the request is a GET.
    Creates a new city if the request is a POST. 
    """

    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    if request.method == 'GET':
        cities = [c.to_dict() for c in s.cities]
        return jsonify(cities)
    if request.method == 'POST':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        if sent_data.get('name') is None:
            abort(400, 'Missing name')
        #sent_data = {"name": "Alexandria"}
        sent_data['state_id'] = state_id
        new_city = City(**sent_data)
        # storage.new(new_city)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id=None):
    """
    Retrieves a city by its ID if the request is a GET.
    Deletes a city if the request is a DELETE.
    Updates a city if the request is a PUT.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        for k, v in sent_data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
