from agents.state import AgentState
from memory_layer.chroma_db import semantic_memory
from memory_layer.mem0_client import user_memory
from memory_layer.knowledge_graph import knowledge_graph
from typing import Dict, Any

def retrieve_memory(state: AgentState) -> Dict[str, Any]:
    print("Agent: Memory")
    # Identify user id (mocked as 'default_user' for now, could be passed in input)
    user_id = "default_user"
    query = state['input']
    
    # 1. Fetch from Chroma
    chroma_res = ""
    try:
        chroma_res = semantic_memory.query_memories(query)
    except Exception as e:
        chroma_res = f"Semantic Mem Error: {e}"
        
    # 2. Fetch from Mem0
    mem0_res = ""
    try:
        mem0_res = user_memory.get_context(user_id, query)
    except Exception as e:
        mem0_res = f"Mem0 Error: {e}"
        
    # 3. Fetch from KG (simplified string matching)
    kg_res = ""
    try:
        words = query.split()
        for w in words:
            relations = knowledge_graph.get_relations(w)
            if relations:
                kg_res += f"KG Links for {w}: {relations}\n"
    except Exception as e:
        kg_res = f"KG Error: {e}"
            
    context = f"Semantic: {chroma_res}\nUser Mem: {mem0_res}\nGraph: {kg_res}"
    
    return {
        "memory_context": context,
        "status": "planning",
        "intermediate_steps": [{"agent": "memory", "action": "retrieved_context", "result": context}]
    }
    
def save_memory(state: AgentState) -> Dict[str, Any]:
    # Saving final output to memory
    print("Agent: Memory (Saving)")
    user_id = "default_user"
    if state.get("output"):
        try:
            user_memory.add_interaction(user_id, f"User: {state['input']}\nBot: {state['output']}")
            semantic_memory.add_memory(str(hash(state['input'])), state['output'], {"type": "conversation"})
        except Exception as e:
            print(f"Memory Save Error: {e}")
        
    return {}
