from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import urllib.parse
import os

# RUN-CMD# flask run --host=127.0.0.1 --port=6000
app = Flask(__name__)


# Query by category
@app.route("/search/<cat>", methods=["GET"])
def search(cat):
    res = requests.get("http://localhost:5000/search/" + cat)
    jsonResponse = jsonify(res.json())
    return jsonResponse


# Query by Book ID
@app.route("/info/<id>", methods=["GET"])
def info(id):
    res = requests.get("http://localhost:5000/info/" + id)
    jsonResponse = res.json()
    return jsonResponse


# Purchase -From order server-
@app.route("/purchase/<id>", methods=["GET"])
def purchase(id):
    res = requests.get("http://localhost:3000/purchase/" + id)
    jsonResponse = jsonify(res.json())
    return jsonResponse


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
