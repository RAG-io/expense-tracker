import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        
            password="",        
            database="expense_db"  
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
