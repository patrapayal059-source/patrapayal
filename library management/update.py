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
