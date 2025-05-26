from typing import Optional, Dict, Any
from datetime import datetime, timezone
import json

# Import all SOP processes and the MadaSeed schema
from ....lc_python_core.schemas.mada_schema import MadaSeed
from ....lc_python_core.sops.sop_l1_startle import startle_process
from ....lc_python_core.sops.sop_l2_frame_click import frame_click_process
from ....lc_python_core.sops.sop_l3_keymap_click import keymap_click_process
from ....lc_python_core.sops.sop_l4_anchor_click import anchor_click_process
from ....lc_python_core.sops.sop_l5_field_click import field_click_process
from ....lc_python_core.sops.sop_l6_reflect_boom import reflect_boom_process
from ....lc_python_core.sops.sop_l7_apply_done import apply_done_process

class LcEpistemicPipelineNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("final_mada_seed", "trace_id", "l6_reflection_summary", "l7_application_summary", "l7_next_steps",)
    FUNCTION = "execute_pipeline"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "l1_origin_hint": ("STRING", {"multiline": False, "default": "ComfyUI_LcPipelineNode"}),
                "l1_optional_attachments_ref": ("STRING", {"multiline": False, "default": ""}),
                "l2_communication_context_hints": ("STRING", {"multiline": True, "default": "{}"}), # JSON string
                "l4_persona_profile_uid_override": ("STRING", {"multiline": False, "default": ""}),
                "l5_field_instance_uid_override": ("STRING", {"multiline": False, "default": ""}),
                "l6_presentation_intent_override": ("STRING", {"multiline": False, "default": ""}),
                "l7_action_intent_override": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    def execute_pipeline(self, input_text: str, 
                         l1_origin_hint: Optional[str] = None, 
                         l1_optional_attachments_ref: Optional[str] = None,
                         l2_communication_context_hints: Optional[str] = None,
                         l4_persona_profile_uid_override: Optional[str] = None,
                         l5_field_instance_uid_override: Optional[str] = None,
                         l6_presentation_intent_override: Optional[str] = None,
                         l7_action_intent_override: Optional[str] = None):

        print("LcEpistemicPipelineNode: Starting L1 Startle...")
        # L1 Startle
        input_event = {
            "reception_timestamp_utc_iso": datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'),
            "origin_hint": l1_origin_hint,
            "data_components": [{"role_hint": "primary_text_content", "content_handle_placeholder": input_text, "size_hint": len(input_text.encode('utf-8')), "type_hint": "text/plain"}]
        }
        if l1_optional_attachments_ref:
            input_event["data_components"].append({"role_hint": "attachment_reference", "content_handle_placeholder": l1_optional_attachments_ref, "size_hint": len(l1_optional_attachments_ref.encode('utf-8')), "type_hint": "text/uri-reference"})
        
        current_mada_seed: MadaSeed = startle_process(input_event)
        trace_id = current_mada_seed.trace_metadata.L1_trace.L1_generated_trace_id if current_mada_seed.trace_metadata.L1_trace else current_mada_seed.seed_id
        print(f"L1 Complete. Trace ID: {trace_id}")

        # L2 FrameClick
        print("LcEpistemicPipelineNode: Starting L2 FrameClick...")
        comm_context_hints_dict: Optional[Dict[str, Any]] = None
        if l2_communication_context_hints and l2_communication_context_hints.strip():
            try: comm_context_hints_dict = json.loads(l2_communication_context_hints)
            except json.JSONDecodeError as e: print(f"Pipeline L2: Invalid JSON for comm_context_hints: {e}")
        current_mada_seed = frame_click_process(current_mada_seed, comm_context_hints_dict)
        print("L2 Complete.")

        # L3 KeymapClick
        print("LcEpistemicPipelineNode: Starting L3 KeymapClick...")
        current_mada_seed = keymap_click_process(current_mada_seed)
        print("L3 Complete.")

        # L4 AnchorClick
        print("LcEpistemicPipelineNode: Starting L4 AnchorClick...")
        eff_persona_uid = l4_persona_profile_uid_override if l4_persona_profile_uid_override and l4_persona_profile_uid_override.strip() else None
        current_mada_seed = anchor_click_process(current_mada_seed, eff_persona_uid)
        print("L4 Complete.")

        # L5 FieldClick
        print("LcEpistemicPipelineNode: Starting L5 FieldClick...")
        eff_field_uid = l5_field_instance_uid_override if l5_field_instance_uid_override and l5_field_instance_uid_override.strip() else None
        current_mada_seed = field_click_process(current_mada_seed, eff_field_uid)
        print("L5 Complete.")

        # L6 ReflectBoom
        print("LcEpistemicPipelineNode: Starting L6 ReflectBoom...")
        eff_pres_intent = l6_presentation_intent_override if l6_presentation_intent_override and l6_presentation_intent_override.strip() else None
        current_mada_seed = reflect_boom_process(current_mada_seed, eff_pres_intent)
        l6_summary = "L6: No text content in reflection payload."
        try:
            l6_payload_obj = current_mada_seed.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L6_reflection_payload_obj
            if l6_payload_obj and l6_payload_obj.payload_content:
                if l6_payload_obj.payload_content.formatted_text:
                    l6_summary = l6_payload_obj.payload_content.formatted_text
                elif l6_payload_obj.payload_content.structured_data:
                    l6_summary = json.dumps(l6_payload_obj.payload_content.structured_data, indent=2)
            l6_summary = f"[L6 State: {l6_payload_obj.l6_epistemic_state.name if l6_payload_obj.l6_epistemic_state else 'N/A'}]\n{l6_summary}"
        except Exception: pass # Keep default summary
        print("L6 Complete.")

        # L7 ApplyDone
        print("LcEpistemicPipelineNode: Starting L7 ApplyDone...")
        eff_l7_intent = l7_action_intent_override if l7_action_intent_override and l7_action_intent_override.strip() else None
        final_mada_seed = apply_done_process(current_mada_seed, eff_l7_intent)
        l7_summary = "L7: No summary."
        l7_next_steps = "L7: No next steps."
        try:
            l7_app_obj = final_mada_seed.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L7_encoded_application
            qa_qc_summary = "QA/QC: " + (final_mada_seed.seed_QA_QC.overall_seed_integrity_status.name if final_mada_seed.seed_QA_QC and final_mada_seed.seed_QA_QC.overall_seed_integrity_status else "N/A")
            action_summary_parts = []
            if l7_app_obj and l7_app_obj.seed_outputs: action_summary_parts.append(f"{len(l7_app_obj.seed_outputs)} output(s).")
            l7_summary = f"[L7 State: {final_mada_seed.trace_metadata.L7_trace.epistemic_state_L7.name if final_mada_seed.trace_metadata.L7_trace and final_mada_seed.trace_metadata.L7_trace.epistemic_state_L7 else 'N/A'}] {qa_qc_summary} {' '.join(action_summary_parts)}"
            if l7_app_obj and l7_app_obj.seed_outputs and l7_app_obj.seed_outputs[0].seed_options and l7_app_obj.seed_outputs[0].seed_options.options:
                l7_next_steps = "Options: " + " | ".join([opt.label for opt in l7_app_obj.seed_outputs[0].seed_options.options])
        except Exception: pass # Keep default summaries
        print("L7 Complete. Pipeline finished.")

        return (final_mada_seed, trace_id, l6_summary, l7_summary, l7_next_steps)
