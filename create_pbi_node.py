from typing import Optional, List, Dict, Any
import json
from ....lc_python_core.services.lc_mem_service import create_pbi
# Potentially import PBI field enums if defined in a central schema place for ComfyUI dropdowns
# For now, using string inputs for enums and validating/casting in Python if necessary.

class CreatePbiNode:
    CATEGORY = "LearntCloud/Backlog" # New category for PBI/Backlog nodes
    RETURN_TYPES = ("STRING",) # new_pbi_uid
    RETURN_NAMES = ("pbi_uid",)
    FUNCTION = "create_new_pbi"

    @classmethod
    def INPUT_TYPES(s):
        # Based on PBI_Schema.md
        return {
            "required": {
                "title": ("STRING", {"multiline": False, "default": "New PBI Title"}),
                "pbi_type": (["Task", "UserStory", "Bug", "Feature", "Epic", "Initiative", "ResearchSpike", "Documentation", "FutureInquiry"], {"default": "Task"}),
                "status": (["New", "Defined", "InProgress", "Blocked", "InReview", "Done", "Deferred", "Archived"], {"default": "New"}),
                "priority": (["Lowest", "Low", "Medium", "High", "Highest", "Critical"], {"default": "Medium"}),
            },
            "optional": {
                "detailed_description": ("STRING", {"multiline": True, "default": ""}),
                "due_date": ("STRING", {"multiline": False, "default": ""}), # Expect ISO format string or empty
                "creator_persona_uid": ("STRING", {"multiline": False, "default": "urn:crux:uid::ComfyUIUser"}),
                "assignee_persona_uids_str": ("STRING", {"multiline": False, "default": ""}), # Semicolon separated
                "tags_keywords_str": ("STRING", {"multiline": False, "default": ""}), # Semicolon separated
                "cynefin_domain_context": ([None, "Simple", "Complicated", "Complex", "Chaotic", "Disorder"], {"default": None}),
                "pa_target_level_hint": ("STRING", {"multiline": False, "default": ""}), # e.g., L1, P5
                "pa_profile_ref_uid": ("STRING", {"multiline": False, "default": ""}),
                "learning_loop_type_hint": ([None, "Single", "Double", "Triple"], {"default": None}),
                "related_oia_cycle_uids_str": ("STRING", {"multiline": False, "default": ""}),
                "related_rdsotm_cycle_linkage_uids_str": ("STRING", {"multiline": False, "default": ""}),
                "related_rdsotm_component_uids_str": ("STRING", {"multiline": False, "default": ""}),
                "dependencies_pbi_uids_str": ("STRING", {"multiline": False, "default": ""}),
                "blocks_pbi_uids_str": ("STRING", {"multiline": False, "default": ""}),
                "acceptance_criteria": ("STRING", {"multiline": True, "default": ""}),
                "effort_estimate_story_points": ("FLOAT", {"default": 0.0, "min": 0.0}),
                "resolution_summary": ("STRING", {"multiline": True, "default": ""}),
                "view_context": ("STRING", {"multiline": False, "default": "Personal"}),
                "attachments_json_str": ("STRING", {"multiline": True, "default": "[]"}) # JSON string for list of attachments
            }
        }

    def _parse_str_list(self, str_list_input: Optional[str]) -> List[str]:
        if not str_list_input or not str_list_input.strip():
            return []
        return [item.strip() for item in str_list_input.split(';') if item.strip()]

    def create_new_pbi(self, title: str, pbi_type: str, status: str, priority: str, **kwargs):
        pbi_data: Dict[str, Any] = {
            "title": title,
            "pbi_type": pbi_type,
            "status": status,
            "priority": priority,
            "detailed_description": kwargs.get("detailed_description"),
            "due_date": kwargs.get("due_date") if kwargs.get("due_date") else None,
            "creator_persona_uid": kwargs.get("creator_persona_uid"),
            "assignee_persona_uids": self._parse_str_list(kwargs.get("assignee_persona_uids_str")),
            "tags_keywords": self._parse_str_list(kwargs.get("tags_keywords_str")),
            "cynefin_domain_context": kwargs.get("cynefin_domain_context"),
            "learning_loop_type_hint": kwargs.get("learning_loop_type_hint"),
            "related_oia_cycle_uids": self._parse_str_list(kwargs.get("related_oia_cycle_uids_str")),
            "related_rdsotm_cycle_linkage_uids": self._parse_str_list(kwargs.get("related_rdsotm_cycle_linkage_uids_str")),
            "related_rdsotm_component_uids": self._parse_str_list(kwargs.get("related_rdsotm_component_uids_str")),
            "dependencies_pbi_uids": self._parse_str_list(kwargs.get("dependencies_pbi_uids_str")),
            "blocks_pbi_uids": self._parse_str_list(kwargs.get("blocks_pbi_uids_str")),
            "acceptance_criteria": kwargs.get("acceptance_criteria"),
            "effort_estimate_story_points": kwargs.get("effort_estimate_story_points"),
            "resolution_summary": kwargs.get("resolution_summary"),
            "view_context": kwargs.get("view_context")
        }
        
        pa_level_hint = kwargs.get("pa_target_level_hint")
        pa_profile_uid = kwargs.get("pa_profile_ref_uid")
        if (pa_level_hint and pa_level_hint.strip()) or (pa_profile_uid and pa_profile_uid.strip()):
            pbi_data["persona_alignment_link"] = {
                "target_pa_level_hint": pa_level_hint if pa_level_hint and pa_level_hint.strip() else None,
                "pa_profile_ref_uid": pa_profile_uid if pa_profile_uid and pa_profile_uid.strip() else None
            }
        else:
            pbi_data["persona_alignment_link"] = None


        attachments_json_str = kwargs.get("attachments_json_str", "[]")
        try:
            attachments = json.loads(attachments_json_str)
            if isinstance(attachments, list):
                pbi_data["attachments"] = attachments
            else:
                pbi_data["attachments"] = []
                print("Warning: attachments_json_str was not a valid JSON list. Defaulting to empty list.")
        except json.JSONDecodeError:
            pbi_data["attachments"] = []
            print("Warning: attachments_json_str was not valid JSON. Defaulting to empty list.")


        # Remove None values for optional fields not provided, so they use schema defaults if any, or are just absent
        pbi_data_cleaned = {k: v for k, v in pbi_data.items() if v is not None and (not isinstance(v, list) or v)}


        print(f"CreatePbiNode: Calling create_pbi with data: {pbi_data_cleaned}")
        # Assuming persona_context is not strictly needed by the file-based create_pbi for now
        new_pbi_uid = create_pbi(pbi_data=pbi_data_cleaned, requesting_persona_context=None) 

        if new_pbi_uid is None:
            raise Exception("Failed to create PBI. Check console for errors from lc_python_core.")
        
        print(f"CreatePbiNode: PBI {new_pbi_uid} created.")
        return (new_pbi_uid,)

```
