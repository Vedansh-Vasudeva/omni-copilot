from agents.state import AgentState
from utils.llm_layer import llm_service
from typing import Dict, Any

def plan_task(state: AgentState) -> Dict[str, Any]:
    print("Agent: Planner")
    system_prompt = """You are the Planner Agent. 
Break down the user's input into a precise, step-by-step array of instructions.
If the task is simple, make it 1-2 steps. Use available tools implicitly in steps.
Return ONLY a JSON array of strings."""

    context_str = f"User Request: {state['input']}\nMemory Context: {state.get('memory_context', 'None')}"
    
    plan_data = llm_service.generate_json(context_str, system_prompt)
    if isinstance(plan_data, list):
        plan = plan_data
    else:
        plan = [state['input']] # fallback
        
    return {
        "plan": plan,
        "current_step": 0,
        "status": "executing",
        "intermediate_steps": [{"agent": "planner", "action": "created_plan", "result": plan}]
    }
