 # DELETE
def delete_book(self, isbn):
        initial_len = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]
        if len(self.books) < initial_len:
            self._save_books()
            print(f"Book with ISBN {isbn} deleted successfully.")
        else:
            print(f"Book with ISBN {isbn} not found.")
