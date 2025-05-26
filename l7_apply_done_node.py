from typing import Optional, Dict, Any
import json # For potentially summarizing complex objects as JSON string

from lc_python_core.sops.sop_l7_apply_done import apply_done_process
from lc_python_core.schemas.mada_schema import MadaSeed, L7EncodedApplication, SeedQAQC # For type hinting

class LcApplyDoneNode:
    CATEGORY = "LearntCloud/EpistemicOSI"
    RETURN_TYPES = ("MADA_SEED", "STRING", "STRING",)
    RETURN_NAMES = ("final_mada_seed", "application_summary_text", "next_step_options_text",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mada_seed_in": ("MADA_SEED",), # Input is the MadaSeed object from L6
            },
            "optional": {
                "l7_action_intent_override": ("STRING", {"multiline": False, "default": ""}), 
            }
        }

    def execute(self, mada_seed_in: MadaSeed, l7_action_intent_override: Optional[str] = None):
        effective_l7_action_intent_override = l7_action_intent_override if l7_action_intent_override and l7_action_intent_override.strip() else None

        print(f"LcApplyDoneNode: Calling apply_done_process with mada_seed and l7_action_intent_override: {effective_l7_action_intent_override}")
        
        # The L7 SOP Python function expects `l7_action_intent_override_l7`
        # and the input mada_seed is actually the L6 output package in the doctrinal sense.
        # The python function `apply_done_process` takes `l6_output_package` as its parameter name.
        # We will pass the mada_seed_in as this l6_output_package.
        
        # To conform to the Python function's parameter name `l6_output_package`:
        l6_package_equivalent = {
            "trace_id": mada_seed_in.seed_id, # Assuming trace_id is seed_id
            "raw_signal_refs": mada_seed_in.seed_content.raw_signals if mada_seed_in.seed_content else [], # Or however raw_signal_refs are passed
            "trace_metadata": mada_seed_in.trace_metadata, # Pass the whole trace_metadata
             # The L7 sop expects 'reflection_payload' within 'trace_metadata' of the l6_output_package.
             # We need to ensure the L6 node correctly places its L6ReflectionPayloadObj there.
             # For now, we assume mada_seed_in.trace_metadata.L6_trace contains what's needed,
             # or more accurately, that mada_seed_in (as a whole) is structured such that
             # apply_done_process can find the L6_reflection_payload_obj.
             # The L6 node stores its output in mada_seed_result.seed_content...L6_reflection_payload.L6_reflection_payload_obj
             # The L7 sop `apply_done_process` expects `l6_reflection_payload` directly from `l6_output_package['trace_metadata']['reflection_payload']`
             # This implies a structural mismatch to resolve.
             # For now, let's assume apply_done_process is adapted or we prepare a specific dict.
        }
        
        # Given the current apply_done_process signature: `apply_done_process(l6_output_package: Dict)`
        # We need to construct this dictionary.
        # The L6 node's output is a MadaSeed. The L7 SOP expects a dict.
        # The L7 SOP's MR logic for apply_done_process(l6_output_package: Dict)
        # accesses l6_output_package['trace_metadata']['reflection_payload']
        # So, mada_seed_in (which is the MadaSeed object from L6) needs to be transformed.

        # Simplification: The Python L7 SOP `apply_done_process` was defined to take the L6 MadaSeed object directly.
        # Let's assume the `apply_done_process` in `sop_l7_apply_done.py` was updated to accept `mada_seed_input: MadaSeed`
        # similar to other SOPs, and internally it accesses `mada_seed_input.seed_content...L6_reflection_payload_obj`.
        # If not, this node would need to construct the specific dict structure that `apply_done_process` expects.
        # For this implementation, we proceed with the assumption that `apply_done_process` takes `MadaSeed`.
        # (This might need adjustment after reviewing `sop_l7_apply_done.py` in detail in the next plan step)

        # If apply_done_process expects a MadaSeed:
        final_mada_seed_result: MadaSeed = apply_done_process(
            mada_seed_input=mada_seed_in, # Assuming apply_done_process was updated for MadaSeed input
            l7_action_intent_override_l7=effective_l7_action_intent_override
        )

        app_summary = "No L7 application summary found."
        next_steps = "No next step options provided."

        try:
            if final_mada_seed_result.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L7_encoded_application:
                l7_app: L7EncodedApplication = final_mada_seed_result.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L7_encoded_application
                
                # Summarize L7 action and seed QA/QC
                qa_qc_summary = "QA/QC: " + (final_mada_seed_result.seed_QA_QC.overall_seed_integrity_status.value if final_mada_seed_result.seed_QA_QC else "Status N/A")
                
                action_summary_parts = []
                if l7_app.L7_backlog and (l7_app.L7_backlog.single_loop or l7_app.L7_backlog.double_loop or l7_app.L7_backlog.triple_loop):
                    action_summary_parts.append(f"Backlog items updated/created.")
                
                if l7_app.seed_outputs:
                    action_summary_parts.append(f"{len(l7_app.seed_outputs)} output stream(s) generated.")
                    
                    # Check for ADK agent output specifically
                    for output_item in l7_app.seed_outputs:
                        if isinstance(output_item.target_consumer_hint, dict) and \
                           output_item.target_consumer_hint.get("invoked_agent") == "lc_adk_agent":
                            adk_output_summary = "ADK agent output present."
                            if isinstance(output_item.content, str) and len(output_item.content) < 100: # Show short ADK outputs
                                adk_output_summary = f"ADK Agent Output: '{output_item.content[:100]}'" # Removed ellipsis as it's <100
                            elif isinstance(output_item.content, str):
                                adk_output_summary = f"ADK Agent Output (summary): '{output_item.content[:100]}...'"
                            action_summary_parts.append(adk_output_summary)
                            break # Assuming only one ADK output for now

                    # For next_step_options_text, concatenate labels from the first output stream's options
                    if l7_app.seed_outputs and l7_app.seed_outputs[0].seed_options and l7_app.seed_outputs[0].seed_options.options:
                        next_steps_list = [opt.label for opt in l7_app.seed_outputs[0].seed_options.options]
                        if next_steps_list:
                            next_steps = "Next Steps: " + " | ".join(next_steps_list)
                        else:
                            next_steps = "No specific next step options defined in first output."
                    else:
                         next_steps = "No seed_options found in the first output."

                app_summary = f"[L7 State: {final_mada_seed_result.trace_metadata.L7_trace.epistemic_state_L7.value if final_mada_seed_result.trace_metadata.L7_trace else 'N/A'}] "
                app_summary += qa_qc_summary
                if action_summary_parts:
                    app_summary += " | Actions: " + "; ".join(action_summary_parts)
                else:
                    app_summary += " | No specific actions logged in L7_encoded_application."


        except AttributeError as e:
            print(f"LcApplyDoneNode: Error accessing L7 payload for summary: {e}")
            app_summary = "Error accessing L7 application payload."
        except Exception as e:
            print(f"LcApplyDoneNode: Unexpected error creating summary: {e}")
            app_summary = "Unexpected error creating L7 summary."

        print(f"LcApplyDoneNode: apply_done_process returned.")
        return (final_mada_seed_result, app_summary, next_steps)
