from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.state import ChatRequest, AgentResponse
from agents.workflow import app as agent_workflow

import os
import uvicorn

app = FastAPI(title="Omni-Copilot API")

# Add CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=AgentResponse)
async def chat_endpoint(request: ChatRequest):
    initial_state = {
        "input": request.message,
        "chat_history": [],
        "plan": [],
        "current_step": 0,
        "tool_results": [],
        "intermediate_steps": [],
        "memory_context": "",
        "output": None,
        "critic_feedback": None,
        "status": "init"
    }

    try:
        # Run langgraph
        result = agent_workflow.invoke(initial_state)
        
        return AgentResponse(
            user_id=request.user_id,
            output=result["output"] or "No output generated.",
            intermediate_steps=result.get("intermediate_steps", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
