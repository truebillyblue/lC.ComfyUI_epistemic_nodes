import json
from typing import Optional, Tuple, Dict, Any

# Attempt to import the backend service
try:
    # Adjust path based on actual ComfyUI loading and project structure
    from ....lc_python_core.services.lc_api_agent_service import execute_api_call
except ImportError:
    print("\n!!! lc_api_llm_agent_node.py: Failed to import execute_api_call from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # Dummy for ComfyUI registration
    def execute_api_call(*args, **kwargs) -> Dict[str, Any]:
        return {
            "status": "Error: lc_api_agent_service.execute_api_call not found. Backend not imported.",
            "agent_response_text": None,
            "full_response_json": {"error": "Backend service not imported"},
            "http_status_code": None
        }

# Define a minimal MadaSeed type string for ComfyUI type system
MADA_SEED_TYPE = "MADA_SEED"


class LcApiLlmAgentNode:
    """
    A ComfyUI node to make API calls to LLMs using the lc_api_agent_service.
    """

    NODE_NAME = "LLM API Agent" 
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING", "STRING", "STRING") 
    RETURN_NAMES = ("mada_seed_out", "agent_response_text", "full_response_json", "status")
    FUNCTION = "execute_api_llm_call"
    CATEGORY = "LearntCloud/Agents"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_endpoint_url": ("STRING", {"multiline": False, "default": ""}),
                "prompt_text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "api_key_env_var": ("STRING", {"multiline": False, "default": "OPENAI_API_KEY"}),
                "request_payload_template_json": ("STRING", {"multiline": True, "default": '{"model": "gpt-3.5-turbo", "messages": []}'}),
                "conversation_history_json": ("STRING", {"multiline": True, "default": ""}), # Default as empty string, service handles as None if empty
                "response_extraction_path": ("STRING", {"multiline": False, "default": "choices[0].message.content"}),
                "request_parameters_json": ("STRING", {"multiline": True, "default": '{"temperature": 0.7, "max_tokens": 512}'}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_api_llm_call(
        self,
        api_endpoint_url: str,
        prompt_text: str,
        api_key_env_var: Optional[str] = "OPENAI_API_KEY",
        request_payload_template_json: Optional[str] = '{"model": "gpt-3.5-turbo", "messages": []}',
        conversation_history_json: Optional[str] = "",
        response_extraction_path: Optional[str] = "choices[0].message.content",
        request_parameters_json: Optional[str] = '{"temperature": 0.7, "max_tokens": 512}',
        mada_seed_in: Optional[Any] = None
    ) -> Tuple[Optional[Any], Optional[str], str, str]:
        """
        Executes the API call to the LLM.
        """
        if not api_endpoint_url or not api_endpoint_url.strip():
            status_out = "Error: API Endpoint URL is required."
            print(f"[LcApiLlmAgentNode] {status_out}")
            return (mada_seed_in, None, "{}", status_out)
        
        if not prompt_text or not prompt_text.strip(): # Prompt text is generally essential
            status_out = "Error: Prompt text is required."
            print(f"[LcApiLlmAgentNode] {status_out}")
            return (mada_seed_in, None, "{}", status_out)

        # Helper to convert empty/whitespace-only strings to None for optional service params
        def none_if_empty(value: Optional[str]) -> Optional[str]:
            return value if value and value.strip() else None

        try:
            result = execute_api_call(
                api_endpoint_url=api_endpoint_url,
                prompt_text=prompt_text,
                api_key_env_var=none_if_empty(api_key_env_var),
                request_payload_template_json=none_if_empty(request_payload_template_json),
                conversation_history_json=none_if_empty(conversation_history_json),
                response_extraction_path=none_if_empty(response_extraction_path),
                request_parameters_json=none_if_empty(request_parameters_json),
                # requesting_persona_context=None # Placeholder for now
            )
        except Exception as e:
            error_message = f"Error calling execute_api_call service: {type(e).__name__} - {str(e)}"
            print(f"[LcApiLlmAgentNode] {error_message}")
            return (mada_seed_in, None, "{}", error_message)

        agent_response_text_out = result.get("agent_response_text")
        full_response_dict = result.get("full_response_json", {}) # Default to empty dict if missing
        status_out = result.get("status", "Error: Status not returned from backend.")
        
        full_response_json_str = "{}"
        try:
            full_response_json_str = json.dumps(full_response_dict, indent=2) if full_response_dict else "{}"
        except TypeError as e: # Should not happen if full_response_dict is JSON serializable
            status_out = f"Error: Failed to serialize full API response to JSON: {e}. Original status: {status_out}"
            print(f"[LcApiLlmAgentNode] Serialization error: {e}")
            # full_response_json_str remains "{}"
        
        print(f"[LcApiLlmAgentNode] Endpoint: {api_endpoint_url}, Status: {status_out}, HTTP Code: {result.get('http_status_code')}")
        if agent_response_text_out:
             print(f"  Agent Response Snippet: {agent_response_text_out[:100]}...")


        return (mada_seed_in, agent_response_text_out, full_response_json_str, status_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcApiLlmAgentNode": LcApiLlmAgentNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcApiLlmAgentNode": "LC LLM API Agent"
}

if __name__ == "__main__":
    print("Testing LcApiLlmAgentNode locally...")

    # Mock the backend service if not available
    if "execute_api_call" not in globals() or globals()["execute_api_call"] is None:
        def mock_service_execute_api_call(api_endpoint_url, prompt_text, **kwargs):
            print(f"Mock Service: Called execute_api_call for URL '{api_endpoint_url}', prompt '{prompt_text[:30]}...'")
            if "error" in api_endpoint_url:
                return {
                    "status": "Error: Mock service failure", 
                    "agent_response_text": None, 
                    "full_response_json": {"detail": "Mocked error condition"},
                    "http_status_code": 500
                }
            
            # Simulate successful call with echo-like behavior for relevant parts
            response_text = f"Mock response to: {prompt_text}"
            if kwargs.get("response_extraction_path") == "specific.path.to.text":
                 response_text = "Specifically extracted mock text."

            full_json_resp = {
                "id": "mock_resp_123",
                "object": "text_completion", # Example structure
                "choices": [{"message": {"role": "assistant", "content": response_text}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
                "input_payload_debug": { # Debug: Show what service might have constructed
                    "endpoint": api_endpoint_url, "prompt": prompt_text, "options": kwargs
                }
            }
            return {
                "status": "Success", 
                "agent_response_text": response_text, 
                "full_response_json": full_json_resp,
                "http_status_code": 200
            }
        
        execute_api_call = mock_service_execute_api_call
        print("Using mock backend for execute_api_call service.")

    node = LcApiLlmAgentNode()

    # Test case 1: Successful API call with default parameters
    print("\n--- Test Case 1: Successful Call (Defaults) ---")
    result1 = node.execute_api_llm_call(
        api_endpoint_url="https://api.example.com/v1/chat",
        prompt_text="What is the capital of France?"
    )
    print(f"Result 1: Status='{result1[3]}', Response Snippet='{str(result1[1])[:50]}...'")
    assert result1[3] == "Success"
    assert "Mock response to: What is the capital of France?" in result1[1]
    assert '"id": "mock_resp_123"' in result1[2] # Check full JSON string

    # Test case 2: API Endpoint URL is empty
    print("\n--- Test Case 2: Empty API Endpoint URL ---")
    result2 = node.execute_api_llm_call(api_endpoint_url="  ", prompt_text="A prompt.")
    print(f"Result 2: Status='{result2[3]}'")
    assert result2[3] == "Error: API Endpoint URL is required."
    assert result2[1] is None
    assert result2[2] == "{}"

    # Test case 3: Prompt text is empty
    print("\n--- Test Case 3: Empty Prompt Text ---")
    result3 = node.execute_api_llm_call(api_endpoint_url="https://api.example.com/v1", prompt_text="\n   \t")
    print(f"Result 3: Status='{result3[3]}'")
    assert result3[3] == "Error: Prompt text is required."

    # Test case 4: Custom response_extraction_path
    print("\n--- Test Case 4: Custom Response Extraction Path ---")
    result4 = node.execute_api_llm_call(
        api_endpoint_url="https://api.example.com/v1/complete",
        prompt_text="Tell me a joke.",
        response_extraction_path="specific.path.to.text" # Mock service will use this
    )
    print(f"Result 4: Status='{result4[3]}', Response='{result4[1]}'")
    assert result4[3] == "Success"
    assert result4[1] == "Specifically extracted mock text."

    # Test case 5: Service returns an error
    print("\n--- Test Case 5: Service Error ---")
    result5 = node.execute_api_llm_call(
        api_endpoint_url="https://error.example.com/v1", # Mock service will trigger error
        prompt_text="This will cause an error."
    )
    print(f"Result 5: Status='{result5[3]}'")
    assert "Error: Mock service failure" in result5[3]
    assert '"detail": "Mocked error condition"' in result5[2]


    # Test case 6: Mada seed passthrough
    print("\n--- Test Case 6: Mada Seed Passthrough ---")
    mock_seed = {"some_data": "seed_content_123"}
    result6 = node.execute_api_llm_call(
        api_endpoint_url="https://api.example.com/v1/chat",
        prompt_text="How does mada_seed work?",
        mada_seed_in=mock_seed
    )
    print(f"Result 6: Status='{result6[3]}', Mada Seed Out Type: {type(result6[0])}")
    assert result6[0] is mock_seed
    assert result6[3] == "Success"

    print("\nLocal testing finished.")
