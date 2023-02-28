#!/usr/bin/python3
"""
This is a Flask web application that serves as an API endpoint, 
connecting to a database and running on the specified host and port. 
It uses the models module and registers the app_views blueprint.
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.errorhandler(404)
def page_not_found(error):
    """
    Handler for 404 errors that returns 
    a JSON-formatted 404 status code response.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def teardown(execute):
    """Removes the current SQLAlchemy session after each request
    is completed"""
    storage.close()

    
if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True, debug=True)
