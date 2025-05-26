from typing import Optional
from lc_python_core.sops.sop_l4_anchor_click import anchor_click_process
from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting

class LcAnchorClickNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED",)
    RETURN_NAMES = ("mada_seed_L4",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L3
            },
            "optional": {
                "persona_profile_uid": ("STRING", {"multiline": False, "default": ""}), 
            }
        }

    def execute(self, mada_seed_in: MadaSeed, persona_profile_uid: Optional[str] = None):
        # The sop_l4_anchor_click.py expects persona_profile_uid as an Optional[str]
        # An empty string from ComfyUI should be treated as None if the SOP expects None for default.
        effective_persona_profile_uid = persona_profile_uid if persona_profile_uid and persona_profile_uid.strip() else None

        print(f"LcAnchorClickNode: Calling anchor_click_process with mada_seed and persona_profile_uid: {effective_persona_profile_uid}")
        
        mada_seed_result: MadaSeed = anchor_click_process(
            mada_seed_input=mada_seed_in, 
            persona_profile_uid_override_l4=effective_persona_profile_uid # Parameter name from L4 MR pseudo-code
        )
        
        print(f"LcAnchorClickNode: anchor_click_process returned.")
        return (mada_seed_result,)
