"""
database.py

Contains important database utilities.

:author Sam Kuzio
"""

import sqlite3


# Keep a single database connection. Use get_db_connection(), do not access the variable directly.
conn = None

# Database file path
DATABASE = 'diddlebot.db'


def get_conn():
    """
    :return: The current database connection, creating a new one if there is no existing connection.
    """
    global conn

    if conn is None:
        conn = sqlite3.connect(DATABASE)

    return conn
