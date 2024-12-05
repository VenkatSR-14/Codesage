import requests
import os
import openai
import chardet

print("Running validation pipeline...")

# Environment setup
SECURITY_ENDPOINT = "http://localhost:8000/generate/security-gpt"
OPTIMIZE_ENDPOINT = "http://localhost:8000/generate/optimize-gpt"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API key
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set. Ensure it is stored as an environment variable or secret.")

openai.api_key = OPENAI_API_KEY

def detect_file_encoding(file_path):
    """
    Detects the encoding of the file.
    """
    with open(file_path, "rb") as file:
        raw_data = file.read(1000)  # Read a portion of the file
        result = chardet.detect(raw_data)
        return result.get("encoding", "utf-8")  # Default to utf-8 if detection fails

def get_modified_files(file_path="modified_files.txt"):
    """
    Reads the list of modified files from 'modified_files.txt', detects encoding, and ensures valid file paths.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found. Ensure it exists and contains file paths.")

    # Detect encoding of the file
    encoding = detect_file_encoding(file_path)
    print(f"Detected encoding for '{file_path}': {encoding}")

    # Read the file using the detected encoding
    with open(file_path, "r", encoding=encoding) as file:
        files = [line.strip() for line in file.readlines()]  # Remove newline and extra spaces

    # Filter out invalid or non-existent files
    valid_files = [f for f in files if f and os.path.isfile(f)]
    if not valid_files:
        raise Exception(f"No valid files found in '{file_path}'. Check the content and paths.")

    return valid_files

def read_file_contents(file_path):
    """
    Reads the contents of a file and returns it as a string.
    Automatically detects the file's encoding.
    """
    try:
        encoding = detect_file_encoding(file_path)
        print(f"Detected encoding for {file_path}: {encoding}")
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")

def post_request(endpoint, payload):
    """
    Sends a POST request to the given endpoint with the provided payload.
    """
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to call {endpoint}: {e}")

def validate_with_gpt(message):
    """
    Validates the message (security or optimization result) with GPT.
    """
    try:
        messages = [
            {"role": "system", "content": "You are a code validation assistant. Validate the result."},
            {"role": "user", "content": f"Here is the result:\n\n{message}\n\nRespond with 'OK' or 'NOK' only."}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=10,
            temperature=0.0,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        raise Exception(f"Failed to validate result with GPT: {e}")

def process_file(file_path):
    """
    Processes a single file: checks for vulnerabilities, optimizes code, and validates both steps.
    """
    print(f"\nProcessing file: {file_path}")

    # Step 1: Read the file contents
    code_snippet = read_file_contents(file_path)

    # Step 2: Run security analysis
    print(f"Running security analysis for {file_path}...")
    security_result = post_request(
        SECURITY_ENDPOINT,
        {"prompt": code_snippet, "max_tokens": 1500, "temperature": 0.7, "top_p": 1.0}
    )
    print(f"Security Analysis Result for {file_path}:\n{security_result}")

    # Step 3: Validate security result
    validation_result = validate_with_gpt(security_result)
    print(f"Security Validation Result: {validation_result}")
    if validation_result != "OK":
        raise Exception(f"Security validation failed for {file_path}.")

    # Step 4: Optimize code
    print(f"Running code optimization for {file_path}...")
    optimized_result = post_request(
        OPTIMIZE_ENDPOINT,
        {"prompt": code_snippet, "max_tokens": 1500, "temperature": 0.7, "top_p": 1.0}
    )
    print(f"Optimized Code for {file_path}:\n{optimized_result}")

    # Step 5: Validate optimized code
    validation_result = validate_with_gpt(optimized_result)
    print(f"Optimization Validation Result: {validation_result}")
    if validation_result != "OK":
        raise Exception(f"Optimization validation failed for {file_path}.")

    print(f"File {file_path} passed both security and optimization checks.\n")

if __name__ == "__main__":
    try:
        # Step 1: Get the list of modified files
        modified_files = get_modified_files()
        if not modified_files:
            print("No modified files to process.")
            exit(0)

        print(f"Modified files: {modified_files}")

        # Step 2: Process each file
        for file_path in modified_files:
            process_file(file_path)

        print("All modified files passed security and optimization validations.")

    except Exception as e:
        print(f"Pipeline execution failed: {e}")
        exit(1)
