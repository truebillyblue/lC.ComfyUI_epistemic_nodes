from typing import Optional, List
from lc_python_core.sops.meta_sops.sop_oia_cycle_management import add_interpretation_to_cycle

class AddInterpretationNode:
    CATEGORY = "LearntCloud/OIA"
    RETURN_TYPES = ("STRING", "STRING",) # oia_cycle_uid, interpretation_id
    RETURN_NAMES = ("oia_cycle_uid", "interpretation_id",)
    FUNCTION = "add_interpretation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "oia_cycle_uid": ("STRING", {"forceInput": True}),
                "summary": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "timeless_principles_extracted_str": ("STRING", {"multiline": True, "default": "Principle 1; Principle 2"}), # Semicolon separated
                "incongruence_flags_str": ("STRING", {"multiline": True, "default": "Flag 1; Flag 2"}), # Semicolon separated
                "references_observation_ids_str": ("STRING", {"multiline": False, "default": ""}), # Semicolon separated
            }
        }

    def add_interpretation(self, oia_cycle_uid: str, summary: str, 
                           timeless_principles_extracted_str: Optional[str]=None, 
                           incongruence_flags_str: Optional[str]=None, 
                           references_observation_ids_str: Optional[str]=None):
        
        principles = [p.strip() for p in timeless_principles_extracted_str.split(';') if p.strip()] if timeless_principles_extracted_str else []
        incongruences = [i.strip() for i in incongruence_flags_str.split(';') if i.strip()] if incongruence_flags_str else []
        ref_obs_ids = [r.strip() for r in references_observation_ids_str.split(';') if r.strip()] if references_observation_ids_str else []

        print(f"AddInterpretationNode: Adding to OIA Cycle UID: {oia_cycle_uid}")
        interpretation_id = add_interpretation_to_cycle(
            oia_cycle_uid=oia_cycle_uid,
            summary=summary,
            timeless_principles_extracted=principles,
            incongruence_flags=incongruences,
            references_observation_ids=ref_obs_ids
        )
        if interpretation_id is None:
            raise Exception("Failed to add interpretation. Check console.")
        print(f"AddInterpretationNode: Interpretation {interpretation_id} added.")
        return (oia_cycle_uid, interpretation_id)
