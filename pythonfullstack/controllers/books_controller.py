from flask import Blueprint, request, jsonify
from services.book_service import BookService

books_blueprint = Blueprint("books", __name__)
service = BookService()

# CREATE
@books_blueprint.route("/", methods=["POST"])
def add_book():
    data = request.json
    return jsonify(service.create_book(data)), 201

# READ ALL
@books_blueprint.route("/", methods=["GET"])
def get_books():
    return jsonify(service.list_books())

# READ ONE
@books_blueprint.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return jsonify(service.get_book(book_id))

# UPDATE
@books_blueprint.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    return jsonify(service.update_book(book_id, data))

# DELETE
@books_blueprint.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    return jsonify(service.delete_book(book_id))
