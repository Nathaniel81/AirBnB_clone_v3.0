from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_cities(state_id=None):
    """ """
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
        new_city.save()
        return jsonify(new_city.to_dict()), 201
