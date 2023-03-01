from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request

app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id=None):
    """ """
    s = storage.get(State, state_id)
    if s is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        all_cities = storage.all('City')
        cities = [c.to_dict() for c in all_cities.values() if c.state_id == state_id]
    
        return jsonify(cities)
    