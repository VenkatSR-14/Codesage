import os
import openai
from dotenv import load_dotenv

# Load environment variables and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file")

# Function to detect language
def detect_language(code):
    """
    Detects the programming language of the provided code using GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code language detection assistant."},
                {"role": "user", "content": f"Identify the programming language of the following code:\n\n{code}\n\nJust provide the language name, nothing else."}
            ],
            max_tokens=10,
            temperature=0,
        )
        result = response.choices[0].message['content'].strip()
        print(f"Detected language: {result}")
        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error detecting language"


# Test cases
if __name__ == "__main__":
    test_cases = [
        {
            "code": "def hello_world():\n    print('Hello, World!')",
            "expected_language": "Python"
        },
        {
            "code": "#include <iostream>\nusing namespace std;\nint main() {\n    cout << 'Hello, World!' << endl;\n    return 0;\n}",
            "expected_language": "C++"
        },
        {
            "code": "console.log('Hello, World!');",
            "expected_language": "JavaScript"
        },
        {
            "code": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println('Hello, World!');\n    }\n}",
            "expected_language": "Java"
        },
        {
            "code": "print 'Hello, World!'",
            "expected_language": "Python"  # Older version (Python 2 syntax)
        },
    ]

    for idx, test in enumerate(test_cases, start=1):
        print(f"\nTest Case {idx}:")
        print(f"Code:\n{test['code']}")
        detected_language = detect_language(test['code'])
        print(f"Expected Language: {test['expected_language']}")
        print(f"Detected Language: {detected_language}")
        print("Result:", "PASS" if detected_language.lower() == test['expected_language'].lower() else "FAIL")
