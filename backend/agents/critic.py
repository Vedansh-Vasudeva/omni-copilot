from agents.state import AgentState
from utils.llm_layer import llm_service
from typing import Dict, Any

def criticize_results(state: AgentState) -> Dict[str, Any]:
    print("Agent: Critic")
    
    results = "\n".join([f"Step: {r.get('step')}\nResult: {r.get('result')}" for r in state.get('tool_results', [])])
    
    system_prompt = """You are the Critic Agent.
Review the user's initial request and the execution results.
If the results satisfy the request, generate a final concise response to the user.
If they DO NOT satisfy the request, explain what failed and suggest requesting a re-plan.
Respond with JSON:
{
  "passed": true/false,
  "final_output": "The response to the user",
  "feedback": "Internal feedback if failed"
}
"""
    prompt = f"User Request: {state['input']}\nExecution Results:\n{results}"
    
    evaluation = llm_service.generate_json(prompt, system_prompt)
    
    passed = evaluation.get("passed", True)
    final_output = evaluation.get("final_output", "Failed to generate proper output.")
    
    if passed:
        return {
            "status": "done",
            "output": final_output,
            "intermediate_steps": [{"agent": "critic", "action": "approved", "result": final_output}]
        }
    else:
        # In a more complex loop, we would loop back to planner. 
        # For simplicity MVP, we just fail gracefully.
        return {
            "status": "failed",
            "output": f"Task Failed. Feedback: {evaluation.get('feedback')}",
            "intermediate_steps": [{"agent": "critic", "action": "rejected", "result": evaluation.get('feedback')}]
        }
