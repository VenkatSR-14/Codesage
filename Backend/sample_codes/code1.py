import os

def list_directory_contents(directory):
    """
    Securely lists the contents of a directory.
    """
    try:
        # Use os.listdir() to avoid command injection
        contents = os.listdir(directory)
        print(f"Contents of {directory}:")
        for item in contents:
            print(item)
    except FileNotFoundError:
        print("Directory not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory to list: ")
    list_directory_contents(directory)
