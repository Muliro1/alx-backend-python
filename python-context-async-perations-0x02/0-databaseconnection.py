# usr/bin/env python3

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Create connection and cursor when entering the context
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close cursor and connection when exiting the context
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Using the context manager to execute a query
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        # Print the results
        for row in results:
            print(row)