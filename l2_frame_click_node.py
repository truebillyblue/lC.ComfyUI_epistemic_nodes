import json
from typing import Any, Dict, List, Tuple, Optional # Keep standard typing imports
from datetime import datetime # Keep standard datetime

# Placeholder for actual imports, to be populated correctly by the node's logic
# This try-except is for runtime resilience if lc_python_core is not perfectly set up.
IMPORTS_OK = False
PYDANTIC_AVAILABLE_L2 = False # Local flag for this node

try:
    from lc_python_core.mada_seed_types import (
        MadaSeed, 
        PYDANTIC_AVAILABLE as CORE_PYDANTIC_AVAILABLE, # Get the flag from the core types
        L2FrameTypeObj, # Needed for extracting output fields
        L2EpistemicStateOfFramingEnum # Needed for output state
    )
    from lc_python_core.sops.sop_l2_frame_click import frame_click_process
    IMPORTS_OK = True
    PYDANTIC_AVAILABLE_L2 = CORE_PYDANTIC_AVAILABLE 
    print("[LcFrameClickNode] Successfully imported types and SOP from lc_python_core.")
except ImportError as e:
    print(f"[LcFrameClickNode] ERROR: Failed to import from lc_python_core: {e!r}. Using dummy classes for LcFrameClickNode.")
    
    # Define minimal dummy classes if imports fail, to allow ComfyUI to load the node
    # These are specific to LcFrameClickNode's direct needs for error reporting / basic structure
    PYDANTIC_AVAILABLE_L2 = False

    class MadaSeed: # Minimal dummy
        def __init__(self, seed_id="ERROR_SEED_ID_L2_IMPORT_FAIL", **kwargs):
            self.seed_id = seed_id
            # Simulate the nested structure enough for error reporting path in execute to work
            self.seed_content = type('SeedContent', (object,), {
                'L1_startle_reflex': type('L1StartleReflex', (object,), {
                    'L2_frame_type': type('L2FrameTypeContainer', (object,), {
                        'L2_frame_type_obj': None # Will be set to an error obj
                    })
                })
            })()
            self.trace_metadata = type('TraceMetadata', (object,), {'L2_trace': None})()
            self.error_details_L2_node = "LcFrameClickNode failed to import lc_python_core. Check console for specific import error details."

        def model_dump_json(self, indent=None): # match Pydantic method
            # Crude serialization for the dummy
            error_obj = {
                "seed_id": self.seed_id, 
                "error": "ImportError in LcFrameClickNode",
                "details": self.error_details_L2_node
            }
            if self.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj:
                 error_obj["L2_frame_type_obj_error"] = self.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj.__dict__

            return json.dumps(error_obj, indent=indent)

    class L2FrameTypeObj: # Dummy for L2 object
        def __init__(self, version="error", frame_type_L2="error", L2_epistemic_state_of_framing="error", error_details="dummy L2FrameTypeObj due to import fail"):
            self.version = version
            self.frame_type_L2 = frame_type_L2
            self.L2_epistemic_state_of_framing = L2_epistemic_state_of_framing
            self.error_details = error_details

    class L2EpistemicStateOfFramingEnum: # Dummy Enum
        FRAMED = "Framed_Node_Import_Fail"
        LCL_CLARIFY_STRUCTURE = "LCL-Clarify-Structure_Node_Import_Fail"
        LCL_DEFER_STRUCTURE = "LCL-Defer-Structure_Node_Import_Fail"
        LCL_FAILURE_SIZE_NOISE = "LCL-Failure-SizeNoise_Node_Import_Fail"
        LCL_FAILURE_AMBIGUOUS_FRAME = "LCL-Failure-AmbiguousFrame_Node_Import_Fail"
        LCL_FAILURE_MISSING_COMMS_CONTEXT = "LCL-Failure-MissingCommsContext_Node_Import_Fail"
        LCL_FAILURE_INTERNAL_L2 = "LCL-Failure-Internal_L2_Node_Import_Fail" # Existing one, slightly modified for consistency

    def frame_click_process(mada_seed_input): # Dummy process
        print("[LcFrameClickNode] Called DUMMY frame_click_process.")
        # Simulate error population in the dummy MadaSeed
        if hasattr(mada_seed_input, 'seed_content') and mada_seed_input.seed_content:
            error_l2_obj = L2FrameTypeObj(
                error_details=f"Dummy frame_click_process called due to import failure. Original error: {getattr(mada_seed_input, 'error_details_L2_node', 'Unknown import error')}"
            )
            mada_seed_input.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj = error_l2_obj
        # Ensure it has a seed_id if it's the dummy from this file
        if not hasattr(mada_seed_input, 'seed_id') or not mada_seed_input.seed_id.startswith("ERROR_SEED_ID"):
             mada_seed_input.seed_id = "ERROR_SEED_ID_L2_DUMMY_PROCESS"

        return mada_seed_input

