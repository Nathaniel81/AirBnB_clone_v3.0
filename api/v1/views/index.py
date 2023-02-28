#!/usr/bin/python3
"""Defines a Flask route at /status that returns a JSON object containing the string "OK", 
indicating a successful status, and has a docstring that describes the endpoint."""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def show_status():
    """An end point to retrive ok status as a response"""
    return jsonify({"status": "OK"})
