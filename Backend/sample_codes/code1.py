import sqlite3
import numpy as np
# Connect to the database
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Create a users table if it doesn't exist
cursor.execute(`
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
`)
connection.commit()

# Simulate user login
def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing query:", query)  # For debugging purposes
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Input from the user

connection.close()
