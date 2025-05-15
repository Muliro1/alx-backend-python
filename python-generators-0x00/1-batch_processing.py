import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if float(user['age']) > 25]
        if filtered:
            yield filtered