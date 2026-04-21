import os
import requests
from tools.mcp_mocker import mcp_server

def file_read(filepath: str) -> str:
    """Read a file from disk"""
    try:
        # Prevent absolute paths out of workspace naturally if needed
        # For MVP, just reading existing files
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

def simple_api_call(url: str, method: str = "GET") -> str:
    """Make a simple API call"""
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url)
        return response.text
    except Exception as e:
        return str(e)

def python_execution(code: str) -> str:
    """Execute Python code and capture output (UNSAFE FOR PROD, MVP ONLY)"""
    import io
    import sys
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        exec(code, {})
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return str(e)

# Register tools mapped in MCP
mcp_server.register_tool("file_read", "Read local file explicitly by filepath", file_read)
mcp_server.register_tool("simple_api_call", "Call a simple REST API (mock OAuth if needed)", simple_api_call)
mcp_server.register_tool("python_execution", "Run python code and get output string", python_execution)
