import json
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime # Import datetime directly

# Assuming mada_seed_types.py is in lab.modules.lC.pythonCore
# Adjust path if ComfyUI's custom node loading requires a different relative path.
# For development, ensure lC.pythonCore is in PYTHONPATH or use appropriate relative imports.
try:
    # Attempting a relative import path suitable for ComfyUI custom nodes
    # when this node is in a subfolder of custom_nodes
    from ...lC_pythonCore.mada_seed_types import ( 
        MadaSeed, RawSignalItem, L1StartleContext, SignalComponentMetadataL1, L1Trace,
        SeedContent, TraceMetadata, L1StartleReflexContainer,
        L2FrameTypeContainer, L3SurfaceKeymapContainer, L4AnchorStateContainer,
        L5FieldStateContainer, L6ReflectionPayloadContainer, L7EncodedApplication,
        L2FrameTypeObj, L3SurfaceKeymapObj, L4AnchorStateObj, L5FieldStateObj,
        L6ReflectionPayloadObj, L7EncodedApplication as L7EncodedApplicationObj, # Alias to avoid class name conflict if any
        L2Trace, L3Trace, L4Trace, L5Trace, L6Trace, L7Trace as L7TraceObj, # Alias for trace
        SeedQAQC,
        get_utc_timestamp, generate_crux_uid, PYDANTIC_AVAILABLE
    )
