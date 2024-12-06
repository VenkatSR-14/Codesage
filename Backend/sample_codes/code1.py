# Basic user storage
users = []

# Register a user
def register_user(username):
    if username in users:
        print("Username already exists.")
    else:
        users.append(username)
        print("User registered successfully!")

# Login a user
def login(username):
    if username in users:
        print("Login successful!")
    else:
        print("Username not found.")

# Example usage
register_user("Alice")
register_user("Bob")
login("Alice")  # Login successful!
login("Charlie")  # Username not found.
