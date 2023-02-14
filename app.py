from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic', cascade="all, delete-orphan") #lazy='dynamic' - постоянная связь двух таблиц

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "authors_id": self.id,
            "name": self.name
        }


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author_id = author.id
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "text": self.text
        }


# Resource: Author
@app.route("/authors")
def get_authors():
    authors = AuthorModel.query.all()
    authors_dict = []
    for author in authors:
        authors_dict.append(author.to_dict())
    return authors_dict


# @app.route("/authors/<int:authors_id>")
# def get_author_by_id(authors_id):
#     authors = AuthorModel.query.all(authors_id)
#     authors_dict = []
#     for author in authors:
#         authors_dict.append(author.to_dict())
#         return {"error": f"Quotes with author={author} not found"}, 404
#     return authors.to_dict, 201

@app.route("/authors/<int:authors_id>")
def get_author_by_id(authors_id):
    author = AuthorModel.query.get(authors_id)
    if author is None:
        return {"error": f"Author with id={id} not found"}, 404
    return author.to_dict, 201


@app.route("/authors", methods=["POST"])
def create_author():
    author_data = request.json
    print(author_data, "!!!")
    author = AuthorModel(author_data["name"])
    db.session.add(author)
    db.session.commit()
    return author.to_dict(), 201


@app.route("/authors/<int:authors_id>", methods=["DELETE"])
def delete_all_authors(authors_id):
    author = AuthorModel.query.get(authors_id)
    if author is None:
        return f"Author with id={authors_id} not found.", 404
    db.session.delete(author)
    db.session.commit()
    return f"Author with id={authors_id} is delete", 200


# Resource: Quote
@app.route("/quotes")
def get_all_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict


@app.route("/quotes/<int:id>")
def get_quotes_id(id):
    quote = QuoteModel.query.all(id)
    if quote is None:
        return {"error": f"Quotes with id={id} not found"}, 404
    return quote.to_dict, 200

#help(SQLAlchemy)


if __name__ == "__main__":
    app.run(debug=True)