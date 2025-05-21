#!/usr/bin/python3

import sqlite3
from functools import wraps
from datetime import datetime

#### decorator to lof SQL queries


def log_queries(func):
    @wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"[{datetime.now()}] SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper
# Create the users table if it doesn't exist
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
# Optionally insert a sample user if table is empty
cursor.execute('SELECT COUNT(*) FROM users')
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
conn.commit()
conn.close()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")