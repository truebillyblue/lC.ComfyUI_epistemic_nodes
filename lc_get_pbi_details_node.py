import json
from typing import Optional, Tuple, Dict, Any

# Attempt to import the backend service
try:
    from lc_python_core.services.lc_mem_service import get_pbi_details
except ImportError:
    print("\n!!! lc_get_pbi_details_node.py: Failed to import get_pbi_details from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # Dummy for ComfyUI registration
    def get_pbi_details(*args, **kwargs) -> Dict[str, Any]:
        return {
            "status": "Error: lc_mem_service.get_pbi_details not found. Backend not imported.",
            "pbi_uid": kwargs.get("pbi_uid"),
            "details": None,
        }

# Define a minimal MadaSeed type string for ComfyUI type system
MADA_SEED_TYPE = "MADA_SEED"


class LcGetPbiDetailsNode:
    """
    A ComfyUI node to retrieve Product Backlog Item (PBI) details
    using the lc_mem_service.
    """

    NODE_NAME = "MADA Get PBI Details" # Consistent naming with MADA Write
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING", "STRING")
    RETURN_NAMES = ("mada_seed_out", "pbi_details_json", "status")
    FUNCTION = "execute_get_details"
    CATEGORY = "LearntCloud/Backlog" # As specified

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pbi_uid": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_get_details(
        self,
        pbi_uid: str,
        requesting_persona_context_json: str = "{}",
        mada_seed_in: Optional[Any] = None  # MadaSeed can be any type for passthrough
    ) -> Tuple[Optional[Any], str, str]:
        """
        Executes the PBI details retrieval operation.
        """
        if not pbi_uid or not pbi_uid.strip():
            status_out = "Error: PBI UID is required."
            print(f"[LcGetPbiDetailsNode] {status_out}")
            return (mada_seed_in, "{}", status_out)

        persona_context_dict: Optional[Dict[str, Any]] = None
        if requesting_persona_context_json and requesting_persona_context_json.strip():
            try:
                persona_context_dict = json.loads(requesting_persona_context_json)
            except json.JSONDecodeError as e:
                status_out = f"Error: Invalid JSON in requesting_persona_context_json: {e}"
                print(f"[LcGetPbiDetailsNode] {status_out}")
                return (mada_seed_in, "{}", status_out)
        
        try:
            result = get_pbi_details(
                pbi_uid=pbi_uid,
                requesting_persona_context=persona_context_dict
            )
        except Exception as e:
            error_message = f"Error calling get_pbi_details: {type(e).__name__} - {str(e)}"
            print(f"[LcGetPbiDetailsNode] {error_message}")
            return (mada_seed_in, "{}", error_message)

        status_out = result.get("status", "Error: Status not returned from backend.")
        pbi_details = result.get("details")

        pbi_details_json_str = "{}"
        if pbi_details is not None and isinstance(pbi_details, dict):
            try:
                pbi_details_json_str = json.dumps(pbi_details, indent=4)
            except TypeError as e: # Should not happen if details is a dict from valid JSON
                status_out = f"Error: Failed to serialize PBI details to JSON: {e}"
                print(f"[LcGetPbiDetailsNode] {status_out}")
                # Keep pbi_details_json_str as "{}"
        elif status_out.startswith("Success") and pbi_details is None:
            # If backend reports success but details are None, it's a bit ambiguous.
            # For robustness, we'll output empty JSON.
            print(f"[LcGetPbiDetailsNode] Warning: Status is Success but PBI details are None for UID {pbi_uid}.")


        print(f"[LcGetPbiDetailsNode] UID: {pbi_uid}, Status: {status_out}, Details fetched: {pbi_details is not None}")

        return (mada_seed_in, pbi_details_json_str, status_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcGetPbiDetailsNode": LcGetPbiDetailsNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcGetPbiDetailsNode": "LC Get PBI Details Node"
}