except ImportError as e1:
    print(f"[LcStartleNode] Relative import failed: {e1}. Trying direct import assuming lC_pythonCore is in sys.path.")
    try:
        from lc_python_core.mada_seed_types import ( # Direct import, corrected case
            MadaSeed, RawSignalItem, L1StartleContext, SignalComponentMetadataL1, L1Trace,
            SeedContent, TraceMetadata, L1StartleReflexContainer,
            L2FrameTypeContainer, L3SurfaceKeymapContainer, L4AnchorStateContainer,
            L5FieldStateContainer, L6ReflectionPayloadContainer, L7EncodedApplication,
            L2FrameTypeObj, L3SurfaceKeymapObj, L4AnchorStateObj, L5FieldStateObj,
            L6ReflectionPayloadObj, L7EncodedApplication as L7EncodedApplicationObj,
            L2Trace, L3Trace, L4Trace, L5Trace, L6Trace, L7Trace as L7TraceObj,
            SeedQAQC,
            get_utc_timestamp, generate_crux_uid, PYDANTIC_AVAILABLE
        )
    except ImportError as e2:
        print(f"[LcStartleNode] Direct import failed: {e2}. Providing dummy classes.")
        PYDANTIC_AVAILABLE = False
        # Define dummy classes for the script to be parsable by ComfyUI if imports fail
        class MadaSeed:
            def __init__(self, version=None, seed_id=None, seed_content=None, trace_metadata=None, seed_QA_QC=None, seed_completion_timestamp=None):
                self.version = version
                self.seed_id = seed_id
                self.seed_content = seed_content
                self.trace_metadata = trace_metadata
                self.seed_QA_QC = seed_QA_QC
                self.seed_completion_timestamp = seed_completion_timestamp
        class RawSignalItem:
            def __init__(self, raw_input_id=None, raw_input_signal=None):
                self.raw_input_id = raw_input_id
                self.raw_input_signal = raw_input_signal
        class L1StartleContext:
            def __init__(self, version=None, L1_epistemic_state_of_startle=None, trace_creation_time_L1=None, input_origin_L1=None, signal_components_metadata_L1=None, error_details=None):
                self.version = version
                self.L1_epistemic_state_of_startle = L1_epistemic_state_of_startle
                self.trace_creation_time_L1 = trace_creation_time_L1
                self.input_origin_L1 = input_origin_L1
                self.signal_components_metadata_L1 = signal_components_metadata_L1
                self.error_details = error_details
        class SignalComponentMetadataL1:
            def __init__(self, component_role_L1=None, raw_signal_ref_uid_L1=None, encoding_status_L1=None, byte_size_hint_L1=None, media_type_hint_L1=None, error_details=None):
                self.component_role_L1 = component_role_L1
                self.raw_signal_ref_uid_L1 = raw_signal_ref_uid_L1
                self.encoding_status_L1 = encoding_status_L1
                self.byte_size_hint_L1 = byte_size_hint_L1
                self.media_type_hint_L1 = media_type_hint_L1
                self.error_details = error_details # Adding error_details as it's a common field, though not in the immediate failing call
        class L1Trace:
            def __init__(self, version_L1_trace_schema=None, sop_name=None, completion_timestamp_L1=None, epistemic_state_L1=None, L1_trace_creation_time_from_context=None, L1_input_origin_from_context=None, L1_signal_component_count=None, L1_generated_trace_id=None, L1_generated_raw_signal_ref_uids_summary=None, L1_applied_policy_refs=None, error_details=None):
                self.version_L1_trace_schema = version_L1_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_L1 = completion_timestamp_L1
                self.epistemic_state_L1 = epistemic_state_L1
                self.L1_trace_creation_time_from_context = L1_trace_creation_time_from_context
                self.L1_input_origin_from_context = L1_input_origin_from_context
                self.L1_signal_component_count = L1_signal_component_count
                self.L1_generated_trace_id = L1_generated_trace_id
                self.L1_generated_raw_signal_ref_uids_summary = L1_generated_raw_signal_ref_uids_summary
                self.L1_applied_policy_refs = L1_applied_policy_refs if L1_applied_policy_refs is not None else []
                self.error_details = error_details
        class SeedContent:
            def __init__(self, raw_signals=None, L1_startle_reflex=None):
                self.raw_signals = raw_signals if raw_signals is not None else []
                self.L1_startle_reflex = L1_startle_reflex
        class TraceMetadata:
            def __init__(self, trace_id=None, L1_trace=None, L2_trace=None, L3_trace=None, L4_trace=None, L5_trace=None, L6_trace=None, L7_trace=None):
                self.trace_id = trace_id
                self.L1_trace = L1_trace
                self.L2_trace = L2_trace
                self.L3_trace = L3_trace
                self.L4_trace = L4_trace
                self.L5_trace = L5_trace
                self.L6_trace = L6_trace
                self.L7_trace = L7_trace
        class L1StartleReflexContainer:
            def __init__(self, L1_startle_context=None, L2_frame_type=None):
                self.L1_startle_context = L1_startle_context
                self.L2_frame_type = L2_frame_type
        class L2FrameTypeContainer:
            def __init__(self, L2_frame_type_obj=None, L3_surface_keymap=None):
                self.L2_frame_type_obj = L2_frame_type_obj
                self.L3_surface_keymap = L3_surface_keymap
        class L3SurfaceKeymapContainer:
            def __init__(self, L3_surface_keymap_obj=None, L4_anchor_state=None):
                self.L3_surface_keymap_obj = L3_surface_keymap_obj
                self.L4_anchor_state = L4_anchor_state
        class L4AnchorStateContainer:
            def __init__(self, L4_anchor_state_obj=None, L5_field_state=None):
                self.L4_anchor_state_obj = L4_anchor_state_obj
                self.L5_field_state = L5_field_state
        class L5FieldStateContainer:
            def __init__(self, L5_field_state_obj=None, L6_reflection_payload=None):
                self.L5_field_state_obj = L5_field_state_obj
                self.L6_reflection_payload = L6_reflection_payload
        class L6ReflectionPayloadContainer:
            def __init__(self, L6_reflection_payload_obj=None, L7_encoded_application=None):
                self.L6_reflection_payload_obj = L6_reflection_payload_obj
                self.L7_encoded_application = L7_encoded_application
        class L7EncodedApplication: 
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L7EncodedApplicationObj:
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L2FrameTypeObj:
            def __init__(self, version=None, description=None, error_details=None, input_class_L2=None, frame_type_L2=None, temporal_hint_L2=None, communication_context_L2=None, L2_validation_status_of_frame=None, L2_epistemic_state_of_framing=None):
                self.version = version
                self.description = description
                self.error_details = error_details
                self.input_class_L2 = input_class_L2
                self.frame_type_L2 = frame_type_L2
                self.temporal_hint_L2 = temporal_hint_L2
                self.communication_context_L2 = communication_context_L2
                self.L2_validation_status_of_frame = L2_validation_status_of_frame
                self.L2_epistemic_state_of_framing = L2_epistemic_state_of_framing
        class L3SurfaceKeymapObj:
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L4AnchorStateObj:
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L5FieldStateObj:
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L6ReflectionPayloadObj:
            def __init__(self, version=None, description=None, error_details=None):
                self.version = version
                self.description = description
                self.error_details = error_details
        class L2Trace:
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class L3Trace:
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class L4Trace:
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class L5Trace:
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class L6Trace:
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class L7TraceObj: 
            def __init__(self, version_Lx_trace_schema=None, sop_name=None, completion_timestamp_Lx=None, epistemic_state_Lx=None, error_details=None):
                self.version_Lx_trace_schema = version_Lx_trace_schema
                self.sop_name = sop_name
                self.completion_timestamp_Lx = completion_timestamp_Lx
                self.epistemic_state_Lx = epistemic_state_Lx
                self.error_details = error_details
        class SeedQAQC:
            def __init__(self, version_seed_qa_qc_schema=None, overall_seed_integrity_status=None, qa_qc_assessment_timestamp=None, integrity_findings=None, error_details=None):
                self.version_seed_qa_qc_schema = version_seed_qa_qc_schema
                self.overall_seed_integrity_status = overall_seed_integrity_status
                self.qa_qc_assessment_timestamp = qa_qc_assessment_timestamp
                self.integrity_findings = integrity_findings if integrity_findings is not None else []
                self.error_details = error_details

        def get_utc_timestamp(): import datetime as dt; return dt.datetime.now(dt.timezone.utc) # Fallback
        def generate_crux_uid(hint: str = ""): import uuid; return f"dummy_uid::{hint}::{uuid.uuid4().hex}"


