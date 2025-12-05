from flask import Flask, request, jsonify
from library import Library  # import your existing code

app = Flask(__name__)
library = Library()  # use your DB-based library system


@app.route("/books", methods=["GET"])
def get_books():
    conn = library._connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    books = [{
        "title": row[0],
        "author": row[1],
        "isbn": row[2],
        "available": bool(row[3])
    } for row in rows]

    return jsonify(books)


@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    isbn = data.get("isbn")

    library.add_book(title, author, isbn)
    return jsonify({"message": "Book added successfully!"})


@app.route("/books/<isbn>/borrow", methods=["PUT"])
def borrow_book(isbn):
    library.borrow_book(isbn)
    return jsonify({"message": "Borrow request processed."})


@app.route("/books/<isbn>/return", methods=["PUT"])
def return_book(isbn):
    library.return_book(isbn)
    return jsonify({"message": "Return request processed."})


@app.route("/books/<isbn>", methods=["DELETE"])
def delete_book(isbn):
    library.delete_book(isbn)
    return jsonify({"message": "Book deleted if it existed."})


# ------------------------
# Run SERVER with a PORT
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # <<< SERVER RUNNING ON PORT 5000