#!/usr/bin/env python3

import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Create connection and cursor when entering the context
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters if provided
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)
            
        # Fetch all results
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close cursor and connection when exiting the context
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Using the context manager to execute a query with parameters
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery(query, params) as results:
        # Print the results
        for row in results:
            print(row)