# Helper function to log internal errors (conceptually from SOP)
def _log_internal_error(helper_name: str, context: Dict[str, Any]):
    print(f"[LcStartleNode_INTERNAL_ERROR] in {helper_name}: {context}")

def _log_critical_error(process_name: str, context: Dict[str, Any]):
    print(f"[LcStartleNode_CRITICAL_ERROR] in {process_name}: {context}")

# Python version of _generate_crux_uid from SOP (uses imported version)
def _generate_crux_uid_py(type_hint: str, context_hint: Dict) -> str:
    try:
        return generate_crux_uid(type_hint) 
    except Exception as e:
        _log_internal_error("Helper:_generate_crux_uid_py", {"type": type_hint, "context": context_hint, "error": str(e)})
        raise Exception(f"CRUX UID Generation Failed for {type_hint}")

# Python version of _get_current_timestamp_utc from SOP (uses imported version)
def _get_current_timestamp_utc_py() -> datetime:
    try:
        return get_utc_timestamp()
    except Exception as e:
        _log_internal_error("Helper:_get_current_timestamp_utc_py", {"error": f"Timestamp error: {e}"})
        # Fallback to timezone-aware datetime
        import datetime as dt 
        return dt.datetime.now(dt.timezone.utc)

# Python version of _process_input_components_for_startle from SOP
def _process_input_components_for_startle_py(
    input_data_components: List[Dict[str, Any]], trace_id_for_context: str
) -> Tuple[List[RawSignalItem], List[SignalComponentMetadataL1]]:
    raw_signals_for_madaSeed: List[RawSignalItem] = []
    signal_meta_for_L1_context: List[SignalComponentMetadataL1] = []

    if not input_data_components or len(input_data_components) == 0:
        print("[LcStartleNode_WARNING] Helper:_process_input_components_for_startle_py: No data_components found in input_event.")
        placeholder_comp_uid = _generate_crux_uid_py("raw_signal_placeholder", {"trace_id": trace_id_for_context})
        
        signal_meta_item_args = {
            "component_role_L1": "placeholder_empty_input",
            "raw_signal_ref_uid_L1": placeholder_comp_uid,
            "encoding_status_L1": "Unknown_L1", 
            "byte_size_hint_L1": 0,
            "media_type_hint_L1": None
        }
        raw_signal_item_args = {
            "raw_input_id": placeholder_comp_uid,
            "raw_input_signal": "[[EMPTY_INPUT_EVENT]]"
        }
        signal_meta_for_L1_context.append(SignalComponentMetadataL1(**signal_meta_item_args))
        raw_signals_for_madaSeed.append(RawSignalItem(**raw_signal_item_args))
        return raw_signals_for_madaSeed, signal_meta_for_L1_context

    for component_event_data in input_data_components:
        raw_signal_ref_uid = _generate_crux_uid_py(
            "raw_signal_content", {"trace_id": trace_id_for_context, "role": component_event_data.get('role_hint')}
        )
        
        raw_signal_item_args = {
            "raw_input_id": raw_signal_ref_uid,
            "raw_input_signal": str(component_event_data.get('content_handle_placeholder', '[[CONTENT_REF_OMITTED]]'))
        }

        encoding_status = "Unknown_L1"
        type_hint = component_event_data.get('type_hint')
        if type_hint:
            if type_hint.lower().startswith("text/"): encoding_status = "AssumedUTF8_TextHint"
            elif type_hint.lower() in ["application/octet-stream", "image/jpeg", "application/pdf", "text/uri-list"]: encoding_status = "DetectedBinary"
            else: encoding_status = "PossibleEncodingIssue_L1"
        
        signal_meta_item_args = {
            "component_role_L1": component_event_data.get('role_hint', 'primary_content'),
            "raw_signal_ref_uid_L1": raw_signal_ref_uid,
            "encoding_status_L1": encoding_status, 
            "byte_size_hint_L1": component_event_data.get('size_hint'),
            "media_type_hint_L1": type_hint
        }
        raw_signals_for_madaSeed.append(RawSignalItem(**raw_signal_item_args))
        signal_meta_for_L1_context.append(SignalComponentMetadataL1(**signal_meta_item_args))
            
    return raw_signals_for_madaSeed, signal_meta_for_L1_context

