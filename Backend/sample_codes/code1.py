import sqlite3
import bcrypt  # Install this package with `pip install bcrypt`

# Connect to the database
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Create a users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
connection.commit()

# Function to add a new user securely
def register_user(username, password):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")

# Function to simulate user login securely
def login(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Example usage
while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        register_user(username, password)
    elif choice == '2':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        login(username, password)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
connection.close()
