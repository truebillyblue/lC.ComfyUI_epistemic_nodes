import json
from ....lc_python_core.sops.meta_sops.sop_oia_cycle_management import get_oia_cycle_state

class ViewOiaCycleNode:
    CATEGORY = "LearntCloud/OIA"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("oia_cycle_summary",)
    FUNCTION = "view_cycle"
    OUTPUT_NODE = True # Typically view nodes are output nodes

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "oia_cycle_uid": ("STRING", {"forceInput": True}),
            }
        }

    def view_cycle(self, oia_cycle_uid: str):
        print(f"ViewOiaCycleNode: Calling get_oia_cycle_state for UID: {oia_cycle_uid}")
        cycle_state_dict = get_oia_cycle_state(oia_cycle_uid)
        summary = "OIA Cycle state not found or error in retrieval."
        if cycle_state_dict:
            try:
                summary = json.dumps(cycle_state_dict, indent=2)
            except TypeError:
                summary = "Error: OIA cycle state is not JSON serializable."
        
        # For console printing via the ShowTextNode pattern:
        print("--------------------------------")
        print(f"OIA Cycle State for {oia_cycle_uid}:")
        print("--------------------------------")
        print(summary)
        print("--------------------------------")
        # For direct UI display (if node has UI preview text element)
        return {"ui": {"text": [summary]}} # This allows text to be shown in some simple text widgets in ComfyUI if node has one
        # If not using UI preview, just return the summary string for connection
        # return (summary,) # If ShowTextNode is connected externally
