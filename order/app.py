from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import os

# RUN-CMD# flask run --host=127.0.0.1 --port=3000
app = Flask(__name__)


# Purchase book from catalog server and if exists
@app.route('/purchase/<id>', methods=['GET'])
def purchase(id):
    # Get info of book from catalog server
    res = requests.get('http://localhost:5000/info/'+id)
    jsonResponse = res.json()
    # Check if quantity is valid (1 or more book exists)
    if jsonResponse['quantity'] > 0:
        # decrement quantity from catalog server
        resPUT = requests.put(
            'http://localhost:5000/purchase/'+id, data={'id': id})
        return resPUT.json()
    else:
        return jsonify({'Error': "Out of stock"})


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
