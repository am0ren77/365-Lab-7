import mysql.connector
from mysql.connector import Error
import pandas as pd
import getpass  # For secure password input

# Database connection details
db_config = {
    "host": "mysql.labthreesixfive.com",
    "user": "amoren77",
    "password": getpass.getpass("Enter your database password: "),
    "database": "amoren77"
}

def create_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Connection successful!")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def fetch_rooms_and_rates(conn):
    """Handles FR1: Rooms and Rates."""
    query = """
    SELECT 
        r.RoomCode,
        r.RoomName,
        r.Beds,
        r.bedType,
        r.maxOcc,
        r.basePrice,
        r.decor,
        ROUND(SUM(
            CASE 
                WHEN res.CheckOut >= CURDATE() - INTERVAL 180 DAY THEN DATEDIFF(LEAST(res.CheckOut, CURDATE()), GREATEST(res.CheckIn, CURDATE() - INTERVAL 180 DAY)) 
                ELSE 0 
            END
        ) / 180, 2) AS PopularityScore,
        MIN(CASE WHEN res.CheckOut < CURDATE() THEN res.CheckOut END) AS NextAvailableCheckInDate,
        MAX(CASE WHEN res.CheckOut < CURDATE() THEN DATEDIFF(res.CheckOut, res.CheckIn) END) AS MostRecentStayLength,
        MAX(CASE WHEN res.CheckOut < CURDATE() THEN res.CheckOut END) AS MostRecentCheckOutDate
    FROM 
        lab7_rooms r
    LEFT JOIN 
        lab7_reservations res ON r.RoomCode = res.Room
    GROUP BY 
        r.RoomCode
    ORDER BY 
        PopularityScore DESC;
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            print("\n=== Rooms and Rates (Sorted by Popularity) ===\n")
            df = pd.DataFrame(results)
            print(df.to_string(index=False))
        else:
            print("No data found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def main_menu():
    """Displays the main menu and handles user input."""
    print("\nMain Menu")
    print("[1] Rooms and Rates")
    print("[2] Book Reservations")
    print("[3] Change Reservations")
    print("[4] Cancel Reservations")
    print("[5] Revenue Summary")
    print("[M] Main Menu")
    print("[0] Exit\n")

def option_select():
    """Handles user input for menu selection."""
    conn = create_connection()
    if not conn:
        print("Could not connect to the database. Exiting...")
        return

    main_menu()
    while True:
        option_selected = input("Input Command: ").strip().lower()

        if option_selected == "1":
            print("\n[1] Rooms and Rates")
            fetch_rooms_and_rates(conn)
        elif option_selected == "2":
            print("\n[2] Book Reservations")
            # FR2 function
        elif option_selected == "3":
            print("\n[3] Change Reservations")
            # FR3 function
        elif option_selected == "4":
            print("\n[4] Cancel Reservations")
            # FR4 function
        elif option_selected == "5":
            print("\n[5] Revenue Summary")
            # FR5 function
        elif option_selected == "m":
            print("\n[M] Main Menu")
            main_menu()
        elif option_selected == "0":
            print("\nExiting... Goodbye!")
            conn.close()
            break
        else:
            print("\nInvalid command. Please try again.")

if __name__ == "__main__":
    option_select()





