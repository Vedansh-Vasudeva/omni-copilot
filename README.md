# Omni-Copilot MVP

Omni-Copilot is an agentic AI system designed to understand complex user tasks, break them into multi-step execution plans, leverage tools/APIs, and maintain persistent memory across sessions. Built with strict adherence to modularity and separation of concerns.

---

## 1. High-Level Architecture

### Components
1. **Agent Orchestration (LangGraph)**: The core engine that routes state between the agents. Stateful execution allows loops (like the `Executor` calling tools iteratively) and condition branching (passing to the `Critic`).
2. **LLM Abstraction Layer (`llm_layer.py`)**: A wrapper around `litellm` that provides model-agnostic generation and structured JSON enforcement. Allows easy swapping between GPT-4, Claude, or local LLMs.
3. **Multi-Agent System**:
   - **Planner Agent**: Deconstructs user inputs and memory context into an actionable JSON array of step-by-step instructions.
   - **Executor Agent**: In a loop, evaluates the current step, maps it to available tools in the MCP layer, executes the tool, and saves results to intermediate state.
   - **Memory Agent**: Retrieves contextual and historical data via semantic queries and graph relations before planning. Saves final outputs back into memory post-execution.
   - **Critic Agent**: After execution finishes, evaluates the intermediate results against the original user input. Generates the final user-facing response or handles failures.
4. **Memory Subsystems**:
   - **ChromaDB**: Handles dense semantic embeddings of user conversations and artifacts.
   - **Mem0**: Extracts high-level user context and preferences autonomously.
   - **NetworkX**: Provides deterministic, traversable relations between concepts using a lightweight JSON-backed graph.
5. **Tool Layer (MCP Mocker)**: Simulates the Model Context Protocol (MCP) by maintaining a registry of tools. Includes local file IO, API fetchers, and isolated python execution.
6. **Frontend**: A React SPA that visualizes not just the conversation but also the internal reasoning traces and tool outputs of each Agent asynchronously.

### Data Flow
`User Input → Memory Retrieval (Chroma+Mem0+KG) → Planner (Steps breakdown) → Executor (Tool looping) → Critic (Validation & Synthesis) → Memory Save → Frontend Output`

---

## 2. Folder Structure

```
Omni-Copilot/
│
├── backend/
│   ├── main.py                  # FastAPI Entrypoint
│   ├── requirements.txt         # Python Dependencies
│   ├── .env.example             # Environment config template
│   │
│   ├── core/
│   │   └── config.py            # Pydantic Settings implementation
│   │
│   ├── agents/
│   │   ├── workflow.py          # LangGraph StateGraph orchestration
│   │   ├── state.py             # Agent TypedDict state and API schemas
│   │   ├── planner.py           # Planner Agent logic
│   │   ├── executor.py          # Executor Agent logic
│   │   ├── memory.py            # Memory Agent (Retrieval & Saving)
│   │   └── critic.py            # Critic Agent validation
│   │
│   ├── memory_layer/
│   │   ├── chroma_db.py         # Semantic Vector DB
│   │   ├── mem0_client.py       # Mem0 User context DB
│   │   └── knowledge_graph.py   # NetworkX Graph memory
│   │
│   ├── tools/
│   │   ├── mcp_mocker.py        # Model Context Protocol abstraction
│   │   └── actions.py           # Tool primitives (file read, python execution, api call)
│   │
│   └── utils/
│       └── llm_layer.py         # litellm abstraction layer
│
└── frontend/
    ├── package.json             # NPM dependencies
    ├── vite.config.js           # Vite build tool config
    ├── index.html               # React entry HTML
    └── src/
        ├── main.jsx             # React DOM bindings
        ├── App.jsx              # Main React App layout
        ├── App.css              # Styling system (Vibrant & dynamic aesthetics)
        └── components/
            ├── ChatInterface.jsx# Main user interface chat logic
            └── AgentStep.jsx    # Visualizes intermediate LangGraph steps
```

---

## 3. Example Workflow

**User Input:** "Read my python data file, analyze the metrics, and update my memory that I prefer summary statistics."

1. **Memory Agent (Start):** Retrieves past info about what "python data file" might refer to, queries Mem0 for past user preferences.
2. **Planner Agent:** Creates JSON Plan: `["Read python data file", "Analyze metrics using Python execution", "Synthesize findings"]`.
3. **Executor Agent (Iteration 1):** Selects tool `file_read(filepath="...")`. Reads file.
4. **Executor Agent (Iteration 2):** Selects tool `python_execution(code="...")`. Gets analytical output.
5. **Critic Agent:** Verifies output addresses user prompt. Synthesizes a coherent summary response. Returns `{"passed": true, "output": "..."}`.
6. **Memory Agent (Save):** Saves the final summary to ChromaDB and Mem0.
7. **Frontend View:** The user receives the summary text as well as an "Agent Reasoning Trace" drop-down showing exact tool calls and intermediate steps from each node.

---

## 4. Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+

### Environment Setup
1. Duplicate `backend/.env.example` as `backend/.env`.
2. Add your provider API keys (OpenAI is default for Mem0 and LiteLLM fallback):
   ```
   OPENAI_API_KEY=sk-...
   DEFAULT_LLM_MODEL=gpt-4o
   ```

### Running Backend (FastAPI + LangGraph)
Open a terminal inside the project root:
```bash
cd backend
python -m venv venv
# On Windows: venv\\Scripts\\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
*API will run on `http://localhost:8000`*

### Running Frontend (React + Vite)
Open a new terminal inside the project root:
```bash
cd frontend
npm install
npm run dev
```
*Application UI will run on `http://localhost:5173`*
