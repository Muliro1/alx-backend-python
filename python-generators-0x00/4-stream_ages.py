#!/usr/bin/python3

import mysql.connector

def stream_user_ages():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum",
            database="ALX_prodev"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield float(row[0])
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    compute_average_age()