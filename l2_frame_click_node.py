from typing import Optional, Dict, Any
from lc_python_core.sops.sop_l2_frame_click import frame_click_process
from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting

class LcFrameClickNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED",)
    RETURN_NAMES = ("mada_seed_L2",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L1
                "communication_context_hints": ("STRING", {"multiline": True, "default": "{}"}), # JSON string for hints
            }
        }

    def execute(self, mada_seed_in: MadaSeed, communication_context_hints: str):
        # communication_context_hints is expected to be a JSON string by the SOP pseudo-code.
        # The actual Python function sop_l2_frame_click.py expects a Dict.
        # For now, we'll assume the user provides a valid JSON string for the hints,
        # or the Python function handles a string appropriately.
        # Ideally, the Python function should parse the JSON string if that's the contract.
        # Based on the pseudo-code for L2, `communication_context_hints` is a direct pass-through
        # to the python function, which then uses it.
        # The current `sop_l2_frame_click.py` expects `input_event_comm_context_conceptual: Optional[Dict[str, Any]]`
        # So we should parse the JSON string to a Dict here.
        
        import json
        comm_context_hints_dict: Optional[Dict[str, Any]] = None
        if communication_context_hints and communication_context_hints.strip():
            try:
                comm_context_hints_dict = json.loads(communication_context_hints)
            except json.JSONDecodeError as e:
                print(f"LcFrameClickNode: Error decoding communication_context_hints JSON: {e}")
                # Potentially pass None or raise an error, depending on desired behavior
                # For now, pass None if JSON is invalid, L2 SOP might have defaults.
                pass # comm_context_hints_dict remains None

        print(f"LcFrameClickNode: Calling frame_click_process with mada_seed and hints_dict: {comm_context_hints_dict}")
        
        # Call the L2 SOP function from lc_python_core
        # frame_click_process is expected to take MadaSeed and Dict, and return a MadaSeed object
        mada_seed_result: MadaSeed = frame_click_process(mada_seed_input=mada_seed_in, input_event_comm_context_conceptual=comm_context_hints_dict)
        
        print(f"LcFrameClickNode: frame_click_process returned.")
        return (mada_seed_result,)
