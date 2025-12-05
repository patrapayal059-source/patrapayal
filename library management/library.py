import json

class Book:
    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}"

    def to_dict(self):
        return self.__dict__

class Library:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = self._load_books()

    def _load_books(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                books = []
                for item in data:
                    book = Book(item['title'], item['author'], item['isbn'], item['available'])
                    books.append(book)
                return books
        except FileNotFoundError:
            return []

    def _save_books(self):
        with open(self.filename, 'w') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)
 # CREATE
    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self._save_books()
        print(f"Book '{title}' added successfully.")

   

    # READ
    def list_all_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books:
            print(book)

    def find_book(self, search_term):
        found_books = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower() or search_term == book.isbn]
        if not found_books:
            print("No books found matching your search.")
            return []
        for book in found_books:
            print(book)
        return found_books

    # UPDATE
    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.available:
                book.available = False
                self._save_books()
                print(f"Book with ISBN {isbn} borrowed successfully.")
                return
        print(f"Book with ISBN {isbn} not found or already borrowed.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.available:
                book.available = True
                self._save_books()
                print(f"Book with ISBN {isbn} returned successfully.")
                return
        print(f"Book with ISBN {isbn} not found or not currently borrowed.")

    # DELETE
    def delete_book(self, isbn):
        initial_len = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]
        if len(self.books) < initial_len:
            self._save_books()
            print(f"Book with ISBN {isbn} deleted successfully.")
        else:
            print(f"Book with ISBN {isbn} not found.")

def main():
    library = Library()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. List All Books")
        print("3. Find Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Delete Book")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            library.add_book(title, author, isbn)
        elif choice == '2':
            library.list_all_books()
        elif choice == '3':
            search_term = input("Enter title, author, or ISBN to search: ")
            library.find_book(search_term)
        elif choice == '4':
            isbn = input("Enter ISBN of the book to borrow: ")
            library.borrow_book(isbn)
        elif choice == '5':
            isbn = input("Enter ISBN of the book to return: ")
            library.return_book(isbn)
        elif choice == '6':
            isbn = input("Enter ISBN of the book to delete: ")
            library.delete_book(isbn)
        elif choice == '7':
            print("Exiting Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

    if __name__ == "__main__":
        main()