from flask import Flask, render_template, request, redirect, abort
from models import Book

app = Flask(__name__)

# Dummy books
if not Book.get_all():
    for i in range(1, 51):
        Book(f"Book {i}", f"Author {i}", 2000 + i % 20, 100 + i, "Genre A")

@app.route("/books")
def books():
    page = int(request.args.get("page", 1))
    per_page = 10
    all_books = Book.get_all()
    total_pages = (len(all_books) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_books = all_books[start:end]
    return render_template("books.html", books=page_books, page=page, total_pages=total_pages)

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        abort(404, description="Not Found")
    return render_template("book_detail.html", book=book)

@app.route("/books/new")
def new_book_form():
    return render_template("book_form.html")

@app.route("/books", methods=["POST"])
def create_book():
    title = request.form["title"]
    author = request.form["author"]
    year = int(request.form["year"])
    total_pages = int(request.form["total_pages"])
    genre = request.form["genre"]
    
    book = Book(title, author, year, total_pages, genre)
    book.save()
    return redirect("/books")
