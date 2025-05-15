import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="muliro",
            password="nihilpraeteroptimum",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, csv_file):
    """Insert data from CSV file into user_data table"""
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            cursor = connection.cursor()
            
            # Skip header row
            next(csv_reader)
            
            for row_num, row in enumerate(csv_reader, start=2):  # start=2 because we skipped header
                try:
                    # Debug print
                    print(f"Processing row {row_num}: {row}")
                    
                    # Remove quotes from each field
                    cleaned_row = [field.strip('"') for field in row]
                    
                    # Check if record already exists
                    cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (cleaned_row[1],))
                    if not cursor.fetchone():
                        # Generate UUID for new record
                        user_id = str(uuid.uuid4())
                        
                        # Handle age value
                        try:
                            # Remove any non-numeric characters and convert to int
                            age_str = ''.join(filter(str.isdigit, str(cleaned_row[2])))
                            if not age_str:
                                age = 0  # Default value if no digits found
                            else:
                                age = int(age_str)
                        except (ValueError, TypeError):
                            age = 0  # Default value if conversion fails
                        
                        cursor.execute("""
                            INSERT INTO user_data (user_id, name, email, age)
                            VALUES (%s, %s, %s, %s)
                        """, (user_id, cleaned_row[0], cleaned_row[1], age))
                        connection.commit()
                        print(f"Successfully inserted row {row_num}")
                        
                except IndexError as e:
                    print(f"Error in row {row_num}: {row}")
                    print(f"IndexError: {e}")
                    continue  # Skip this row and continue with next
                except Exception as e:
                    print(f"Error processing row {row_num}: {e}")
                    continue  # Skip this row and continue with next
            
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found")
    except Exception as e:
        print(f"Unexpected error: {e}")