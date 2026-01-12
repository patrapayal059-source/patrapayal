from flask import Blueprint, render_template, request, redirect, url_for

books_bp = Blueprint("books", __name__, url_prefix="/books")

BOOKS = ["Python Basics", "Flask Web Development", "Django for Beginners","c++","java"]

@books_bp.route("/", methods=["GET", "POST"])
def books():
    if request.method == "POST":
        book_name = request.form.get("book_name")
        if book_name:
            BOOKS.append(book_name)
        return redirect(url_for("books.books"))

    return render_template("books.html", books=BOOKS)


@books_bp.route("/delete/<int:book_id>")
def delete_book(book_id):
    if 0 <= book_id < len(BOOKS):
        BOOKS.pop(book_id)
    return redirect(url_for("books.books"))
