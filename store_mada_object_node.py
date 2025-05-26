import json
from typing import Optional, Dict, Any

# Assuming mock_lc_core_services are accessible via this path
from lc_python_core.services.lc_mem_service import mock_lc_mem_core_ensure_uid, mock_lc_mem_core_create_object

class StoreMadaObjectNode:
    CATEGORY = "LearntCloud/MADA"
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("new_object_uid", "storage_status",)
    FUNCTION = "store_object"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "object_payload_json": ("STRING", {"multiline": True, "default": "{}"}),
                "object_type": ("STRING", {"multiline": False, "default": "GenericMadaObject"}),
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}), 
            },
            "optional": {
                "initial_metadata_json": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    def store_object(self, object_payload_json: str, object_type: str, requesting_persona_context_json: str, initial_metadata_json: Optional[str] = None):
        storage_status = ""
        new_object_uid = ""

        try:
            payload_dict: Optional[Dict[str, Any]] = None
            if object_payload_json and object_payload_json.strip():
                try:
                    payload_dict = json.loads(object_payload_json)
                except json.JSONDecodeError as e:
                    storage_status = f"Error decoding object_payload_json: {e}"
                    print(f"StoreMadaObjectNode: {storage_status}")
                    return (new_object_uid, storage_status)
            else:
                storage_status = "Error: object_payload_json cannot be empty."
                print(f"StoreMadaObjectNode: {storage_status}")
                return (new_object_uid, storage_status)

            persona_context_dict: Optional[Dict[str, Any]] = None
            if requesting_persona_context_json and requesting_persona_context_json.strip():
                try:
                    persona_context_dict = json.loads(requesting_persona_context_json)
                except json.JSONDecodeError as e:
                    storage_status = f"Error decoding persona_context_json: {e}"
                    print(f"StoreMadaObjectNode: {storage_status}")
                    return (new_object_uid, storage_status)
            
            metadata_dict: Optional[Dict[str, Any]] = None
            if initial_metadata_json and initial_metadata_json.strip() and initial_metadata_json != "{}":
                try:
                    metadata_dict = json.loads(initial_metadata_json)
                except json.JSONDecodeError as e:
                    storage_status = f"Error decoding initial_metadata_json: {e}"
                    print(f"StoreMadaObjectNode: {storage_status}")
                    return (new_object_uid, storage_status)

            print(f"StoreMadaObjectNode: Calling mock_lc_mem_core_ensure_uid for type: {object_type}")
            # ensure_uid(object_type: str, context_description: Optional[str] = None, existing_uid_candidate: Optional[str] = None)
            generated_uid_or_error = mock_lc_mem_core_ensure_uid(object_type=object_type, context_description=f"ComfyUI StoreMadaObjectNode call for {object_type}")

            if "Error" in generated_uid_or_error or "ERROR" in generated_uid_or_error : # Basic error check for mock
                storage_status = f"Error ensuring UID: {generated_uid_or_error}"
                print(f"StoreMadaObjectNode: {storage_status}")
                return (new_object_uid, storage_status)
            
            new_object_uid = generated_uid_or_error
            print(f"StoreMadaObjectNode: Ensured UID {new_object_uid}. Calling mock_lc_mem_core_create_object.")

            # create_object(object_uid: str, object_payload: Dict[str, Any], initial_metadata: Optional[Dict[str, Any]] = None, requesting_persona_context: Optional[Dict[str, Any]] = None)
            success_or_error = mock_lc_mem_core_create_object(
                object_uid=new_object_uid,
                object_payload=payload_dict, # Must not be None here
                initial_metadata=metadata_dict,
                requesting_persona_context=persona_context_dict
            )
            
            if success_or_error == True: # Mock service returns True on success
                storage_status = f"Success: Object stored with UID {new_object_uid}."
            else: # Mock service might return an error string or False
                storage_status = f"Error storing object: {success_or_error}"
                new_object_uid = "" # Clear UID if storage failed

            print(f"StoreMadaObjectNode: {storage_status}")

        except Exception as e:
            storage_status = f"Exception during store_object: {str(e)}"
            new_object_uid = ""
            print(f"StoreMadaObjectNode: {storage_status}")
        
        return (new_object_uid, storage_status)
