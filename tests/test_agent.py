import pytest
import asyncio # Keep asyncio for now, might be needed by ADK internally, but not for this test directly
import sys
sys.path.append('.') # Add the project root to the Python path for module discovery
from example_agent.agent import get_current_time

def test_get_current_time():
    """
    Test the get_current_time tool.
    """
    result = get_current_time()
    assert result["status"] == "success"
    assert "The current time is" in result["report"]