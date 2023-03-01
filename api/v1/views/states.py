from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify



@app_views.route('/states', methods=['GET', 'POST'])
def all_state():
    """ """
    if request.method == 'GET':
        states = [o.to_dict() for o in storage.all(State).values()]
        return jsonify(states)
