from fastapi import FastAPI
from app.controllers import gpt_generation_controller

# Initialize FastAPI app
app = FastAPI(
    title="GPT Code Analysis API",
    description="An API to optimize code and analyze code security using OpenAI's GPT-3.5",
    version="1.0.0"
)

# Include routers
app.include_router(gpt_generation_controller.router)

# Root endpoint for health check
@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the GPT Code Analysis API. Visit /docs for API documentation."}

# Add any global middleware (if required)
# Example: CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Optional: Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    """
    print("Starting up the API...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    print("Shutting down the API...")
