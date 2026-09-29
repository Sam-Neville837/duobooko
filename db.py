import sqlite3
import os


file_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(file_dir, "books.db")

def get_connection():
    """
    opens and returns a fresh connection to the SQLite database
    """
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row

    return con