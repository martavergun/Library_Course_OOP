import ctypes
from ctypes import c_char_p, c_bool, c_int, c_void_p


class LibraryInterface:
    def __init__(self):
        # Завантаження бібліотеки C++
        self.lib = ctypes.CDLL("C:/Users/ADMIN/source/repos/Home_Library/x64/Debug/Home_Library.dll")

        # Налаштування функцій
        self.lib.addBook.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int]
        self.lib.addBook.restype = c_void_p

        self.lib.viewBooks.restype = c_char_p

        self.lib.deleteBook.argtypes = [c_char_p]
        self.lib.deleteBook.restype = c_bool

        self.lib.searchBooks.argtypes = [c_char_p]
        self.lib.searchBooks.restype = c_char_p

        self.lib.searchBooksByTag.argtypes = [c_char_p]
        self.lib.searchBooksByTag.restype = c_char_p

        self.lib.sortBooksByAuthor.restype = None

        self.lib.getBooksByStatus.argtypes = [ctypes.c_int]
        self.lib.getBooksByStatus.restype = ctypes.c_char_p

        self.lib.getBooksByFormat.argtypes = [ctypes.c_int]
        self.lib.getBooksByFormat.restype = ctypes.c_char_p

        self.lib.saveToFile.argtypes = [c_char_p]
        self.lib.saveToFile.restype = c_void_p

        self.lib.loadFromFile.argtypes = [c_char_p]
        self.lib.loadFromFile.restype = c_void_p

    def add_book(self, title, author, year, genre, tags, status, format):
        format_map = {"Паперова": 0, "Електронна": 1}
        print(f"Adding book with format: {format}")  # Логування
        tags_string = ",".join(tags)
        self.lib.addBook(
            title.encode('utf-8'),
            author.encode('utf-8'),
            year,
            genre.encode('utf-8'),
            tags_string.encode('utf-8'),
            status,
            format_map[format]
        )


    def view_books(self):
        """Retrieve all books from the C++ library."""
        books = self.lib.viewBooks()
        if books:
            return books.decode("utf-8").strip().split("\n")
        return []

    def delete_book(self, title):

        return self.lib.deleteBook(title.encode('utf-8'))

    def search_books(self, title):
        if not title or not title.strip():
            print("Empty or invalid search query.")  # Логування помилки
            return []

        try:
            results = self.lib.searchBooks(title.encode('utf-8'))
            if results:
                books = results.decode('utf-8').strip().split("\n")
                print(f"Search results for '{title}': {books}")  # Логування результату
                return books
        except Exception as e:
            print(f"Error during search_books: {e}")
        return []

    def search_books_by_tag(self, tag):

        results = self.lib.searchBooksByTag(tag.encode('utf-8'))
        if results:
            return results.decode('utf-8').split("\n")
        return []

    def get_books_by_status(self, status):

        try:
            results = self.lib.getBooksByStatus(status)
            if results:
                books = results.decode('utf-8').strip().split("\n")
                print(f"Books with status {status}: {books}")  # Debug log
                return books
        except Exception as e:
            print(f"Error retrieving books by status: {e}")
        return []

    def update_book_status(self, title, new_status):

        try:
            print(f"Updating status for book: {title}, new status: {new_status}")  # Логування
            result = self.lib.updateBookStatus(title.encode('utf-8'), new_status)
            print(f"Result from C++: {result}")  # Логування результату
            return bool(result)
        except Exception as e:
            print(f"Error updating book status: {e}")
            return False

    def get_books_by_format(self, book_format):

        format_map = {"Paper": 0, "Electronic": 1}
        if book_format not in format_map:
            raise ValueError(f"Invalid format: {book_format}")

        # Виклик функції C++ бібліотеки
        results = self.lib.getBooksByFormat(format_map[book_format])
        if isinstance(results, bytes):
            return results.decode('utf-8').strip().split("\n")
        elif isinstance(results, str):
            return results.strip().split("\n")
        else:
            raise ValueError("Unexpected type of result from C++ function.")

    def save_books_to_file(self, filename):

        self.lib.saveToFile(filename.encode('utf-8'))

    def load_books_from_file(self, filename):

        self.lib.loadFromFile(filename.encode('utf-8'))

    def sort_books_by_format(self):
        self.library.sortBooksByFormat()
        self.load_books_to_table()
