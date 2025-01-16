#!/usr/bin/env python
from langtrace_python_sdk import langtrace
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import warnings
from crew import BloggerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ignore specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Initialize langtrace
langtrace.init(
    api_key=os.getenv("LANGTRACE_API_KEY"),
)

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Replace "*" with your frontend's URL in production, e.g., ["http://localhost:3000"]
    allow_origins=["http://localhost:3000",
                   "https://www.learnaiwithus.codes"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class BlogRequest(BaseModel):
    topic: str


@app.post("/generate_blog/")
async def generate_blog(request: BlogRequest):
    """
    Generate a blog based on the input topic.
    """
    try:
        inputs = {'topic': request.topic}
        logger.info(f"Received request with inputs: {inputs}")
        res = BloggerAgent().crew().kickoff(inputs=inputs)
        logger.info(f"Received response: {res}")
        return {"result": res}
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error generating blog: {str(e)}")