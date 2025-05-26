from typing import Optional
from lc_python_core.sops.meta_sops.sop_oia_cycle_management import add_observation_to_cycle

class AddObservationNode:
    CATEGORY = "LearntCloud/OIA"
    RETURN_TYPES = ("STRING", "STRING",) # oia_cycle_uid, observation_id
    RETURN_NAMES = ("oia_cycle_uid", "observation_id",)
    FUNCTION = "add_observation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "oia_cycle_uid": ("STRING", {"forceInput": True}),
                "summary": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "data_source_mada_uid": ("STRING", {"multiline": False, "default": ""}),
                "raw_observation_ref": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    def add_observation(self, oia_cycle_uid: str, summary: str, data_source_mada_uid: Optional[str]=None, raw_observation_ref: Optional[str]=None):
        effective_data_source = data_source_mada_uid if data_source_mada_uid and data_source_mada_uid.strip() else None
        effective_raw_ref = raw_observation_ref if raw_observation_ref and raw_observation_ref.strip() else None
        
        print(f"AddObservationNode: Adding to OIA Cycle UID: {oia_cycle_uid}")
        observation_id = add_observation_to_cycle(
            oia_cycle_uid=oia_cycle_uid,
            summary=summary,
            data_source_mada_uid=effective_data_source,
            raw_observation_ref=effective_raw_ref
        )
        if observation_id is None:
            raise Exception("Failed to add observation to OIA cycle. Check console.")
        print(f"AddObservationNode: Observation {observation_id} added.")
        return (oia_cycle_uid, observation_id) # Pass through UID for chaining
