
# CREATE
def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self._save_books()
        print(f"Book '{title}' added successfully.")
