import sqlite3

con = sqlite3.connect("books.db")
cur = con.cursor()

"""
cur_books_db.execute("CREATE TABLE books(title, author, cover_image, genre, page_count)")
cur_books_db.execute("CREATE TABLE user_books(status, notes, rating)")

"""