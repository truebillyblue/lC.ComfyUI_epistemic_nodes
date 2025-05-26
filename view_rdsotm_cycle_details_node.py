import json
from typing import Optional
from ....lc_python_core.sops.meta_sops.sop_rdsotm_management import get_rdsotm_cycle_details

class ViewRDSOTMCycleDetailsNode:
    CATEGORY = "LearntCloud/RDSOTM"
    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("cycle_details_json",)
    FUNCTION = "view_details"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cycle_linkage_uid": ("STRING", {"forceInput": True}),
                "resolve_component_summaries": ("BOOLEAN", {"default": True}),
            }
        }

    def view_details(self, cycle_linkage_uid: str, resolve_component_summaries: bool):
        print(f"ViewRDSOTMCycleDetailsNode: Calling get_rdsotm_cycle_details for UID: {cycle_linkage_uid}")
        
        cycle_details_dict = get_rdsotm_cycle_details(
            cycle_linkage_uid=cycle_linkage_uid,
            resolve_component_summaries=resolve_component_summaries
        )
        
        summary_str = f"RDSOTM Cycle details for {cycle_linkage_uid} not found or error in retrieval."
        if cycle_details_dict:
            try:
                summary_str = json.dumps(cycle_details_dict, indent=2)
            except TypeError:
                summary_str = f"Error: RDSOTM Cycle details for {cycle_linkage_uid} are not JSON serializable."
        
        print("--------------------------------")
        print(f"RDSOTM Cycle Details for {cycle_linkage_uid}:")
        print("--------------------------------")
        print(summary_str)
        print("--------------------------------")
        
        return {"ui": {"text": [summary_str]}} # For direct UI display in node
        # Alternatively, to output as a string for ShowTextNode:
        # return (summary_str,)