# Python version of _create_initial_madaSeed_shell from SOP
def _create_initial_madaSeed_shell_py(seed_uid: str, trace_id_val: str, raw_signals_list: List[RawSignalItem]) -> MadaSeed:
    current_time_placeholder = _get_current_timestamp_utc_py()

    l2_frame_obj = L2FrameTypeObj(version="0.1.2", description="L2 Frame Placeholder")
    l3_keymap_obj = L3SurfaceKeymapObj(version="0.1.1", description="L3 Keymap Placeholder")
    l4_anchor_obj = L4AnchorStateObj(version="0.2.17", description="L4 Anchor Placeholder")
    l5_field_obj = L5FieldStateObj(version="0.2.0", description="L5 Field Placeholder")
    l6_reflect_obj = L6ReflectionPayloadObj(version="0.1.6", description="L6 Reflection Placeholder")
    l7_app_obj = L7EncodedApplicationObj(version="0.1.1", description="L7 Application Placeholder")

    dummy_l1_context = L1StartleContext(
        version="0.1.1",
        L1_epistemic_state_of_startle="Startle_Complete_SignalRefs_Generated",
        trace_creation_time_L1=current_time_placeholder,
        signal_components_metadata_L1=[SignalComponentMetadataL1(
            component_role_L1="placeholder", raw_signal_ref_uid_L1="placeholder_uid", encoding_status_L1="Unknown_L1"
        )]
    )
    dummy_l1_trace = L1Trace(
        version_L1_trace_schema="0.1.0", sop_name="lC.SOP.startle",
        completion_timestamp_L1=current_time_placeholder,
        epistemic_state_L1="Startle_Complete_SignalRefs_Generated",
        L1_trace_creation_time_from_context=current_time_placeholder,
        L1_signal_component_count=1
    )

    trace_meta_args = {"trace_id": trace_id_val, "L1_trace": dummy_l1_trace}
    if PYDANTIC_AVAILABLE: 
        trace_meta = TraceMetadata(**trace_meta_args) # Pydantic uses default_factory for L2-L7
    else: 
        trace_meta = TraceMetadata(
            **trace_meta_args, L2_trace=L2Trace(), L3_trace=L3Trace(), L4_trace=L4Trace(),
            L5_trace=L5Trace(), L6_trace=L6Trace(), L7_trace=L7TraceObj()
        )

    seed_content_args = {
        "raw_signals": raw_signals_list,
        "L1_startle_reflex": L1StartleReflexContainer(
            L1_startle_context=dummy_l1_context, 
            L2_frame_type=L2FrameTypeContainer( L2_frame_type_obj=l2_frame_obj,
                L3_surface_keymap=L3SurfaceKeymapContainer( L3_surface_keymap_obj=l3_keymap_obj,
                    L4_anchor_state=L4AnchorStateContainer( L4_anchor_state_obj=l4_anchor_obj,
                        L5_field_state=L5FieldStateContainer( L5_field_state_obj=l5_field_obj,
                            L6_reflection_payload=L6ReflectionPayloadContainer(
                                L6_reflection_payload_obj=l6_reflect_obj, L7_encoded_application=l7_app_obj
    ))))))}
    
    mada_seed_args = {
        "version": "0.3.0", "seed_id": seed_uid,
        "seed_content": SeedContent(**seed_content_args),
        "trace_metadata": trace_meta,
        "seed_QA_QC": SeedQAQC(), 
        "seed_completion_timestamp": None
    }
    return MadaSeed(**mada_seed_args)

