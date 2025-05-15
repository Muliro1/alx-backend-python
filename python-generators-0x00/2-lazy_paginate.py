import mysql.connector

seed = __import__('seed')

def paginate_users(page_size, offset):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum",
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
