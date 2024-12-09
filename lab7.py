import mysql.connector
from mysql.connector import Error
import getpass

db_password = getpass.getpass("Enter your database password: ")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql.labthreesixfive.com",  
            user="amoren77",          
            password=db_password,
            database="amoren77"      
        )
        if connection.is_connected():
            print("Connection successful!")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


