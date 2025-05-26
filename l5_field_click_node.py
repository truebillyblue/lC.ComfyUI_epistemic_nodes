from typing import Optional
from lc_python_core.sops.sop_l5_field_click import field_click_process
from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting

class LcFieldClickNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED",)
    RETURN_NAMES = ("mada_seed_L5",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L4
            },
            "optional": {
                "field_instance_uid_override": ("STRING", {"multiline": False, "default": ""}), 
            }
        }

    def execute(self, mada_seed_in: MadaSeed, field_instance_uid_override: Optional[str] = None):
        effective_field_instance_uid_override = field_instance_uid_override if field_instance_uid_override and field_instance_uid_override.strip() else None

        print(f"LcFieldClickNode: Calling field_click_process with mada_seed and field_instance_uid_override: {effective_field_instance_uid_override}")
        
        # The L5 SOP Python function expects `field_instance_uid_override_l5`
        mada_seed_result: MadaSeed = field_click_process(
            mada_seed_input=mada_seed_in, 
            field_instance_uid_override_l5=effective_field_instance_uid_override
        )
        
        print(f"LcFieldClickNode: field_click_process returned.")
        return (mada_seed_result,)
