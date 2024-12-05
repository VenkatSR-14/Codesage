import sqlite3

# Connect to the database
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Create a users table if it doesn't exist

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
user_input_username = input("Enter your username: ")
user_input_password = input("Enter your password: ")
login(user_input_username, user_input_password)

connection.close()
