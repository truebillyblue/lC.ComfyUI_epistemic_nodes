import json
from typing import Optional, Dict, Any

# Assuming mock_lc_core_services are accessible via this path
# This might need adjustment based on actual lc_python_core structure and PYTHONPATH
from lc_python_core.services.lc_mem_service import mock_lc_mem_core_get_object

class GetMadaObjectNode:
    CATEGORY = "LearntCloud/MADA" # New category for MADA related nodes
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("mada_object_content", "retrieval_status",)
    FUNCTION = "get_object"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "object_uid": ("STRING", {"multiline": False, "default": "urn:crux:uid::example_uid"}),
                # For now, persona_context is a simple string; future might involve more structured input
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}), 
            }
        }

    def get_object(self, object_uid: str, requesting_persona_context_json: str):
        retrieval_status = ""
        mada_object_content_str = ""

        try:
            persona_context_dict: Optional[Dict[str, Any]] = None
            if requesting_persona_context_json and requesting_persona_context_json.strip():
                try:
                    persona_context_dict = json.loads(requesting_persona_context_json)
                except json.JSONDecodeError as e:
                    retrieval_status = f"Error decoding persona_context JSON: {e}"
                    print(f"GetMadaObjectNode: {retrieval_status}")
                    return (mada_object_content_str, retrieval_status)
            
            print(f"GetMadaObjectNode: Calling mock_lc_mem_core_get_object for UID: {object_uid}")
            
            # Call the mock service function
            # mock_lc_mem_core_get_object(object_uid: str, version_hint: Optional[str] = None, requesting_persona_context: Optional[Dict] = None, default_value: Any = None)
            retrieved_object = mock_lc_mem_core_get_object(
                object_uid=object_uid,
                requesting_persona_context=persona_context_dict 
                # default_value could be set to a specific error indicator if object not in mock_mada_store
            )

            if retrieved_object is not None:
                # We need to serialize the object to a JSON string for the output
                try:
                    mada_object_content_str = json.dumps(retrieved_object, indent=2)
                    retrieval_status = f"Success: Object retrieved for UID {object_uid}."
                    # Add object to the mock store if it was a default string indicating not found.
                    # This part is tricky as the mock function's default_value might be a string.
                    # For a more robust mock, the mock_lc_mem_core_get_object would ideally return a specific marker
                    # if the object is not found, rather than its default_value being confusable with actual content.
                    # For now, we assume if it's not None, it's considered "found".
                    if isinstance(retrieved_object, str) and "not found in mock_mada_store" in retrieved_object:
                         retrieval_status = f"Info: UID {object_uid} not found in mock_mada_store. Returned default."
                    
                except TypeError as te:
                    mada_object_content_str = f"Error: Retrieved object for UID {object_uid} is not JSON serializable."
                    retrieval_status = f"Error: Retrieved object for UID {object_uid} is not JSON serializable: {te}"
                    print(f"GetMadaObjectNode: {retrieval_status}")
            else:
                retrieval_status = f"Error: No object found for UID {object_uid} (or mock service returned None)."
                print(f"GetMadaObjectNode: {retrieval_status}")

        except Exception as e:
            retrieval_status = f"Exception during get_object: {e}"
            print(f"GetMadaObjectNode: {retrieval_status}")
        
        return (mada_object_content_str, retrieval_status)
