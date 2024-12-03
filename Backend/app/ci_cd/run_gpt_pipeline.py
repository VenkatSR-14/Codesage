import requests
import os
import openai

# Environment setup
SECURITY_ENDPOINT = "http://localhost:8000/security-gpt"  # Replace with your security analysis endpoint
OPTIMIZE_ENDPOINT = "http://localhost:8000/optimize-gpt"  # Replace with your optimization endpoint
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Load OpenAI API key from environment

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

# Input code snippet for testing
CODE_SNIPPET = """
def calculate_sum(a, b):
    return a + b
"""

def check_security_vulnerabilities(code):
    """
    Calls the /security-gpt endpoint to check for security vulnerabilities.
    """
    try:
        print("Checking code for security vulnerabilities via /security-gpt...")
        response = requests.post(
            SECURITY_ENDPOINT,
            json={
                "prompt": code,
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 1.0
            }
        )
        response.raise_for_status()
        return response.json()["security_analysis"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to call /security-gpt endpoint: {e}")

def get_optimized_code(code):
    """
    Calls the /optimize-gpt endpoint with the provided code snippet.
    """
    try:
        print("Optimizing code via /optimize-gpt...")
        response = requests.post(
            OPTIMIZE_ENDPOINT,
            json={
                "prompt": code,
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 1.0
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to call /optimize-gpt endpoint: {e}")

def validate_with_gpt(message):
    """
    Validates the message (security or optimization result) with GPT.
    """
    try:
        print("Validating the result with GPT...")
        messages = [
            {"role": "system", "content": "You are a code validation assistant. Your task is to validate the result."},
            {"role": "user", "content": f"Here is the result:\n\n{message}\n\nIs this OK or NOK? Respond with 'OK' or 'NOK' only."}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=10,
            temperature=0.0,
        )
        return response.choices[0].message["content"].strip()
    except openai.error.OpenAIError as e:
        raise Exception(f"Failed to validate result with GPT: {e}")

if __name__ == "__main__":
    try:
        # Step 1: Check for security vulnerabilities
        security_analysis = check_security_vulnerabilities(CODE_SNIPPET)
        print(f"Security Analysis Result:\n{security_analysis}")

        # Validate security result
        security_validation = validate_with_gpt(security_analysis)
        print(f"Security Validation Result: {security_validation}")
        if security_validation != "OK":
            print("Security validation failed. Stopping the pipeline...")
            exit(1)  # Exit with non-zero status to fail the pipeline

        # Step 2: Optimize the code
        optimized_code = get_optimized_code(CODE_SNIPPET)
        print(f"Optimized Code:\n{optimized_code}")

        # Validate optimized code
        optimization_validation = validate_with_gpt(optimized_code)
        print(f"Optimization Validation Result: {optimization_validation}")
        if optimization_validation != "OK":
            print("Optimization validation failed. Stopping the pipeline...")
            exit(1)  # Exit with non-zero status to fail the pipeline

        # If both validations pass
        print("Both security and optimization validations passed. Proceeding with the pipeline...")

    except Exception as e:
        print(f"Pipeline execution failed: {e}")
        exit(1)
