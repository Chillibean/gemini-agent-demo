import os
import sys
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv

# Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Create the FastAPI app using ADK's helper
app: FastAPI = get_fast_api_app(
    agents_dir=BASE_DIR,
    allow_origins=["*"],  # In production, restrict this
    web=True,  # Enable the ADK Web UI
)

# Add custom endpoints (optional, but good for health checks)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# This endpoint is for demonstration and requires importing the agent
from example_agent import root_agent
@app.get("/agent-info")
async def agent_info():
    """Provide agent information"""
    return {
        "agent_name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model,
        "tools": [t.__name__ for t in root_agent.tools]
    }

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=4000,
        reload=False
    )