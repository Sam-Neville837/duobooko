import sqlite3
from db import get_connection
import books_queries

def get_reading_log():
    """
    returns every entry in the user's reading log
    joined with the data from books
    """

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            user_books.id,
            books.title,
            books.author,
            user_books.status,
            user_books.rating,
            user_books.notes
        FROM user_books
        JOIN books ON user_books.book_id = books.id

    """)

    results = cur.fetchall()
    con.close()

    print('done')
    return results

def log_book_read(title, author, status='Finished', rating=None, notes=None):
    """
    logs an existing book in the books catalog as read
    """

    title = title.title()
    author = author.title()
    status = status.title()

    con = get_connection()
    cur = con.cursor()

    catalog_id = books_queries.get_book_id(title, author)

    cur.execute(
        "INSERT INTO user_books (book_id, status, rating, notes) VALUES (?, ?, ?, ?)",
        (catalog_id, status, rating, notes)
    )

    con.commit()
    con.close()
    print('done')

def update_reading_log_entry(entry_id, status=None, rating=None, notes=None):
    """
    change data about an existing entry
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT status, notes, rating FROM user_books
        WHERE id = ?
    """, (entry_id, )
    )
    row = cur.fetchone()

    if row is None:
        raise ValueError(f"No log entry with id {entry_id}")

    curr_status, curr_notes, curr_rating = row

    if status is not None:
        curr_status = status.title()

    if rating is not None:
        curr_rating = rating

    if notes is not None:
        curr_notes = notes

    cur.execute(
        "UPDATE user_books SET status = ?, rating = ?, notes = ? WHERE id = ?",
        (curr_status, curr_rating, curr_notes, entry_id)
    )
    con.commit()
    con.close()

def delete_reading_log_entry(entry_id):
    """
    deletes a specific entry by its id
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM user_books WHERE id = ?", (entry_id, ))

    con.commit()
    con.close()

def get_log_entry_by_id(entry_id):
    """
    fetch a specific logged item by user_books id
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT title, author, status, rating, notes 
        FROM user_books
        JOIN books ON user_books.book_id = books.id
        WHERE user_books.id = ?
        """, (entry_id, ))

    results = cur.fetchone()
    con.close()

    if results is None:
        raise ValueError(f"{entry_id} not in user_books")

    return results

def get_books_by_rating(rating):
    """
    get all books of a specified rating
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    SELECT title, author
    FROM user_books
    JOIN books ON user_books.book_id = books.id
    WHERE rating = ?
    """, (rating, ))

    results = cur.fetchall()

    con.close()
    return results