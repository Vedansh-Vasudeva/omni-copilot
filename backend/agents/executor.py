import json
from agents.state import AgentState
from utils.llm_layer import llm_service
from tools.mcp_mocker import mcp_server
from typing import Dict, Any

def execute_step(state: AgentState) -> Dict[str, Any]:
    print(f"Agent: Executor (Step {state['current_step'] + 1}/{len(state['plan'])})")
    
    if state['current_step'] >= len(state['plan']):
        return {"status": "criticizing"}

    current_instruction = state['plan'][state['current_step']]
    
    available_tools = mcp_server.list_tools()
    tools_str = json.dumps(available_tools, indent=2)
    
    system_prompt = f"""You are the Executor Agent. 
Your task: {current_instruction}
Given the available tools, decide which tool to use and what arguments to pass.
If no tool is needed, respond with tool "none".
Available tools:
{tools_str}

Return EXACTLY a JSON format:
{{
  "tool": "tool_name or none",
  "args": {{ ... }}
}}
"""
    
    action = llm_service.generate_json(current_instruction, system_prompt)
    
    tool_name = action.get("tool", "none")
    tool_args = action.get("args", {})
    
    if tool_name != "none":
        print(f"  Executing tool: {tool_name}")
        result = mcp_server.execute_tool(tool_name, tool_args)
    else:
        result = llm_service.generate(f"Complete this task: {current_instruction}")
        
    step_result = {
        "agent": "executor",
        "step": current_instruction,
        "tool_used": tool_name,
        "result": str(result)
    }
    
    next_step = state['current_step'] + 1
    new_status = "executing" if next_step < len(state['plan']) else "criticizing"
    
    return {
        "current_step": next_step,
        "tool_results": [step_result],
        "intermediate_steps": [step_result],
        "status": new_status
    }
