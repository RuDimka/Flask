from flask import Flask, abort, request, current_app
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)


app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# QuoteModel --> dict --> JSON
class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __repr__(self):
        return f"Quote: {self.author} {self.text}"

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text
        }


# Сериализация: lis[quotes] --> list[dict] --> str(JSON)
@app.route("/quotes")
def get_all_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = QuoteModel.query.get(id)
    if quote is None:
        return {"error": f"Quote with id={id} not found"}, 404
    return quote.to_dict(), 200


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Author: {self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quotes": self.quotes
        }



if __name__ == "__main__":
    app.run(debug=True)