if __name__ == "__main__":
    print("Testing LcGetPbiDetailsNode locally...")

    # Mock the backend service if not available
    if "get_pbi_details" not in globals() or globals()["get_pbi_details"] is None:
        def mock_backend_get_pbi_details(pbi_uid: str, requesting_persona_context: Optional[Dict[str, Any]] = None):
            print(f"Mock Backend: Called get_pbi_details for UID '{pbi_uid}' with context: {requesting_persona_context}")
            if pbi_uid == "pbi-exists-001":
                return {
                    "status": "Success", 
                    "pbi_uid": pbi_uid, 
                    "details": {"title": "Mock PBI Title", "description": "This is a mock PBI."}
                }
            elif pbi_uid == "pbi-no-details-002":
                 return {
                    "status": "Success", # Success, but no details (edge case)
                    "pbi_uid": pbi_uid, 
                    "details": None 
                }
            else:
                return {"status": "Error: PBI not found", "pbi_uid": pbi_uid, "details": None}
        
        get_pbi_details = mock_backend_get_pbi_details
        print("Using mock backend for get_pbi_details.")

    node = LcGetPbiDetailsNode()

    # Test case 1: PBI exists
    print("\n--- Test Case 1: PBI Exists ---")
    persona_ctx_str1 = json.dumps({"user": "test_user_1"})
    pbi_uid1 = "pbi-exists-001"
    result1 = node.execute_get_details(pbi_uid=pbi_uid1, requesting_persona_context_json=persona_ctx_str1)
    print(f"Result 1 (Exists): {result1}")
    # Expected: (None, '{\n    "title": "Mock PBI Title",\n    "description": "This is a mock PBI."\n}', 'Success')
    assert result1[2] == "Success"
    assert "Mock PBI Title" in result1[1]

    # Test case 2: PBI does not exist
    print("\n--- Test Case 2: PBI Does Not Exist ---")
    pbi_uid2 = "pbi-nonexistent-000"
    result2 = node.execute_get_details(pbi_uid=pbi_uid2)
    print(f"Result 2 (Not Found): {result2}")
    # Expected: (None, '{}', 'Error: PBI not found')
    assert result2[1] == "{}"
    assert "Error: PBI not found" in result2[2]

    # Test case 3: PBI exists, with mada_seed_in
    print("\n--- Test Case 3: PBI Exists with Mada Seed ---")
    mock_mada_seed = {"seed_info": "passthrough_data_789"}
    result3 = node.execute_get_details(pbi_uid=pbi_uid1, mada_seed_in=mock_mada_seed)
    print(f"Result 3 (Exists with Seed): {result3}")
    # Expected: ({'seed_info': 'passthrough_data_789'}, '{\n    "title": "Mock PBI Title",\n    "description": "This is a mock PBI."\n}', 'Success')
    assert result3[0] is mock_mada_seed
    assert "Mock PBI Title" in result3[1]

    # Test case 4: Invalid JSON for persona context
    print("\n--- Test Case 4: Invalid Persona Context JSON ---")
    invalid_persona_json = '{"user": "test_user_2", "broken_json": True' # Intentionally broken
    result4 = node.execute_get_details(pbi_uid=pbi_uid1, requesting_persona_context_json=invalid_persona_json)
    print(f"Result 4 (Invalid JSON): {result4}")
    # Expected: (None, '{}', 'Error: Invalid JSON in requesting_persona_context_json: ...')
    assert result4[1] == "{}"
    assert "Error: Invalid JSON" in result4[2]
    
    # Test case 5: Empty PBI UID
    print("\n--- Test Case 5: Empty PBI UID ---")
    result5 = node.execute_get_details(pbi_uid="")
    print(f"Result 5 (Empty UID): {result5}")
    # Expected: (None, '{}', 'Error: PBI UID is required.')
    assert result5[1] == "{}"
    assert result5[2] == "Error: PBI UID is required."

    # Test case 6: Backend returns success but details are None
    print("\n--- Test Case 6: Backend Success, Details None ---")
    pbi_uid6 = "pbi-no-details-002"
    result6 = node.execute_get_details(pbi_uid=pbi_uid6)
    print(f"Result 6 (Success, No Details): {result6}")
    # Expected: (None, '{}', 'Success')
    assert result6[1] == "{}" # Should still output empty JSON string
    assert result6[2] == "Success"


    print("\nLocal testing finished.")
