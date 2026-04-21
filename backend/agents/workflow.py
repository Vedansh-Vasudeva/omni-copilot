from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.planner import plan_task
from agents.executor import execute_step
from agents.memory import retrieve_memory, save_memory
from agents.critic import criticize_results

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("memory", retrieve_memory)
workflow.add_node("planner", plan_task)
workflow.add_node("executor", execute_step)
workflow.add_node("critic", criticize_results)
workflow.add_node("save_memory", save_memory)

# Define edges
workflow.set_entry_point("memory")
workflow.add_edge("memory", "planner")
workflow.add_edge("planner", "executor")

# Conditional edge for executor (loops until all steps are done)
def executor_router(state: AgentState):
    if state["status"] == "criticizing":
        return "critic"
    return "executor"

workflow.add_conditional_edges(
    "executor",
    executor_router,
    {"executor": "executor", "critic": "critic"}
)

workflow.add_edge("critic", "save_memory")
workflow.add_edge("save_memory", END)

# Compile graph
app = workflow.compile()
