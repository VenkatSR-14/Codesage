from pydantic import BaseModel

class GPTRequest(BaseModel):
    """
    Request model for GPT-based operations.
    """
    prompt: str
    max_tokens: int = 500
    temperature: float = 0.7
    top_p: float = 0.9
