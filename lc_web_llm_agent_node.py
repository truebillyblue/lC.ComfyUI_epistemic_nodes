import json
from typing import Optional, Tuple, Dict, Any, List

# Attempt to import the backend service
try:
    # Adjust path based on actual ComfyUI loading and project structure
    from lc_python_core.services.lc_web_agent_service import execute_web_interaction
except ImportError:
    print("\n!!! lc_web_llm_agent_node.py: Failed to import execute_web_interaction from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # Dummy for ComfyUI registration
    def execute_web_interaction(*args, **kwargs) -> Dict[str, Any]:
        return {
            "status": "Error: lc_web_agent_service.execute_web_interaction not found. Backend not imported.",
            "extracted_data": None,
            "log": ["Backend service not imported."],
        }

# Define a minimal MadaSeed type string for ComfyUI type system
MADA_SEED_TYPE = "MADA_SEED"

DEFAULT_INTERACTION_SCRIPT = json.dumps([
    {"action": "goto", "url": None}, # None means use target_url from input
    {"action": "wait_for_timeout", "timeout_ms": 1000},
    {"action": "read_text", "selector": "body", "variable_name": "page_content"}
], indent=2)

DEFAULT_BROWSER_PARAMS = json.dumps({
    "browser_type": "chromium", 
    "headless": True, 
    "page_load_timeout_ms": 30000, 
    "default_action_timeout_ms": 10000
}, indent=2)


class LcWebLlmAgentNode:
    """
    A ComfyUI node to perform web interactions using Playwright via the lc_web_agent_service.
    """

    NODE_NAME = "Web LLM Agent" 
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING", "STRING", "STRING") 
    RETURN_NAMES = ("mada_seed_out", "extracted_data", "interaction_log", "status")
    FUNCTION = "execute_web_llm_interaction"
    CATEGORY = "LearntCloud/Agents"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_url": ("STRING", {"multiline": False, "default": "https://www.google.com"}),
                "interaction_script_json": ("STRING", {"multiline": True, "default": DEFAULT_INTERACTION_SCRIPT}),
            },
            "optional": {
                "browser_control_params_json": ("STRING", {"multiline": True, "default": DEFAULT_BROWSER_PARAMS}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_web_llm_interaction(
        self,
        target_url: str,
        interaction_script_json: str,
        browser_control_params_json: Optional[str] = DEFAULT_BROWSER_PARAMS,
        mada_seed_in: Optional[Any] = None
    ) -> Tuple[Optional[Any], str, str, str]:
        """
        Executes the web interaction script.
        """
        if not target_url or not target_url.strip():
            status_out = "Error: Target URL is required."
            print(f"[LcWebLlmAgentNode] {status_out}")
            return (mada_seed_in, "{}", "[]", status_out)
        
        if not interaction_script_json or not interaction_script_json.strip():
            status_out = "Error: Interaction Script JSON is required."
            print(f"[LcWebLlmAgentNode] {status_out}")
            return (mada_seed_in, "{}", "[]", status_out)

        # Validate interaction_script_json (basic check, service does more)
        try:
            json.loads(interaction_script_json)
        except json.JSONDecodeError as e:
            status_out = f"Error: Invalid JSON in Interaction Script: {e}"
            print(f"[LcWebLlmAgentNode] {status_out}")
            return (mada_seed_in, "{}", "[]", status_out)

        # Validate browser_control_params_json if provided (basic check)
        parsed_browser_params_json_str: Optional[str] = None
        if browser_control_params_json and browser_control_params_json.strip():
            try:
                json.loads(browser_control_params_json) # Validate
                parsed_browser_params_json_str = browser_control_params_json
            except json.JSONDecodeError as e:
                status_out = f"Error: Invalid JSON in Browser Control Params: {e}"
                print(f"[LcWebLlmAgentNode] {status_out}")
                return (mada_seed_in, "{}", "[]", status_out)
        
        try:
            # Backend service (execute_web_interaction) expects JSON strings.
            result = execute_web_interaction(
                target_url=target_url,
                interaction_script_json=interaction_script_json, 
                browser_control_params_json=parsed_browser_params_json_str
                # requesting_persona_context can be None for now
            )
        except Exception as e:
            error_message = f"Error calling execute_web_interaction service: {type(e).__name__} - {str(e)}"
            print(f"[LcWebLlmAgentNode] {error_message}")
            return (mada_seed_in, "{}", "[]", error_message)

        extracted_data_dict = result.get("extracted_data", {})
        log_list = result.get("log", [])
        status_out = result.get("status", "Error: Unknown status from service")
        
        extracted_data_json_str = "{}"
        interaction_log_json_str = "[]"

        try:
            extracted_data_json_str = json.dumps(extracted_data_dict, indent=2) if extracted_data_dict is not None else "{}"
        except TypeError as e:
            status_out = f"Error serializing extracted_data: {e}. Original status: {status_out}"
            print(f"[LcWebLlmAgentNode] Extracted data serialization error: {e}")
            # extracted_data_json_str remains "{}"

        try:
            interaction_log_json_str = json.dumps(log_list, indent=2) if log_list is not None else "[]"
        except TypeError as e:
            status_out = f"Error serializing interaction_log: {e}. Original status: {status_out}"
            print(f"[LcWebLlmAgentNode] Interaction log serialization error: {e}")
            # interaction_log_json_str remains "[]"
        
        print(f"[LcWebLlmAgentNode] Target URL: {target_url}, Status: {status_out}")
        if extracted_data_dict:
             print(f"  Extracted Data Snippet: {str(extracted_data_dict)[:100]}...")
        # print(f"  Interaction Log: {interaction_log_json_str}")


        return (mada_seed_in, extracted_data_json_str, interaction_log_json_str, status_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcWebLlmAgentNode": LcWebLlmAgentNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcWebLlmAgentNode": "LC Web Interaction Agent"
}

if __name__ == "__main__":
    print("Testing LcWebLlmAgentNode locally...")

    # Mock the backend service if not available
    if "execute_web_interaction" not in globals() or globals()["execute_web_interaction"] is None:
        def mock_service_execute_web_interaction(target_url, interaction_script_json, browser_control_params_json=None, **kwargs):
            print(f"Mock Service: Called execute_web_interaction for URL '{target_url}'")
            script = json.loads(interaction_script_json)
            log = [f"Mock service received script with {len(script)} steps for {target_url}."]
            extracted = {}
            status = "Success"

            if "error" in target_url:
                status = "Error: Mock service web interaction failure"
                log.append(status)
            else:
                for step in script:
                    log.append(f"  Mock processing action: {step.get('action')}")
                    if step.get("action") == "read_text" and step.get("variable_name"):
                        extracted[step.get("variable_name")] = f"Mock content for selector {step.get('selector')} on {target_url}"
                log.append("Mock script processing complete.")
            
            return {
                "status": status, 
                "extracted_data": extracted, 
                "log": log
            }
        
        execute_web_interaction = mock_service_execute_web_interaction
        print("Using mock backend for execute_web_interaction service.")

    node = LcWebLlmAgentNode()

    # Test case 1: Successful web interaction
    print("\n--- Test Case 1: Successful Interaction ---")
    script1 = json.dumps([
        {"action": "goto", "url": "https://example.com/page1"},
        {"action": "read_text", "selector": "h1", "variable_name": "title"}
    ])
    result1 = node.execute_web_llm_interaction(
        target_url="https://example.com", # Fallback if script goto url is null
        interaction_script_json=script1
    )
    print(f"Result 1: Status='{result1[3]}', Extracted Snippet='{result1[1][:50]}...', Log Snippet='{result1[2][:50]}...'")
    assert result1[3] == "Success"
    assert '"title": "Mock content for selector h1 on https://example.com/page1"' in result1[1]
    assert "Mock processing action: goto" in result1[2]


    # Test case 2: Target URL is empty
    print("\n--- Test Case 2: Empty Target URL ---")
    result2 = node.execute_web_llm_interaction(target_url="  ", interaction_script_json=DEFAULT_INTERACTION_SCRIPT)
    print(f"Result 2: Status='{result2[3]}'")
    assert result2[3] == "Error: Target URL is required."
    assert result2[1] == "{}" and result2[2] == "[]"

    # Test case 3: Interaction script is empty
    print("\n--- Test Case 3: Empty Interaction Script ---")
    result3 = node.execute_web_llm_interaction(target_url="https://example.com", interaction_script_json="\n   \t")
    print(f"Result 3: Status='{result3[3]}'")
    assert result3[3] == "Error: Interaction Script JSON is required."

    # Test case 4: Invalid JSON in interaction_script_json
    print("\n--- Test Case 4: Invalid Interaction Script JSON ---")
    result4 = node.execute_web_llm_interaction(target_url="https://example.com", interaction_script_json="[{'action': 'goto',]") # Invalid JSON
    print(f"Result 4: Status='{result4[3]}'")
    assert "Error: Invalid JSON in Interaction Script" in result4[3]
    
    # Test case 5: Invalid JSON in browser_control_params_json
    print("\n--- Test Case 5: Invalid Browser Control Params JSON ---")
    result5 = node.execute_web_llm_interaction(
        target_url="https://example.com", 
        interaction_script_json=DEFAULT_INTERACTION_SCRIPT,
        browser_control_params_json="{'browser': 'chrome',}" # Invalid JSON
    )
    print(f"Result 5: Status='{result5[3]}'")
    assert "Error: Invalid JSON in Browser Control Params" in result5[3]

    # Test case 6: Service returns an error
    print("\n--- Test Case 6: Service Error ---")
    result6 = node.execute_web_llm_interaction(
        target_url="https://error.example.com", # Mock service will trigger error
        interaction_script_json=DEFAULT_INTERACTION_SCRIPT
    )
    print(f"Result 6: Status='{result6[3]}'")
    assert "Error: Mock service web interaction failure" in result6[3]
    
    # Test case 7: Mada seed passthrough
    print("\n--- Test Case 7: Mada Seed Passthrough ---")
    mock_seed = {"web_seed_data": "alpha_beta_zeta"}
    result7 = node.execute_web_llm_interaction(
        target_url="https://example.com",
        interaction_script_json=DEFAULT_INTERACTION_SCRIPT,
        mada_seed_in=mock_seed
    )
    print(f"Result 7: Status='{result7[3]}', Mada Seed Out Type: {type(result7[0])}")
    assert result7[0] is mock_seed
    assert result7[3] == "Success"

    print("\nLocal testing finished.")
