from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)


@app.route('/')
def index():
    books = Book.query.all()
    return books


if __name__ == "__main__":
    db.create_all()

    book1 = Book(title="HowtogetagoodgradeinDOSin40minutesaday",
                 category="distributed systems",
                 quantity=100, price=14.00)
    book2 = Book(title="RPCsforNoobs",
                 category="distributed systems",
                 quantity=100, price=12.00)
    book3 = Book(title="XenandtheArtofSurvivingUndergraduateSchool",
                 category="undergraduate school",
                 quantity=100, price=15.00)
    book4 = Book(title="CookingfortheImpatientUndergrad",
                 category="undergraduate school",
                 quantity=100, price=18.00)

    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(book4)
    db.session.commit()

    app.run(debug=True)
