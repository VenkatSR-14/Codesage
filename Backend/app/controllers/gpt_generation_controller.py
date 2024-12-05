from fastapi import APIRouter, HTTPException
from app.Services.gpt_services import generate_optimized_code, analyze_code_security, generate_code_review_analysis
from app.models.gpt_request_models import GPTRequest
from datasets import Dataset, load_dataset
import pandas as pd

#loading datasets
security_dataset = load_dataset("CyberNative/Code_Vulnerability_Security_DPO")
code_optimization_dataset=  load_dataset("Dahoas/code-review-instruct-critique-revision-python")
code_review_dataset = pd.read_csv("dataset/code_review_data.csv")


router = APIRouter(
    prefix="/generate",
    tags=["GPT Generation"]
)

@router.post("/optimize-gpt")
async def optimize_code_gpt(request: GPTRequest):
    """
    Endpoint to generate optimized code using GPT.
    """
    try:
        response = generate_optimized_code(
            dataset=code_optimization_dataset,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            num_examples=5,  # Add an appropriate default or dynamic value
        )
        return {"prompt": request.prompt, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing code: {str(e)}")

@router.post("/security-gpt")
async def security_analysis_gpt(request: GPTRequest):
    """
    Endpoint to analyze code security using GPT.
    """
    try:
        response = analyze_code_security(
            dataset=security_dataset['train'],
            code=request.prompt,  # Correct parameter name
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        return {"prompt": request.prompt, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing security: {str(e)}")

@router.post("/code-refractoring-gpt")
async def code_review_analysis(request: GPTRequest):
    """
    Endpoint to analyze a code diff for review comments.
    """
    try:
        # Generate response using service logic
        response = generate_code_review_analysis(
            code_diff=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        return {"prompt": request.prompt, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code review analysis: {str(e)}")