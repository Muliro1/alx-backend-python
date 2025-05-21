#!/usr/bin/python3

import sqlite3
from functools import wraps

#### decorator to lof SQL queries


def log_queries(func):
    @wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper

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