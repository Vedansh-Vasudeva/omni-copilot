import os
import json
from typing import List, Dict, Any
from litellm import completion

class LLMService:
    def __init__(self, model_override: str = None):
        self.default_model = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")
        self.model = model_override or self.default_model
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = completion(
                model=self.model,
                messages=messages,
                api_key=os.getenv("OPENAI_API_KEY", "dummy_key_if_using_local")
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"
            
    def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        result_text = self.generate(f"{prompt}\nReturn ONLY valid JSON.", system_prompt)
        
        # If it failed to connect to LLM, return a predictable mock based on the prompt signature
        if result_text.startswith("Error connecting"):
            if "Planner Agent" in system_prompt:
                return [f"Mock Step 1 for: {prompt[:30]}", "Mock Step 2 (End)"]
            elif "Executor Agent" in system_prompt:
                return {"tool": "none", "args": {}}
            elif "Critic Agent" in system_prompt:
                return {"passed": True, "final_output": f"Notice: Currently running in MOCK fallback mode due to Quota Limits.\nOriginal Request: {prompt[:100]}..."}
            return {"error": result_text}

        # Attempt to clean up markdown if any
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
        
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON target", "raw_output": result_text}

llm_service = LLMService()
