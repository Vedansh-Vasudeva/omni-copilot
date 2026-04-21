from typing import TypedDict, List, Dict, Any, Optional
import operator
from typing_extensions import Annotated
from pydantic import BaseModel

class AgentState(TypedDict):
    input: str
    chat_history: List[Dict[str, str]]
    plan: List[str]
    current_step: int
    tool_results: Annotated[List[Dict[str, Any]], operator.add]
    intermediate_steps: Annotated[List[Dict[str, Any]], operator.add]
    memory_context: str
    output: Optional[str]
    critic_feedback: Optional[str]
    status: str

# API Models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    
class AgentResponse(BaseModel):
    user_id: str
    output: str
    intermediate_steps: List[Dict[str, Any]]