class LcFrameClickNode:
    NODE_NAME = "LcFrameClickNode"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mada_seed_L1_json": ("STRING", {"default": "{}", "multiline": True, "dynamicPrompts": False}),
                "trace_id_L1": ("STRING", {"default": "N/A", "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("mada_seed_L2", "trace_id", "l2_frame_type", "l2_epistemic_state",)
    FUNCTION = "execute"
    CATEGORY = "learnt.cloud/Epistemic"

    def execute(self, mada_seed_L1_json: str, trace_id_L1: str):
        print(f"=== [{self.NODE_NAME}] execute() PYTHON LOGIC ===")
        
        current_trace_id = trace_id_L1 if trace_id_L1 != "N/A" else "UNKNOWN_TRACE_AT_L2_EXEC_START"
        current_mada_seed_obj = None
        error_prefix = f"[{self.NODE_NAME}] ERROR:"

        if not IMPORTS_OK:
            # Imports failed during node loading, use dummy MadaSeed to report this
            current_mada_seed_obj = MadaSeed(seed_id=current_trace_id) 
            # error_details_L2_node is already set in the dummy MadaSeed __init__ from the import error
            
            # The dummy frame_click_process will further note that it's a dummy call
            current_mada_seed_obj = frame_click_process(current_mada_seed_obj)
            
            # Extract what we can for return types from the dummy structure
            l2_frame_type_str = "L2_IMPORT_ERROR"
            l2_epistemic_state_str = "L2_IMPORT_ERROR"
            
            # Access dummy attributes carefully
            try:
                l2_obj = current_mada_seed_obj.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj
                if l2_obj:
                    l2_frame_type_str = str(getattr(l2_obj, 'frame_type_L2', 'L2_IMPORT_ERROR_FT'))
                    l2_epistemic_state_str = str(getattr(l2_obj, 'L2_epistemic_state_of_framing', 'L2_IMPORT_ERROR_ES'))
            except AttributeError: # If even the dummy structure is not as expected
                pass

            output_json = current_mada_seed_obj.model_dump_json(indent=2)
            print(f"{error_prefix} Critical import failure for lc_python_core. Node cannot operate correctly.")
            return (output_json, current_mada_seed_obj.seed_id, l2_frame_type_str, l2_epistemic_state_str)

        try:
            if not mada_seed_L1_json or mada_seed_L1_json.strip() == "{}":
                print(f"{error_prefix} Empty or default mada_seed_L1_json received.")
                # This shouldn't happen if L1 is working. Create an error MadaSeed.
                current_trace_id = trace_id_L1 if trace_id_L1 != "N/A" else self._generate_error_uid_l2("EMPTY_INPUT")
                current_mada_seed_obj = self._create_error_mada_seed_l2(
                    current_trace_id, "Received empty MadaSeed JSON from L1", L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2
                )
                # Fall through to serialization and return

            if current_mada_seed_obj is None: # If not set by the empty JSON case above
                data_L1 = json.loads(mada_seed_L1_json)
                if PYDANTIC_AVAILABLE_L2: # True if from lc_python_core.mada_seed_types, Pydantic V2 is available
                    current_mada_seed_obj = MadaSeed.model_validate(data_L1)
                    current_trace_id = current_mada_seed_obj.seed_id # Get the actual trace_id
                else:
                    # This case implies mada_seed_types.py set its PYDANTIC_AVAILABLE to False
                    # (meaning Pydantic library itself failed to import there).
                    # The object from L1 would be a dict/dataclass, not matching our Pydantic MadaSeed.
                    # This is a severe issue with the lc_python_core setup.
                    print(f"{error_prefix} lc_python_core.mada_seed_types.PYDANTIC_AVAILABLE is False. Cannot process with Pydantic models.")
                    current_trace_id = data_L1.get("seed_id", current_trace_id)
                    current_mada_seed_obj = self._create_error_mada_seed_l2(
                        current_trace_id, 
                        "Pydantic not available in lc_python_core.mada_seed_types; L1 output may be non-Pydantic.",
                        L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2
                    )
                    # Fall through

        except json.JSONDecodeError as e_deserialize:
            print(f"{error_prefix} Deserializing MadaSeed from L1 failed: {e_deserialize!r}")
            current_trace_id = trace_id_L1 if trace_id_L1 != "N/A" else self._generate_error_uid_l2("DESERIALIZE_FAIL")
            current_mada_seed_obj = self._create_error_mada_seed_l2(
                current_trace_id, f"JSON Deserialization error in L2: {e_deserialize!r}", L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2
            )
        except Exception as e_validate: # Catches Pydantic's ValidationError if model_validate fails
            print(f"{error_prefix} Validating MadaSeed from L1 failed: {e_validate!r}")
            current_trace_id = trace_id_L1 if trace_id_L1 != "N/A" else self._generate_error_uid_l2("VALIDATE_FAIL")
            # Try to get seed_id from the raw JSON if validation fails partway
            try:
                raw_data_L1 = json.loads(mada_seed_L1_json)
                current_trace_id = raw_data_L1.get("seed_id", current_trace_id)
            except:
                pass
            current_mada_seed_obj = self._create_error_mada_seed_l2(
                current_trace_id, f"Pydantic Validation error for L1 MadaSeed in L2: {e_validate!r}", L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2
            )
            
        # Ensure current_mada_seed_obj is an instance of our (potentially dummy) MadaSeed
        if not isinstance(current_mada_seed_obj, MadaSeed):
             # This can happen if PYDANTIC_AVAILABLE_L2 was false and data_L1 was not directly usable
             # by the dummy MadaSeed constructor, or if an error path above failed to set it.
            print(f"{error_prefix} MadaSeed object is not of expected type after L1 processing. Type: {type(current_mada_seed_obj)}")
            current_trace_id = trace_id_L1 if trace_id_L1 != "N/A" else self._generate_error_uid_l2("TYPE_ERROR_POST_L1")
            current_mada_seed_obj = self._create_error_mada_seed_l2(
                current_trace_id, 
                f"MadaSeed object type error after L1 processing: {type(current_mada_seed_obj)}", 
                L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2
            )

        # Call the L2 SOP processing function
        try:
            mada_seed_obj_L2 = frame_click_process(current_mada_seed_obj)
        except Exception as e_sop:
            print(f"{error_prefix} L2 SOP 'frame_click_process' failed: {e_sop!r}")
            # Populate L2 error details into the existing mada_seed_obj_L1 (now current_mada_seed_obj)
            if hasattr(current_mada_seed_obj, 'seed_content'): # Should exist even for dummy
                 l2_error_obj = L2FrameTypeObj( # Use our (potentially dummy) L2FrameTypeObj
                    version="0.1.2", # From schema
                    L2_epistemic_state_of_framing=L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2, # This will use the real Enum if IMPORTS_OK else dummy
                    error_details=f"L2 SOP frame_click_process failed: {e_sop!r}"
                )
                 current_mada_seed_obj.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj = l2_error_obj
            # Also update L2 trace with error
            if hasattr(current_mada_seed_obj, 'trace_metadata'):
                from lc_python_core.mada_seed_types import L2Trace # Assuming IMPORTS_OK for this path
                from datetime import timezone # Ensure timezone is available
                current_mada_seed_obj.trace_metadata.L2_trace = L2Trace(
                    version_L2_trace_schema="0.1.0", 
                    sop_name="lC.SOP.frame_click",
                    completion_timestamp_L2=datetime.now(timezone.utc),
                    epistemic_state_L2=L2EpistemicStateOfFramingEnum.LCL_FAILURE_INTERNAL_L2, # This will use the real Enum if IMPORTS_OK else dummy
                    error_detail=f"L2 SOP frame_click_process failed: {e_sop!r}"
                )
            mada_seed_obj_L2 = current_mada_seed_obj # Return the seed with error info

        # Extract outputs
        final_trace_id = mada_seed_obj_L2.seed_id
        l2_frame_type_str = "N/A"
        l2_epistemic_state_str = "N/A"

        try:
            l2_frame_obj = mada_seed_obj_L2.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj
            if l2_frame_obj: # Check if it's not None
                l2_frame_type_str = str(getattr(l2_frame_obj, 'frame_type_L2', "N/A_FT"))
                l2_epistemic_state_str = str(getattr(l2_frame_obj, 'L2_epistemic_state_of_framing', "N/A_ES"))
        except AttributeError:
            print(f"{error_prefix} Could not extract L2 frame_type or epistemic_state from MadaSeed. Structure might be incorrect.")
            # l2_frame_type_str and l2_epistemic_state_str will remain "N/A" or their last set value

        # Serialize the MadaSeed L2 object back to JSON string
        output_mada_seed_json = "{}"
        try:
            # Check if the object is a Pydantic model and PYDANTIC_AVAILABLE_L2 was true
            is_real_pydantic_model = PYDANTIC_AVAILABLE_L2 and hasattr(mada_seed_obj_L2, 'model_dump_json')
            
            if is_real_pydantic_model:
                output_mada_seed_json = mada_seed_obj_L2.model_dump_json(indent=2, exclude_none=True)
            else: # Fallback for dummy objects or if Pydantic failed within mada_seed_types
                # This uses the custom serializer or __dict__ approach for our simple dummy classes
                def fallback_serializer_l2(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    if hasattr(obj, 'name') and callable(obj.name): # For Enums in dummy objects
                        return obj.name 
                    if hasattr(obj, '__dict__'):
                        return obj.__dict__
                    try:
                        return str(obj) 
                    except:
                        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable in L2 fallback")
                output_mada_seed_json = json.dumps(mada_seed_obj_L2, default=fallback_serializer_l2, indent=2)

        except TypeError as te:
            print(f"{error_prefix} Serializing MadaSeed L2 (TypeError): {te!r}")
            output_mada_seed_json = json.dumps({"error": f"TypeError during MadaSeed L2 serialization: {te!r}", "seed_id": final_trace_id}, indent=2)
        except Exception as e_serialize:
            print(f"{error_prefix} Serializing MadaSeed L2 failed: {e_serialize!r}")
            output_mada_seed_json = json.dumps({"error": f"Failed to serialize MadaSeed L2: {e_serialize!r}", "seed_id": final_trace_id}, indent=2)

        print(f"=== [{self.NODE_NAME}] End of execute(). Trace ID: {final_trace_id} ===")
        return (output_mada_seed_json, final_trace_id, l2_frame_type_str, l2_epistemic_state_str)

    # Helper to create an error MadaSeed object using the node's MadaSeed class (real or dummy)
    def _create_error_mada_seed_l2(self, trace_id: str, error_message: str, l2_state: Any) -> MadaSeed:
        # Uses the MadaSeed class available in the node's scope (could be dummy or real)
        # This is a simplified error seed, focusing on L2.
        # A more robust version would try to use the real Pydantic models if IMPORTS_OK is True.
        
        # Use the L2FrameTypeObj and L2EpistemicStateOfFramingEnum available in this scope
        # (which could be dummies if IMPORTS_OK is False)
        
        # If IMPORTS_OK is False, l2_state might be a string from the dummy enum.
        # If IMPORTS_OK is True, l2_state should be an actual Enum member.
        # The L2FrameTypeObj constructor (real or dummy) should handle this.
        # The dummy L2FrameTypeObj takes a string for L2_epistemic_state_of_framing.
        # The real L2FrameTypeObj (Pydantic) can take an Enum member.
        error_l2_obj = L2FrameTypeObj(
            version="0.1.2", 
            L2_epistemic_state_of_framing=l2_state, # Pass Enum member or string
            error_details=error_message
        )
        
        # Create a basic MadaSeed structure for error reporting
        # This structure needs to be compatible with what frame_click_process expects
        # or how the dummy MadaSeed is defined if imports failed.
        
        if IMPORTS_OK: # Use real Pydantic models if they were imported
            from lc_python_core.mada_seed_types import (
                SeedContent, L1StartleReflexContainer, L2FrameTypeContainer, 
                TraceMetadata, L1Trace, L2Trace, SeedQAQC
            )
            from datetime import timezone # Ensure timezone is available
            # Create a somewhat valid shell for error reporting
            error_seed = MadaSeed(
                version="0.3.0",
                seed_id=trace_id,
                seed_content=SeedContent(
                    raw_signals=[], # Empty for L2 error
                    L1_startle_reflex=L1StartleReflexContainer(
                        L1_startle_context=None, # L1 context might be missing or invalid
                        L2_frame_type=L2FrameTypeContainer(
                            L2_frame_type_obj=error_l2_obj,
                            L3_surface_keymap=None # Placeholder
                        )
                    )
                ),
                trace_metadata=TraceMetadata(
                    trace_id=trace_id,
                    L1_trace=None, # Placeholder
                    L2_trace=L2Trace( # Ensure this is the Pydantic L2Trace model
                        version_Lx_trace_schema="0.1.0", # Correct field name from PlaceholderTraceObj
                        sop_name="lC.SOP.frame_click", # Correctly overridden in L2Trace model
                        completion_timestamp_Lx=datetime.now(timezone.utc), # Correct field name from PlaceholderTraceObj
                        epistemic_state_Lx=l2_state.value if hasattr(l2_state, 'value') else str(l2_state), # Use .value for Enum
                        error_details=error_message # Correct field name from PlaceholderTraceObj
                        # Add any other L2Trace specific fields with defaults if needed.
                        # Based on sop_l2_frame_click.py, other fields like L2_input_class_determined_in_trace etc.
                        # are typically not populated in this minimal error trace, which is acceptable.
                    )
                    # Other traces can be default/None
                ),
                seed_QA_QC=SeedQAQC(), # Default
                seed_completion_timestamp=datetime.now(timezone.utc)
            )
        else: # IMPORTS_OK is False, use the dummy MadaSeed defined in this file
            error_seed = MadaSeed(seed_id=trace_id)
            error_seed.error_details_L2_node = getattr(error_seed, 'error_details_L2_node', '') + f" | L2 Error: {error_message}"
            # Populate the nested dummy structure for L2 error object
            error_seed.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj = error_l2_obj
            # Minimal L2 trace for dummy
            # Cannot import L2Trace here if IMPORTS_OK is false.
            # The dummy MadaSeed has trace_metadata.L2_trace = None initially.
            # We can create a simple object/dict here if needed for the dummy model_dump_json
            dummy_l2_trace_dict = {
                "version_Lx_trace_schema": "0.1.0_dummy", # Consistent field name
                "sop_name": "lC.SOP.frame_click_dummy",
                "completion_timestamp_Lx": datetime.now().isoformat(), # Consistent field name
                "epistemic_state_Lx": str(l2_state.value if hasattr(l2_state, 'value') else l2_state), # Consistent field name
                "error_details": error_message # Consistent field name
            }
            if hasattr(error_seed, 'trace_metadata'):
                 error_seed.trace_metadata.L2_trace = type('DummyL2Trace', (object,), dummy_l2_trace_dict)()


        return error_seed

    def _generate_error_uid_l2(self, hint: str) -> str:
        # Uses the generate_crux_uid available in this scope (could be dummy or real)
        if IMPORTS_OK:
            from lc_python_core.mada_seed_types import generate_crux_uid as real_gen_uid
            return real_gen_uid(f"L2_Node_Error_{hint}")
        else: # Fallback to node's dummy if main one not available
            import uuid
            return f"dummy_uid::L2_Node_Error_{hint}::{uuid.uuid4().hex}"

NODE_CLASS_MAPPINGS = {
    "LcFrameClickNode": LcFrameClickNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LcFrameClickNode": "learnt.cloud L2 FrameClick"
}
