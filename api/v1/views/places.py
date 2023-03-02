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
from models.state import State
from models.amenity import Amenity


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

@app_views.route('/places_search', methods=['POST'])
def search_place():
    """Handles http POST request for searching places depending on some data"""
    data = request.get_json()
    if data is None:
        abort(400)
    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)
    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]
    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)
    return jsonify(places)
