import mysql.connector

def stream_users():
    """Generator function that streams users one by one from the database"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum",
            database="ALX_prodev"
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        # Yield one row at a time
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

'''if __name__ == "__main__":
    for user in stream_users():
        print(user)'''