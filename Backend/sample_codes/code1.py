import os

def delete_file(filename):
    """
    Deletes a file based on user-provided input.
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print("File deleted successfully.")
        else:
            print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    filename = input("Enter the name of the file to delete: ")
    delete_file(filename)
