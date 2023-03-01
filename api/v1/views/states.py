from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify



@app_views.route('/states', methods=['GET', 'POST'])
def all_state():
    """ """
    if request.method == 'GET':
        st_list = []
        for o in storage.all('State').values().to_dict():
            st_list.append(o)
        return jsonify(st_list)
