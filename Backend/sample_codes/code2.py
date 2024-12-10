import os

def list_directory_contents(directory):
    try:
        base_dir = os.path.abspath("safe_directory")
        directory_path = os.path.abspath(os.path.join(base_dir, directory))

        if not directory_path.startswith(base_dir):
            print("Unauthorized access attempt detected.")
            return

        contents = os.listdir(directory_path)
        print(f"Contents of {directory_path}:")
        for item in contents:
            print(item)
    except FileNotFoundError:
        print("Directory not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory to list: ")
    list_directory_contents(directory)
