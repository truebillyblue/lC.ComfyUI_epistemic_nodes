from lc_python_core.sops.sop_l3_keymap_click import keymap_click_process
from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting

class LcKeymapClickNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED",)
    RETURN_NAMES = ("mada_seed_L3",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L2
            }
            # No other inputs specified for L3 in the issue description
        }

    def execute(self, mada_seed_in: MadaSeed):
        print(f"LcKeymapClickNode: Calling keymap_click_process with mada_seed.")
        
        # Call the L3 SOP function from lc_python_core
        # keymap_click_process is expected to take MadaSeed and return a MadaSeed object
        mada_seed_result: MadaSeed = keymap_click_process(mada_seed_input=mada_seed_in)
        
        print(f"LcKeymapClickNode: keymap_click_process returned.")
        return (mada_seed_result,)
