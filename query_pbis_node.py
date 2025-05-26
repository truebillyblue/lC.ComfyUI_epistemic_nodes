from typing import Optional, List, Dict, Any
import json
from lc_python_core.services.lc_mem_service import mock_lc_mem_core_query_objects, PBI_OBJECT_TYPE

class QueryPbisNode:
    CATEGORY = "LearntCloud/Backlog"
    RETURN_TYPES = ("STRING", "STRING",) # pbi_results_json, query_summary
    RETURN_NAMES = ("pbis_json", "summary",)
    FUNCTION = "query_pbis_from_mada"
    OUTPUT_NODE = True # Can act as an output/display node too

    @classmethod
    def INPUT_TYPES(s):
        # These mirror some of the query_params designed for lc_mem_service.query_pbis
        return {
            "optional": {
                "status": (["Any", "New", "Defined", "InProgress", "Blocked", "InReview", "Done", "Deferred", "Archived"], {"default": "Any"}),
                "priority": (["Any", "Lowest", "Low", "Medium", "High", "Highest", "Critical"], {"default": "Any"}),
                "pbi_type": (["Any", "Task", "UserStory", "Bug", "Feature", "Epic", "Initiative", "ResearchSpike", "Documentation", "FutureInquiry"], {"default": "Any"}),
                "cynefin_domain_context": (["Any", None, "Simple", "Complicated", "Complex", "Chaotic", "Disorder"], {"default": "Any"}), # Note: 'None' might not work well in ComfyUI dropdowns, might need a string like "None" or "Any"
                "related_oia_cycle_uid": ("STRING", {"multiline": False, "default": ""}),
                "related_rdsotm_cycle_linkage_uid": ("STRING", {"multiline": False, "default": ""}),
                "related_rdsotm_component_uid": ("STRING", {"multiline": False, "default": ""}),
                # Add other queryable fields as needed, e.g., assignee, tags
            }
        }

    def query_pbis_from_mada(self, **kwargs):
        query_params: Dict[str, Any] = {"object_type": PBI_OBJECT_TYPE} # Ensure we always query for PBIs

        for key, value in kwargs.items():
            # Handle 'None' string from ComfyUI dropdown if it was used for cynefin_domain_context
            if key == "cynefin_domain_context" and value == "None":
                value = None 
            
            if value is not None and value != "Any" and (not isinstance(value, str) or value.strip()):
                query_params[key] = value
            
        print(f"QueryPbisNode: Calling mock_lc_mem_core_query_objects with params: {query_params}")
        
        results_list = mock_lc_mem_core_query_objects(query_params=query_params, requesting_persona_context=None) # Persona context for query TBD

        results_json_str = "[]"
        summary_str = f"Found {len(results_list)} PBIs matching criteria."

        if results_list:
            try:
                results_json_str = json.dumps(results_list, indent=2)
            except TypeError:
                summary_str = f"Found {len(results_list)} PBIs, but they were not all JSON serializable for full output."
                # Fallback: try to get UIDs if full serialization fails
                try:
                    uids_only = [item.get("pbi_uid", str(item)) for item in results_list]
                    results_json_str = json.dumps(uids_only, indent=2)
                except Exception as e:
                     results_json_str = f"Error during fallback UID serialization: {e}"


        print(f"QueryPbisNode: {summary_str}")
        # For direct UI display in node:
        # ComfyUI's default text widget might not be large enough for many results.
        # It's better to output the string and use a ShowTextNode if the user wants to see it all.
        # The primary purpose of this node is to provide the JSON string as an output for other nodes.
        # However, if we want a UI preview for this node itself:
        # return {"ui": {"text": [summary_str + "\n\n" + results_json_str[:1000] + ("..." if len(results_json_str) > 1000 else "")]}}
        
        return (results_json_str, summary_str)
