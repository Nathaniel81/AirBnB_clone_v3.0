#!/usr/bin/python3
"""Doc"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def show_status():
    """An end point to retrive ok status as a response"""
    return jsonify({"status": "OK"})
