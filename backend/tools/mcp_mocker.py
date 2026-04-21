class MCPMocker:
    """Mock implementation of Model Context Protocol"""
    def __init__(self):
        self.resources = {}
        self.prompts = {}
        self.tools = []
        
    def register_tool(self, tool_name: str, description: str, handler):
        self.tools.append({
            "name": tool_name,
            "description": description,
            "handler": handler
        })
        
    def list_tools(self):
        return [{"name": t["name"], "description": t["description"]} for t in self.tools]
        
    def execute_tool(self, tool_name: str, args: dict):
        for t in self.tools:
            if t["name"] == tool_name:
                try:
                    return t["handler"](**args)
                except Exception as e:
                    return f"Error executing tool {tool_name}: {str(e)}"
        return f"Tool {tool_name} not found"

mcp_server = MCPMocker()
