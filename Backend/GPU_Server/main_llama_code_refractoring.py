from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from __main__ import llama_model_patch, tokenizer_llama  # Use the preloaded model and tokenizer
import re
import torch

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Helper function to clean up responses
def clean_response(response):
    """
    Removes unwanted HTML tags and trims extra spaces.
    """
    cleaned_response = re.sub(r"<[^>]+>", "", response)  # Remove HTML tags
    return cleaned_response.strip()

# Helper function to format the prompt
def format_prompt(code):
    """
    Formats the prompt with a fixed task and instructions, adding context and code.
    """
    formatted_string = f"""
    ### Code Review Task:
    Review the provided code diff and provide constructive feedback. If necessary, identify what the `[ADD]` sections introduce and what the `[DEL]` sections lacked or addressed. If there are no issues, write: "Everything is fine, LGTM."

    ### Code Diff:
    {code}    

    ### Feedback and Suggestions (Response):

    """
    return formatted_string

# Helper function to generate a response
def generate_response(prompt, model, max_new_tokens=512, temperature=0.2, top_p=0.9, repetition_penalty=1.2):
    """
    Generates a response from the preloaded model.
    """
    try:
        # Tokenize the input prompt with explicit `text`
        
        inputs = tokenizer_llama(text=prompt, return_tensors="pt").to("cuda")

        # Generate the response
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            repetition_penalty=repetition_penalty,
            eos_token_id=tokenizer_llama.eos_token_id,
        )

        # Decode and clean the response
        generated_text = tokenizer_llama.decode(outputs[0], skip_special_tokens=True)
        response = generated_text[len(prompt):].strip()
        return clean_response(response)
    except Exception as e:
        raise ValueError(f"Error during response generation: {e}")

# Define request model
class InferenceRequest(BaseModel):
    code: str
    max_new_tokens: int = 512
    temperature: float = 0.2
    top_p: float = 0.9
    repetition_penalty: float = 1.2

# Define FastAPI endpoints
@app.post("/generate/code-refractoring-llama")
def optimization_llama(request: InferenceRequest):
    """
    Endpoint for optimization tasks using llama.
    """
    try:
        # Format the zero-shot prompt
        zero_shot_prompt = format_prompt(request.code)
        print(zero_shot_prompt)
        # Generate the response using the model
        response = generate_response(
            model=llama_model_patch,
            prompt=zero_shot_prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            repetition_penalty=request.repetition_penalty,
        )

        return {"prompt": zero_shot_prompt, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# Test Endpoint (Optional)
@app.get("/")
def read_root():
    return {"message": "llama Inference API is running."}
