import os
from dotenv import load_dotenv
import openai

# Load environment variables and initialize the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Validate the API key
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file")