# Python version of startle_process from SOP
def startle_process_py(input_event: Dict[str, Any]) -> MadaSeed:
    generated_trace_id = "ERROR_TRACE_ID_AT_STARTLE_INIT" 
    error_details_for_obj: Optional[str] = None
    error_details_for_trace: Optional[str] = None
    
    try:
        if not input_event or input_event.get('reception_timestamp_utc_iso') is None:
            raise ValueError("Invalid Input: Missing reception_timestamp_utc_iso.")
        
        l1_trace_creation_time_str = input_event.get('reception_timestamp_utc_iso')
        if l1_trace_creation_time_str.endswith("Z"):
            l1_trace_creation_time_dt = datetime.fromisoformat(l1_trace_creation_time_str[:-1] + "+00:00")
        else:
            l1_trace_creation_time_dt = datetime.fromisoformat(l1_trace_creation_time_str)
        
        l1_input_origin = input_event.get('origin_hint')
        input_components_data = input_event.get('data_components', [])

        generated_trace_id = _generate_crux_uid_py("trace_event_L1", {"origin": l1_input_origin, "time": l1_trace_creation_time_str})
        
        raw_signals_for_seed, signal_components_meta_for_l1_payload = \
            _process_input_components_for_startle_py(input_components_data, generated_trace_id)
        
        working_mada_seed = _create_initial_madaSeed_shell_py(generated_trace_id, generated_trace_id, raw_signals_for_seed)
        
        l1_final_epistemic_state = "Startle_Complete_SignalRefs_Generated"
        
        l1_startle_context_args = {
            "version": "0.1.1",
            "L1_epistemic_state_of_startle": l1_final_epistemic_state,
            "trace_creation_time_L1": l1_trace_creation_time_dt,
            "input_origin_L1": l1_input_origin,
            "signal_components_metadata_L1": signal_components_meta_for_l1_payload,
            "error_details": None 
        }
        working_mada_seed.seed_content.L1_startle_reflex.L1_startle_context = L1StartleContext(**l1_startle_context_args)

        l1_completion_time_dt = _get_current_timestamp_utc_py()
        l1_trace_obj_args = {
            "version_L1_trace_schema": "0.1.0", "sop_name": "lC.SOP.startle",
            "completion_timestamp_L1": l1_completion_time_dt,
            "epistemic_state_L1": l1_final_epistemic_state,
            "L1_trace_creation_time_from_context": l1_trace_creation_time_dt,
            "L1_input_origin_from_context": l1_input_origin,
            "L1_signal_component_count": len(signal_components_meta_for_l1_payload),
            "L1_generated_trace_id": generated_trace_id,
            "L1_generated_raw_signal_ref_uids_summary": {
                "count": len(raw_signals_for_seed),
                "first_ref_uid_sample": raw_signals_for_seed[0].raw_input_id if raw_signals_for_seed else None
            },
            "L1_applied_policy_refs": [], "error_details": None
        }
        working_mada_seed.trace_metadata.L1_trace = L1Trace(**l1_trace_obj_args)
        return working_mada_seed

    except Exception as critical_process_error:
        _log_critical_error("Startle Process Failed Critically", {"input_origin": input_event.get('origin_hint'), "error": str(critical_process_error)})
        error_details_for_obj = str(critical_process_error)
        error_details_for_trace = str(critical_process_error)
        
        current_time_init_fail = _get_current_timestamp_utc_py()
        reception_ts_str_on_error = input_event.get('reception_timestamp_utc_iso', current_time_init_fail.isoformat())
        if reception_ts_str_on_error.endswith("Z"):
            trace_creation_on_error_dt = datetime.fromisoformat(reception_ts_str_on_error[:-1] + "+00:00")
        else:
            trace_creation_on_error_dt = datetime.fromisoformat(reception_ts_str_on_error)

        raw_signals_on_error = [RawSignalItem(raw_input_id="ERROR_RAW_ID", raw_input_signal="ERROR_RAW_SIGNAL")]
        error_seed_shell = _create_initial_madaSeed_shell_py(generated_trace_id, generated_trace_id, raw_signals_on_error)
        
        error_l1_context_args = {
            "version": "0.1.1", "L1_epistemic_state_of_startle": "LCL-Failure-Internal_L1",
            "trace_creation_time_L1": trace_creation_on_error_dt,
            "input_origin_L1": input_event.get('origin_hint'),
            "signal_components_metadata_L1": [SignalComponentMetadataL1(
                 component_role_L1="error_placeholder", raw_signal_ref_uid_L1="error_uid", encoding_status_L1="Unknown_L1")],
            "error_details": error_details_for_obj
        }
        error_l1_trace_args = {
            "version_L1_trace_schema": "0.1.0", "sop_name": "lC.SOP.startle", 
            "completion_timestamp_L1": current_time_init_fail,
            "epistemic_state_L1": "LCL-Failure-Internal_L1",
            "L1_trace_creation_time_from_context": trace_creation_on_error_dt,
            "L1_input_origin_from_context": input_event.get('origin_hint'),
            "L1_signal_component_count": 0, "L1_generated_trace_id": generated_trace_id,
            "error_details": error_details_for_trace
        }
        error_seed_shell.seed_content.L1_startle_reflex.L1_startle_context = L1StartleContext(**error_l1_context_args)
        error_seed_shell.trace_metadata.L1_trace = L1Trace(**error_l1_trace_args)
        return error_seed_shell

