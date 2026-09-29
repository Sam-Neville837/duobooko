import sqlite3
from db import get_connection

def get_all_books():
    """
    returns all the books saved
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    SELECT id, title, author, cover_image, genre, page_count
    FROM books
    """)

    results = cur.fetchall()

    con.close()
    return results

def add_book(title, author, genre, page_count, cover_image=None):
    """
    adds a new book to the catalog
    """

    title = title.title()
    author = author.title()
    genre = genre.title()

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO books (title, author, genre, page_count, cover_image) VALUES (?, ?, ?, ?, ?)",
        (title, author, genre, page_count, cover_image)
    )

    con.commit()
    con.close()

def get_book_by_id(book_id):
    """
    returns a single book by its id
    """

    if type(book_id) is not int:
        raise TypeError(f"{book_id} is not an integer")

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT title, author, cover_image, genre, page_count
        FROM books
        WHERE id = ?
        
    """, (book_id, ))

    results = cur.fetchone()
    con.close()

    if results is None:
        raise ValueError(f"{book_id} does not exist")
    
    return results

def get_book_id(title, author):
    """
    takes a name and author and finds the book(s), and returns the id(s)
    if multiple books have the same author/name raises an error (not return None)
    """

    title = title.title()
    author = author.title()

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT id FROM books WHERE title = ? AND author = ?",
    (title, author))

    results = cur.fetchall()
    con.close()

    if len(results) == 0:
        raise ValueError(f"No book {title} by {author} saved")

    elif len(results) > 1:
        raise ValueError(f"Multiple books named {title} by {author} found")

    results = results[0][0]
    return results

def get_books_by_author(author):
    """
    returns all books written by a specific author
    """

    author = author.title()

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT title FROM books WHERE author = ?",
    (author,))

    results = cur.fetchall()
    con.close()

    return results

def get_books_by_genre(genre):
    """
    returns all books in a specific genre
    """

    genre = genre.title()

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT title, author FROM books WHERE genre = ?",
    (genre, ))

    results = cur.fetchall()
    con.close()

    return results
