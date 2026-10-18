from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Book

app = Flask(__name__)

# Tell Flask where our database is located
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"

# Disable unnecessary modification tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect the database to our Flask application
db.init_app(app)

# Set up database migrations
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "Welcome to the Library Management System!"


@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()

    books_list = []

    for book in books:
        books_list.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "available": book.available
        })

    return jsonify(books_list)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    new_book = Book(
        title=data["title"],
        author=data["author"]
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book added succesfully",
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "available": new_book.available
    }), 201

@app.route("/books/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error":"Book not found"}), 404

    data = request.get_json()

    if "title" in data:
        book.title = data["title"]

    if "author" in data:
        book.author = data ["author"]

    if "available" in data:
        book.available = data["available"]

    db.session.commit()

    return jsonify({
        "message": "Book updated Successfully",
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "available": book.available
    })

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)