from typing import Optional, List
from lc_python_core.sops.meta_sops.sop_oia_cycle_management import add_application_to_cycle

class AddApplicationNode:
    CATEGORY = "LearntCloud/OIA"
    RETURN_TYPES = ("STRING", "STRING",) # oia_cycle_uid, application_id
    RETURN_NAMES = ("oia_cycle_uid", "application_id",)
    FUNCTION = "add_application"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "oia_cycle_uid": ("STRING", {"forceInput": True}),
                "summary_of_action": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "target_mada_uid": ("STRING", {"multiline": False, "default": ""}),
                "outcome_mada_seed_trace_id": ("STRING", {"multiline": False, "default": ""}),
                "references_interpretation_ids_str": ("STRING", {"multiline": False, "default": ""}), # Semicolon separated
            }
        }

    def add_application(self, oia_cycle_uid: str, summary_of_action: str,
                        target_mada_uid: Optional[str]=None,
                        outcome_mada_seed_trace_id: Optional[str]=None,
                        references_interpretation_ids_str: Optional[str]=None):

        effective_target_uid = target_mada_uid if target_mada_uid and target_mada_uid.strip() else None
        effective_outcome_trace_id = outcome_mada_seed_trace_id if outcome_mada_seed_trace_id and outcome_mada_seed_trace_id.strip() else None
        ref_interp_ids = [r.strip() for r in references_interpretation_ids_str.split(';') if r.strip()] if references_interpretation_ids_str else []

        print(f"AddApplicationNode: Adding to OIA Cycle UID: {oia_cycle_uid}")
        application_id = add_application_to_cycle(
            oia_cycle_uid=oia_cycle_uid,
            summary_of_action_taken_or_planned=summary_of_action,
            target_mada_uid=effective_target_uid,
            outcome_mada_seed_trace_id=effective_outcome_trace_id,
            references_interpretation_ids=ref_interp_ids
        )
        if application_id is None:
            raise Exception("Failed to add application. Check console.")
        print(f"AddApplicationNode: Application {application_id} added.")
        return (oia_cycle_uid, application_id)
