from typing import Optional, List, Dict, Any
from ....lc_python_core.sops.meta_sops.sop_rdsotm_management import create_rdsotm_component

# Enum-like class for ComfyUI dropdown
class RDSOTMComponentTypes:
    VALUES = ["Doctrine", "Strategy", "Operations", "Tactics", "Mission", "RealityInput"]
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"component_type": (s.VALUES,)}}

class CreateRDSOTMComponentNode:
    CATEGORY = "LearntCloud/RDSOTM"
    RETURN_TYPES = ("STRING", "STRING",) # cycle_linkage_uid (passthrough), new_component_uid
    RETURN_NAMES = ("cycle_linkage_uid", "component_uid",)
    FUNCTION = "create_component"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cycle_linkage_uid": ("STRING", {"forceInput": True}),
                "component_type": (RDSOTMComponentTypes.VALUES,),
                "name": ("STRING", {"multiline": False, "default": "New Component"}),
                "description": ("STRING", {"multiline": True, "default": ""}),
                "content_text": ("STRING", {"multiline": True, "default": "Component content..."}),
            },
            "optional": {
                "related_component_uids_str": ("STRING", {"multiline": False, "default": ""}), # Semicolon separated UIDs
                "specific_fields_json": ("STRING", {"multiline": True, "default": "{}"}), # JSON for specific fields
            }
        }

    def create_component(self, cycle_linkage_uid: str, component_type: str, name: str, description: str, content_text: str,
                               related_component_uids_str: Optional[str]=None,
                               specific_fields_json: Optional[str]=None):
        
        related_uids = [uid.strip() for uid in related_component_uids_str.split(';') if uid.strip()] if related_component_uids_str else []
        
        specific_fields_dict: Optional[Dict[str, Any]] = None
        if specific_fields_json and specific_fields_json.strip() != '{}':
            import json # Import locally to avoid class-level if not always needed
            try:
                specific_fields_dict = json.loads(specific_fields_json)
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON in specific_fields_json: {e}")

        print(f"CreateRDSOTMComponentNode: Adding {component_type} '{name}' to cycle {cycle_linkage_uid}")
        component_uid = create_rdsotm_component(
            cycle_linkage_uid=cycle_linkage_uid,
            component_type=component_type,
            name=name,
            description=description,
            content_text=content_text,
            related_component_uids=related_uids,
            specific_fields=specific_fields_dict
        )
        if component_uid is None:
            raise Exception(f"Failed to create RDSOTM component '{name}'. Check console.")
        print(f"CreateRDSOTMComponentNode: Component {component_uid} created.")
        return (cycle_linkage_uid, component_uid) # Pass through cycle_uid for chaining
