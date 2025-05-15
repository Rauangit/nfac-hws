class Book:
    _books = []
    _id_counter = 1

    def __init__(self, title, author, year, total_pages, genre):
        self.id = Book._id_counter
        self.title = title
        self.author = author
        self.year = year
        self.total_pages = total_pages
        self.genre = genre
        Book._id_counter += 1
        Book._books.append(self)

    def save(self):
        pass

    @staticmethod
    def get_all():
        return Book._books

    @staticmethod
    def get_by_id(book_id):
        return next((book for book in Book._books if book.id == book_id), None)

    def update(self, title, author, year, total_pages, genre):
        self.title = title
        self.author = author
        self.year = year
        self.total_pages = total_pages
        self.genre = genre

    @staticmethod
    def delete(book):
        Book._books.remove(book)
