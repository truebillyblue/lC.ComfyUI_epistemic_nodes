from typing import Optional
from ....lc_python_core.sops.meta_sops.sop_oia_cycle_management import initiate_oia_cycle

class InitiateOiaNode:
    CATEGORY = "LearntCloud/OIA"
    RETURN_TYPES = ("STRING",) # oia_cycle_uid
    RETURN_NAMES = ("oia_cycle_uid",)
    FUNCTION = "start_cycle"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "cycle_name": ("STRING", {"multiline": False, "default": "New OIA Cycle"}),
                "initial_focus_prompt": ("STRING", {"multiline": True, "default": ""}),
                "related_trace_id": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    def start_cycle(self, cycle_name: Optional[str]=None, initial_focus_prompt: Optional[str]=None, related_trace_id: Optional[str]=None):
        effective_name = cycle_name if cycle_name and cycle_name.strip() else None
        effective_prompt = initial_focus_prompt if initial_focus_prompt and initial_focus_prompt.strip() else None
        effective_trace_id = related_trace_id if related_trace_id and related_trace_id.strip() else None
        
        print(f"InitiateOiaNode: Calling initiate_oia_cycle with name: {effective_name}, prompt: {effective_prompt}, trace: {effective_trace_id}")
        oia_cycle_uid = initiate_oia_cycle(
            name=effective_name,
            initial_focus_prompt=effective_prompt,
            related_trace_id=effective_trace_id
        )
        if oia_cycle_uid is None:
            # Raise an exception or return an error tuple to ComfyUI
            raise Exception("Failed to initiate OIA cycle. Check console for errors from lc_python_core.")
        print(f"InitiateOiaNode: OIA Cycle UID {oia_cycle_uid} initiated.")
        return (oia_cycle_uid,)
