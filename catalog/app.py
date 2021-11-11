from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# database initialization
db = SQLAlchemy(app)

# marshmallow initialization
ma = Marshmallow(app)


# Book Class/Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __init__(self, title, category, price, quantity):
        self.title = title
        self.category = category
        self.price = price
        self.quantity = quantity


# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'category', 'price', 'quantity')


# Init Schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Add a book
@app.route('/addBook', methods=['POST'])
def add_book():
    title = request.json['title']
    category = request.json['category']
    price = request.json['price']
    quantity = request.json['quantity']

    new_book = Book(title, category, price, quantity)
    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


# Query by category
@app.route('/search/<cat>', methods=['GET'])
def search(cat):
    books = Book.query.filter_by(category=cat)
    return books_schema.jsonify(books)


# Query by Book ID
@app.route('/info/<id>', methods=['GET'])
def info(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)


# Update by book ID
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    book = Book.query.get(id)

    price = request.json['price']
    quantity = request.json['quantity']

    book.price = price
    book.quantity = quantity
    db.session.commit()

    return book_schema.jsonify(book)


# Purchase -From order server-
@app.route('/purchase/<id>', methods=['PUT'])
def purchase(id):
    book = Book.query.get(id)

    book.quantity = book.quantity - 1
    db.session.commit()

    return book_schema.jsonify(book)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
