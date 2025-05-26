from typing import Optional
from ....lc_python_core.sops.meta_sops.sop_rdsotm_management import initiate_rdsotm_cycle

class InitiateRDSOTMCycleNode:
    CATEGORY = "LearntCloud/RDSOTM"
    RETURN_TYPES = ("STRING",) # cycle_linkage_uid
    RETURN_NAMES = ("cycle_linkage_uid",)
    FUNCTION = "initiate_cycle"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "cycle_name": ("STRING", {"multiline": False, "default": "New RDSOTM Cycle"}),
            }
        }

    def initiate_cycle(self, cycle_name: Optional[str]=None):
        effective_name = cycle_name if cycle_name and cycle_name.strip() else "Default RDSOTM Cycle"
        
        print(f"InitiateRDSOTMCycleNode: Calling initiate_rdsotm_cycle with name: {effective_name}")
        cycle_uid = initiate_rdsotm_cycle(name=effective_name)

        if cycle_uid is None:
            raise Exception("Failed to initiate RDSOTM cycle. Check console.")
        print(f"InitiateRDSOTMCycleNode: RDSOTM Cycle UID {cycle_uid} initiated.")
        return (cycle_uid,)
