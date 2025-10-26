# db_setup.py
import sqlite3


def create_database():
    conn = sqlite3.connect('eye.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
                        id INTEGER PRIMARY KEY ,
                        name TEXT NOT NULL,
                        birthday TEXT NOT NULL,
                        job TEXT NOT NULL,
                        image BLOB NOT NULL 
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        immatriculation TEXT UNIQUE,
                        name TEXT NOT NULL,
                        major TEXT NOT NULL,
                        image BLOB NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
                        id INTEGER PRIMARY KEY,
                        immatriculation TEXT UNIQUE,
                        name TEXT NOT NULL,
                        departement TEXT NOT NULL,
                         image BLOB NOT NULL
                    )''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
# Call the function to create the database and tables
create_database()
