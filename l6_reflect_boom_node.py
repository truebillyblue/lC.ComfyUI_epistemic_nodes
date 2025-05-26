from typing import Optional, Dict, Any
import json # For potentially summarizing complex objects as JSON string

from lc_python_core.sops.sop_l6_reflect_boom import reflect_boom_process
from lc_python_core.schemas.mada_schema import MadaSeed, L6ReflectionPayloadObj # For type hinting

class LcReflectBoomNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED", "STRING",)
    RETURN_NAMES = ("mada_seed_L6", "reflection_text_summary",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L5
            },
            "optional": {
                "presentation_intent_override": ("STRING", {"multiline": False, "default": ""}), 
            }
        }

    def execute(self, mada_seed_in: MadaSeed, presentation_intent_override: Optional[str] = None):
        effective_presentation_intent_override = presentation_intent_override if presentation_intent_override and presentation_intent_override.strip() else None

        print(f"LcReflectBoomNode: Calling reflect_boom_process with mada_seed and presentation_intent_override: {effective_presentation_intent_override}")
        
        # The L6 SOP Python function expects `presentation_intent_override_l6`
        mada_seed_result: MadaSeed = reflect_boom_process(
            mada_seed_input=mada_seed_in, 
            presentation_intent_override_l6=effective_presentation_intent_override
        )
        
        reflection_summary = "No L6 reflection payload content found or content is not text."
        try:
            if mada_seed_result.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload:
                l6_payload: L6ReflectionPayloadObj = mada_seed_result.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L6_reflection_payload_obj
                
                # Attempt to extract a human-readable summary
                if l6_payload.payload_content:
                    if l6_payload.payload_content.formatted_text:
                        reflection_summary = l6_payload.payload_content.formatted_text
                    elif l6_payload.payload_content.structured_data:
                        # Summarize structured data as JSON string for now
                        try:
                            reflection_summary = json.dumps(l6_payload.payload_content.structured_data, indent=2)
                        except TypeError:
                            reflection_summary = "L6 Payload (structured_data) is not JSON serializable."
                    elif l6_payload.payload_content.multimodal_package:
                        reflection_summary = f"L6 Payload: Multimodal package with {len(l6_payload.payload_content.multimodal_package)} components."
                    elif l6_payload.payload_content.api_payload:
                         reflection_summary = f"L6 Payload: API Payload provided."
                
                # Add L6 epistemic state to summary
                reflection_summary = f"[L6 State: {l6_payload.l6_epistemic_state}]\n{reflection_summary}"

        except AttributeError as e:
            print(f"LcReflectBoomNode: Error accessing L6 payload for summary: {e}")
            reflection_summary = "Error accessing L6 reflection payload."
        except Exception as e: # Catch any other unexpected error during summary creation
            print(f"LcReflectBoomNode: Unexpected error creating summary: {e}")
            reflection_summary = "Unexpected error creating L6 summary."


        print(f"LcReflectBoomNode: reflect_boom_process returned.")
        return (mada_seed_result, reflection_summary)
