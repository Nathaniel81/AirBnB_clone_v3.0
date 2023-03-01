from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify, abort



@app_views.route('/states', methods=['GET', 'POST'])
def get_state():
    """ """
    if request.method == 'GET':
        states = [o.to_dict() for o in storage.all(State).values()]
        return jsonify(states)
    if request.method == 'POST':
        sent_data = request.get_json()
        if sent_data is None:
            abort(400, 'Not a JSON')
        if sent_data.get('name') is None:
            abort(400, 'Missing name')
        new_state = State(**sent_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state_wID(state_id=None):
    """ """
    o = storage.get(State, state_id)
    if o is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(o.to_dict())
