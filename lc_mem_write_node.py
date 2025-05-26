import json
from typing import Optional, Tuple, Dict, Any

# Attempt to import the backend service.
# The path '....lc_python_core.services.lc_mem_service' suggests ComfyUI custom nodes
# are loaded in a way that '....' navigates up from a deeper structure.
# This might need adjustment based on actual ComfyUI import behavior for custom nodes
# located outside the main ComfyUI directory structure if this file is symlinked or directly placed.
# For now, assuming a standard Python import mechanism relative to some base in sys.path.
try:
    from ....lc_python_core.services.lc_mem_service import write_mada_object
except ImportError:
    # Fallback for local development or if the path assumption is wrong.
    # This allows the node to load in ComfyUI even if the backend isn't immediately found,
    # though it will fail at runtime.
    print("\n!!! lc_mem_write_node.py: Failed to import write_mada_object from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # As a dummy, to allow ComfyUI to register the node without crashing on load:
    def write_mada_object(*args, **kwargs) -> Dict[str, Any]:
        return {
            "object_uid": None,
            "status": "Error: lc_mem_service.write_mada_object not found. Backend not imported.",
            "version": None,
        }

# Define a minimal MadaSeed type string for ComfyUI type system.
# In a real scenario, this would be a more complex object or a defined type.
MADA_SEED_TYPE = "MADA_SEED"


class LcMemWriteNode:
    """
    A ComfyUI node to write (create or update) a MADA object
    using the lc_mem_service.
    """

    NODE_NAME = "MADA Write Object"
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING", "STRING", "STRING")
    RETURN_NAMES = ("mada_seed_out", "object_uid", "storage_status", "version")
    FUNCTION = "execute_write"
    CATEGORY = "LearntCloud/MADA"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "object_payload_json": ("STRING", {"multiline": True, "default": "{}"}),
                "object_type": ("STRING", {"multiline": False, "default": "GenericMadaObject"}),
            },
            "optional": {
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}),
                "object_uid_to_update": ("STRING", {"multiline": False, "default": ""}),
                "initial_metadata_json": ("STRING", {"multiline": True, "default": "{}"}),
                "update_metadata_json": ("STRING", {"multiline": True, "default": "{}"}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_write(
        self,
        object_payload_json: str,
        object_type: str,
        requesting_persona_context_json: str = "{}",
        object_uid_to_update: Optional[str] = None,
        initial_metadata_json: str = "{}",
        update_metadata_json: str = "{}",
        mada_seed_in: Optional[Any] = None  # MadaSeed can be any type for passthrough
    ) -> Tuple[Optional[Any], Optional[str], str, Optional[str]]:
        """
        Executes the MADA object write operation.
        """
        # Prepare inputs for the backend service
        uid_to_update = object_uid_to_update if object_uid_to_update and object_uid_to_update.strip() else None
        
        # The backend service (write_mada_object) is expected to handle JSON string parsing.
        # No json.loads() here for the main content strings.

        # Validate JSON strings for critical optional fields if they are not empty,
        # as backend might expect valid JSON or empty/None.
        # However, write_mada_object is designed to handle invalid JSON strings gracefully.

        try:
            result = write_mada_object(
                object_payload_json=object_payload_json,
                object_type=object_type,
                requesting_persona_context_json=requesting_persona_context_json,
                object_uid_to_update=uid_to_update,
                initial_metadata_json=initial_metadata_json,
                update_metadata_json=update_metadata_json,
            )
        except Exception as e:
            # Catch any unexpected errors during the call to the backend
            error_message = f"Error calling write_mada_object: {type(e).__name__} - {str(e)}"
            print(f"[LcMemWriteNode] {error_message}")
            return (mada_seed_in, None, error_message, None)

        object_uid_out = result.get("object_uid")
        status_out = result.get("status", "Error: Status not returned from backend.")
        version_out = str(result.get("version", "")) # Ensure version is a string

        # Print for debugging in ComfyUI console
        print(f"[LcMemWriteNode] UID: {object_uid_out}, Status: {status_out}, Version: {version_out}")

        return (mada_seed_in, object_uid_out, status_out, version_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcMemWriteNode": LcMemWriteNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcMemWriteNode": "LC MADA Write Node"
}

if __name__ == "__main__":
    # This block is for testing the node logic outside of ComfyUI if needed.
    # It requires a mock or actual backend service.
    print("Testing LcMemWriteNode locally...")

    # Mock the backend service if not available
    if "write_mada_object" not in globals() or globals()["write_mada_object"] is None:
        def mock_backend_write(object_payload_json, object_type, **kwargs):
            print(f"Mock Backend: Called with type '{object_type}', payload: '{object_payload_json[:50]}...'")
            uid = kwargs.get("object_uid_to_update") or f"{object_type}-{hash(object_payload_json)}"
            version = 1
            if kwargs.get("object_uid_to_update"):
                version = 2 # Simulate update
            return {"object_uid": uid, "status": "Success (mocked)", "version": version}
        
        # Replace the potentially failed import with the mock for local testing
        write_mada_object = mock_backend_write 
        print("Using mock backend for write_mada_object.")


    node = LcMemWriteNode()

    # Test case 1: Create new object
    print("\n--- Test Case 1: Create New Object ---")
    payload1 = json.dumps({"data": "example_value", "number": 123})
    type1 = "TestType1"
    persona1 = json.dumps({"user": "test_user"})
    initial_meta1 = json.dumps({"source": "ComfyUI_test"})

    result1 = node.execute_write(
        object_payload_json=payload1,
        object_type=type1,
        requesting_persona_context_json=persona1,
        initial_metadata_json=initial_meta1
    )
    print(f"Result 1 (Create): {result1}")
    # Expected: (None, 'TestType1-<hash_of_payload1>', 'Success (mocked)', '1')

    # Test case 2: Update existing object
    print("\n--- Test Case 2: Update Existing Object ---")
    uid_to_update = result1[1] if result1[1] else "TestType1-dummy_uid_for_update"
    updated_payload1 = json.dumps({"data": "updated_value", "number": 456, "extra_field": True})
    update_meta1 = json.dumps({"modified_by": "ComfyUI_test_update"})

    result2 = node.execute_write(
        object_payload_json=updated_payload1,
        object_type=type1, # Type might be relevant for backend routing or validation
        object_uid_to_update=uid_to_update,
        update_metadata_json=update_meta1,
        requesting_persona_context_json=persona1
    )
    print(f"Result 2 (Update): {result2}")
    # Expected: (None, uid_to_update, 'Success (mocked)', '2')

    # Test case 3: Create with mada_seed_in
    print("\n--- Test Case 3: Create with mada_seed_in ---")
    payload3 = json.dumps({"config": "test_config"})
    type3 = "ConfigType"
    mock_mada_seed = {"seed_data": "some_seed_value_123"} # Example MadaSeed object
    
    result3 = node.execute_write(
        object_payload_json=payload3,
        object_type=type3,
        mada_seed_in=mock_mada_seed
    )
    print(f"Result 3 (Create with Seed): {result3}")
    # Expected: ({'seed_data': 'some_seed_value_123'}, 'ConfigType-<hash_of_payload3>', 'Success (mocked)', '1')
    assert result3[0] is mock_mada_seed # Verify passthrough

    # Test case 4: Empty UID string for update (should be treated as None by backend)
    print("\n--- Test Case 4: Empty UID string for update (should be create) ---")
    result4 = node.execute_write(
        object_payload_json=json.dumps({"info": "new object due to empty uid"}),
        object_type="AnotherType",
        object_uid_to_update="" # Empty string
    )
    print(f"Result 4 (Empty UID for update): {result4}")
    # Expected to behave like a create, version 1

    print("\nLocal testing finished.")
