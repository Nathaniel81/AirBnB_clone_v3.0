from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify

app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id=None):
    """ """
    s = storage.get(State, state_id)
    cities = [c.to_dict() for c in s.cities]
    return jsonify(cities)
    