class LcStartleNode:
    RETURN_TYPES = ("STRING", "STRING",) 
    RETURN_NAMES = ("mada_seed_L1", "trace_id",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        # print("[LcStartleNode] INPUT_TYPES() called") # Less verbose
        return {
            "required": {
                "input_text": ("STRING", {"default": "startle reflex"}),
                "origin_hint": ("STRING", {"default": "ComfyUI_LcStartleNode_Py"}),
                "optional_attachments_ref": ("STRING", {"default": "", "multiline": True}),
                "user_id": ("STRING", {"default": "ComfyUI_User"}),
            }
        }

    def execute(self, input_text: str, origin_hint: str, optional_attachments_ref: str, user_id: str):
        print("=== [LcStartleNode] execute() PYTHON LOGIC ===")
        try:
            reception_time_iso = get_utc_timestamp().isoformat()
            # The get_utc_timestamp() from mada_seed_types returns a timezone-aware datetime object.
            # .isoformat() on a timezone-aware object correctly includes timezone information (e.g., +00:00 or Z).
            
            data_components = [{
                "role_hint": "primary_text_content",
                "content_handle_placeholder": input_text,
                "size_hint": len(input_text.encode("utf-8")) if input_text else 0,
                "type_hint": "text/plain"
            }]

            if optional_attachments_ref and optional_attachments_ref.strip():
                data_components.append({
                    "role_hint": "attachment_reference",
                    "content_handle_placeholder": optional_attachments_ref,
                    "size_hint": None, "type_hint": "text/uri-list" 
                })

            input_event_dict = {
                "reception_timestamp_utc_iso": reception_time_iso,
                "origin_hint": origin_hint,
                "data_components": data_components
            }
            mada_seed_obj = startle_process_py(input_event_dict)
            
            mada_seed_json_str = ""
            final_trace_id = "ERROR_NO_SEED_ID_FALLBACK"

            if mada_seed_obj:
                final_trace_id = mada_seed_obj.seed_id
                if PYDANTIC_AVAILABLE and hasattr(mada_seed_obj, 'model_dump_json'):
                    mada_seed_json_str = mada_seed_obj.model_dump_json(indent=2)
                else: 
                    def dt_handler(o):
                        if isinstance(o, datetime): return o.isoformat()
                        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
                    try:
                        import dataclasses
                        if dataclasses.is_dataclass(mada_seed_obj):
                           dict_obj = dataclasses.asdict(mada_seed_obj)
                           mada_seed_json_str = json.dumps(dict_obj, default=dt_handler, indent=2)
                        else: 
                           mada_seed_json_str = json.dumps({"error": "Object is not a Pydantic model or dataclass"}, indent=2)
                    except Exception as json_e:
                        print(f"[LcStartleNode] JSON serialization error: {json_e}")
                        mada_seed_json_str = f'{{"error": "Failed to serialize MadaSeed: {json_e}", "seed_id": "{final_trace_id}"}}'
            
            print(f"[LcStartleNode] Python logic trace_id: {final_trace_id}")
            return (mada_seed_json_str, final_trace_id)

        except Exception as e:
            print(f"[LcStartleNode] ERROR in Python logic execute(): {type(e).__name__}: {e}")
            _log_critical_error("LcStartleNode.execute", {"error": str(e)})
            # Ensure generate_crux_uid is available for error trace_id
            try: error_trace_id_gen = generate_crux_uid("error_execute")
            except: error_trace_id_gen = "ERROR_UID_GEN_FAILED"
            
            error_json = json.dumps({
                "seed_id": error_trace_id_gen,
                "error_message": "LcStartleNode execution failed", 
                "error_details_execute": str(e),
                "trace_metadata": { "trace_id": error_trace_id_gen, "L1_trace": { "error_details": str(e) } }
            }, indent=2)
            return (error_json, error_trace_id_gen)

# Standard ComfyUI registration (if file is directly used as a custom node)
# NODE_CLASS_MAPPINGS = { "LcStartleNode": LcStartleNode }
# NODE_DISPLAY_NAME_MAPPINGS = { "LcStartleNode": "learnt.cloud L1 Startle Node (Python)" }
