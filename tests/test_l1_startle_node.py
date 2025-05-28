import unittest
import json
from datetime import datetime, timezone

# Assuming the test file is run from a context where this import path works.
# This might need adjustment based on the actual test execution environment (e.g., using sys.path.append).
try:
    from ...lC_pythonCore.mada_seed_types import (
        MadaSeed, PYDANTIC_AVAILABLE, L1StartleContext, L1Trace, RawSignalItem, SignalComponentMetadataL1,
        L2FrameTypeObj, L3SurfaceKeymapObj, L4AnchorStateObj, L5FieldStateObj, L6ReflectionPayloadObj, L7EncodedApplicationObj,
        L2Trace, L3Trace, L4Trace, L5Trace, L6Trace, L7TraceObj
    )
    # If Pydantic is available, we can use its parsing capabilities
    if PYDANTIC_AVAILABLE:
        from pydantic import ValidationError
except ImportError as e:
    print(f"Test Setup Error: Could not import MadaSeed types for testing: {e}")
    # Define dummy classes if import fails, so the test file can at least be parsed
    PYDANTIC_AVAILABLE = False
    class MadaSeed: pass
    class L1StartleContext: pass
    class L1Trace: pass
    class RawSignalItem: pass
    class SignalComponentMetadataL1: pass
    class L2FrameTypeObj: pass
    class L3SurfaceKeymapObj: pass
    class L4AnchorStateObj: pass
    class L5FieldStateObj: pass
    class L6ReflectionPayloadObj: pass
    class L7EncodedApplicationObj: pass
    class L2Trace: pass
    class L3Trace: pass
    class L4Trace: pass
    class L5Trace: pass
    class L6Trace: pass
    class L7TraceObj: pass
    class ValidationError(Exception): pass


from ..l1_startle_node import LcStartleNode # Import the node to be tested

class TestLcStartleNode(unittest.TestCase):

    def setUp(self):
        self.node = LcStartleNode()

    def _parse_mada_seed(self, json_string: str) -> MadaSeed:
        data = json.loads(json_string)
        if PYDANTIC_AVAILABLE:
            try:
                return MadaSeed(**data)
            except ValidationError as e:
                self.fail(f"Pydantic validation error during MadaSeed parsing: {e}\nJSON Data: {json_string}")
        else:
            # Manual dataclass hydration (simplified, assumes direct field mapping)
            # This would need to be more robust for a real dataclass scenario
            # For testing, focusing on Pydantic path first.
            # If Pydantic is not available, these tests will largely pass through if dummy classes are used.
            print("Warning: Pydantic not available, using basic dict for MadaSeed in tests.")
            return data # Return as dict if no Pydantic, assertions will be on dict keys/values

    def test_basic_successful_execution(self):
        mada_seed_json, trace_id = self.node.execute(
            input_text="Test Startle",
            origin_hint="TestOrigin",
            optional_attachments_ref="",
            user_id="TestUser"
        )
        self.assertIsInstance(mada_seed_json, str)
        self.assertIsInstance(trace_id, str)
        
        try:
            data = json.loads(mada_seed_json)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON.")

        self.assertIn("seed_id", data)
        self.assertEqual(data["seed_id"], trace_id)
        self.assertTrue(trace_id.startswith("urn:crux:uid::trace_event_L1::"))

    def test_top_level_mada_seed_fields(self):
        mada_seed_json, trace_id = self.node.execute("Test", "TestOrigin", "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            self.assertEqual(mada_seed.version, "0.3.0")
            self.assertEqual(mada_seed.seed_id, trace_id)
            self.assertIsNotNone(mada_seed.seed_content)
            self.assertIsNotNone(mada_seed.trace_metadata)
            self.assertIsNotNone(mada_seed.seed_QA_QC)
            self.assertIsNone(mada_seed.seed_completion_timestamp)
        else: # Basic dict checks
            self.assertEqual(mada_seed.get("version"), "0.3.0")
            self.assertEqual(mada_seed.get("seed_id"), trace_id)
            self.assertIn("seed_content", mada_seed)
            self.assertIn("trace_metadata", mada_seed)
            self.assertIn("seed_QA_QC", mada_seed)
            self.assertIsNone(mada_seed.get("seed_completion_timestamp"), "seed_completion_timestamp should be None at L1")


    def test_raw_signals_single_input(self):
        input_text = "Hello Startle"
        mada_seed_json, _ = self.node.execute(input_text, "TestOrigin", "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)
        
        if PYDANTIC_AVAILABLE:
            sc = mada_seed.seed_content
            self.assertEqual(len(sc.raw_signals), 1)
            raw_signal_item = sc.raw_signals[0]
            self.assertIsInstance(raw_signal_item, RawSignalItem)
            self.assertTrue(raw_signal_item.raw_input_id.startswith("urn:crux:uid::raw_signal_content::"))
            self.assertEqual(raw_signal_item.raw_input_signal, input_text)
        else:
            sc = mada_seed.get("seed_content", {})
            self.assertEqual(len(sc.get("raw_signals", [])), 1)
            # Further dict checks if needed

    def test_l1_startle_context_fields(self):
        origin = "TestOriginL1Context"
        mada_seed_json, _ = self.node.execute("Test", origin, "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context
            self.assertIsInstance(l1_context, L1StartleContext)
            self.assertEqual(l1_context.version, "0.1.1")
            self.assertEqual(l1_context.L1_epistemic_state_of_startle, "Startle_Complete_SignalRefs_Generated")
            
            # Timestamp validation for trace_creation_time_L1
            self.assertIsInstance(l1_context.trace_creation_time_L1, datetime)
            self.assertIsNotNone(l1_context.trace_creation_time_L1.tzinfo, "trace_creation_time_L1 should be timezone-aware")
            self.assertEqual(l1_context.trace_creation_time_L1.tzinfo, timezone.utc, "trace_creation_time_L1 should be UTC")

            self.assertEqual(l1_context.input_origin_L1, origin)
            self.assertIsNone(l1_context.error_details)

            self.assertEqual(len(l1_context.signal_components_metadata_L1), 1)
            signal_meta = l1_context.signal_components_metadata_L1[0]
            self.assertIsInstance(signal_meta, SignalComponentMetadataL1)
            self.assertEqual(signal_meta.component_role_L1, "primary_text_content")
            self.assertTrue(signal_meta.raw_signal_ref_uid_L1.startswith("urn:crux:uid::raw_signal_content::"))
            self.assertEqual(signal_meta.encoding_status_L1, "AssumedUTF8_TextHint")
            self.assertEqual(signal_meta.media_type_hint_L1, "text/plain")
        else: # Basic dict checks
            l1_context = mada_seed.get("seed_content", {}).get("L1_startle_reflex", {}).get("L1_startle_context", {})
            self.assertEqual(l1_context.get("version"), "0.1.1")
            # ... other dict checks
            # Manual string parsing for non-Pydantic path
            l1_context_dict = mada_seed.get("seed_content", {}).get("L1_startle_reflex", {}).get("L1_startle_context", {})
            ts_string = l1_context_dict.get("trace_creation_time_L1")
            self.assertIsInstance(ts_string, str)
            try:
                parsed_dt = datetime.fromisoformat(ts_string.replace('Z', '+00:00'))
                self.assertIsNotNone(parsed_dt.tzinfo, "Parsed trace_creation_time_L1 string should be timezone-aware")
            except ValueError:
                self.fail(f"Could not parse trace_creation_time_L1 string: {ts_string}")

    def test_l1_trace_fields(self):
        origin = "TestOriginL1Trace"
        mada_seed_json, trace_id = self.node.execute("Test L1 Trace", origin, "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            l1_trace = mada_seed.trace_metadata.L1_trace
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context

            l1_trace = mada_seed.trace_metadata.L1_trace
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context

            self.assertIsInstance(l1_trace, L1Trace)
            self.assertEqual(l1_trace.version_L1_trace_schema, "0.1.0")
            self.assertEqual(l1_trace.sop_name, "lC.SOP.startle")

            # Timestamp validation for completion_timestamp_L1
            self.assertIsInstance(l1_trace.completion_timestamp_L1, datetime)
            self.assertIsNotNone(l1_trace.completion_timestamp_L1.tzinfo, "completion_timestamp_L1 should be timezone-aware")
            self.assertEqual(l1_trace.completion_timestamp_L1.tzinfo, timezone.utc, "completion_timestamp_L1 should be UTC")
            
            self.assertTrue(l1_trace.completion_timestamp_L1 >= l1_context.trace_creation_time_L1) 

            self.assertEqual(l1_trace.epistemic_state_L1, "Startle_Complete_SignalRefs_Generated")
            
            # Timestamp validation for L1_trace_creation_time_from_context
            self.assertIsInstance(l1_trace.L1_trace_creation_time_from_context, datetime)
            self.assertIsNotNone(l1_trace.L1_trace_creation_time_from_context.tzinfo, "L1_trace_creation_time_from_context should be timezone-aware")
            self.assertEqual(l1_trace.L1_trace_creation_time_from_context.tzinfo, timezone.utc, "L1_trace_creation_time_from_context should be UTC")
            self.assertEqual(l1_trace.L1_trace_creation_time_from_context, l1_context.trace_creation_time_L1)
            
            self.assertEqual(l1_trace.L1_input_origin_from_context, origin)
            self.assertEqual(l1_trace.L1_signal_component_count, 1)
            self.assertEqual(l1_trace.L1_generated_trace_id, trace_id)
            self.assertIsNone(l1_trace.error_details)
            self.assertIsNotNone(l1_trace.L1_generated_raw_signal_ref_uids_summary)
            self.assertEqual(l1_trace.L1_generated_raw_signal_ref_uids_summary.get("count"), 1)
        else: # Basic dict checks
            l1_trace = mada_seed.get("trace_metadata", {}).get("L1_trace", {})
            self.assertEqual(l1_trace.get("sop_name"), "lC.SOP.startle")
            # ... other dict checks
            # Manual string parsing for non-Pydantic path
            l1_trace_dict = mada_seed.get("trace_metadata", {}).get("L1_trace", {})
            
            ts_completion_str = l1_trace_dict.get("completion_timestamp_L1")
            self.assertIsInstance(ts_completion_str, str)
            try:
                parsed_dt_completion = datetime.fromisoformat(ts_completion_str.replace('Z', '+00:00'))
                self.assertIsNotNone(parsed_dt_completion.tzinfo, "Parsed completion_timestamp_L1 string should be timezone-aware")
            except ValueError:
                self.fail(f"Could not parse completion_timestamp_L1 string: {ts_completion_str}")

            ts_creation_context_str = l1_trace_dict.get("L1_trace_creation_time_from_context")
            self.assertIsInstance(ts_creation_context_str, str)
            try:
                parsed_dt_creation_context = datetime.fromisoformat(ts_creation_context_str.replace('Z', '+00:00'))
                self.assertIsNotNone(parsed_dt_creation_context.tzinfo, "Parsed L1_trace_creation_time_from_context string should be timezone-aware")
            except ValueError:
                self.fail(f"Could not parse L1_trace_creation_time_from_context string: {ts_creation_context_str}")

    def test_l2_l7_placeholders(self):
        mada_seed_json, _ = self.node.execute("Test Placeholders", "TestOrigin", "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            # Content Objects (L2-L7)
            l2_obj = mada_seed.seed_content.L1_startle_reflex.L2_frame_type.L2_frame_type_obj
            self.assertIsInstance(l2_obj, L2FrameTypeObj)
            self.assertEqual(l2_obj.version, "0.1.2") # As per shell creation
            self.assertEqual(l2_obj.description, "L2 Frame Placeholder")

            l7_obj = mada_seed.seed_content.L1_startle_reflex.L2_frame_type.L3_surface_keymap.L4_anchor_state.L5_field_state.L6_reflection_payload.L7_encoded_application
            self.assertIsInstance(l7_obj, L7EncodedApplicationObj) # Using alias from import
            self.assertEqual(l7_obj.version, "0.1.1")

            # Trace Objects (L2-L7) - Check completion timestamps are None
            trace_metadata = mada_seed.trace_metadata
            self.assertIsNone(trace_metadata.L2_trace.completion_timestamp_Lx, "L2 completion_timestamp should be None")
            self.assertIsNone(trace_metadata.L3_trace.completion_timestamp_Lx, "L3 completion_timestamp should be None")
            self.assertIsNone(trace_metadata.L4_trace.completion_timestamp_Lx, "L4 completion_timestamp should be None")
            self.assertIsNone(trace_metadata.L5_trace.completion_timestamp_Lx, "L5 completion_timestamp should be None")
            self.assertIsNone(trace_metadata.L6_trace.completion_timestamp_Lx, "L6 completion_timestamp should be None")
            self.assertIsNone(trace_metadata.L7_trace.completion_timestamp_Lx, "L7 completion_timestamp should be None")
            
            # Also check specific fields if they exist in schema and are not part of PlaceholderTraceObj
            # Example for L2Trace if it had 'completion_timestamp_L2' explicitly
            if hasattr(trace_metadata.L2_trace, 'completion_timestamp_L2'):
                 self.assertIsNone(trace_metadata.L2_trace.completion_timestamp_L2, "L2_trace.completion_timestamp_L2 should be None")
            # Repeat for L3-L7 if their specific trace models have explicit Lx timestamp fields

        else: # Basic dict checks
            l2_obj = mada_seed.get("seed_content",{}).get("L1_startle_reflex",{}).get("L2_frame_type",{}).get("L2_frame_type_obj",{})
            self.assertEqual(l2_obj.get("version"), "0.1.2")
            
            trace_meta_dict = mada_seed.get("trace_metadata", {})
            for i in range(2, 8):
                lx_trace = trace_meta_dict.get(f"L{i}_trace", {})
                # PlaceholderTraceObj in mada_seed_types sets completion_timestamp_Lx to None by default
                self.assertIsNone(lx_trace.get("completion_timestamp_Lx"), f"L{i} completion_timestamp_Lx should be None")
                # Check specific field name if different from placeholder if necessary
                self.assertIsNone(lx_trace.get(f"completion_timestamp_L{i}"), f"L{i} completion_timestamp_L{i} should be None")


    def test_empty_input_text(self):
        mada_seed_json, _ = self.node.execute(input_text="", origin_hint="EmptyInputTest", optional_attachments_ref="", user_id="TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context
            self.assertEqual(len(l1_context.signal_components_metadata_L1), 1)
            signal_meta = l1_context.signal_components_metadata_L1[0]
            self.assertEqual(signal_meta.component_role_L1, "placeholder_empty_input")
            self.assertEqual(signal_meta.byte_size_hint_L1, 0)
            self.assertTrue(signal_meta.raw_signal_ref_uid_L1.startswith("urn:crux:uid::raw_signal_placeholder::"))

            raw_signals = mada_seed.seed_content.raw_signals
            self.assertEqual(len(raw_signals), 1)
            self.assertEqual(raw_signals[0].raw_input_signal, "[[EMPTY_INPUT_EVENT]]")
            self.assertEqual(raw_signals[0].raw_input_id, signal_meta.raw_signal_ref_uid_L1)
        else: # Basic dict checks
            l1_context = mada_seed.get("seed_content", {}).get("L1_startle_reflex", {}).get("L1_startle_context", {})
            signal_meta_list = l1_context.get("signal_components_metadata_L1", [])
            self.assertEqual(len(signal_meta_list), 1)
            # ... other dict checks

    def test_crux_uid_format(self):
        mada_seed_json, trace_id = self.node.execute("UID Test", "TestOrigin", "", "TestUser")
        mada_seed = self._parse_mada_seed(mada_seed_json)
        
        self.assertTrue(trace_id.startswith("urn:crux:uid::"))
        if PYDANTIC_AVAILABLE:
            self.assertTrue(mada_seed.seed_id.startswith("urn:crux:uid::"))
            self.assertTrue(mada_seed.trace_metadata.trace_id.startswith("urn:crux:uid::"))
            self.assertTrue(mada_seed.trace_metadata.L1_trace.L1_generated_trace_id.startswith("urn:crux:uid::"))
            
            raw_signal_uid = mada_seed.seed_content.raw_signals[0].raw_input_id
            self.assertTrue(raw_signal_uid.startswith("urn:crux:uid::"))
            
            signal_meta_uid = mada_seed.seed_content.L1_startle_reflex.L1_startle_context.signal_components_metadata_L1[0].raw_signal_ref_uid_L1
            self.assertTrue(signal_meta_uid.startswith("urn:crux:uid::"))
        # Else: dict checks would be similar with .get()

    def test_attachment_handling(self):
        attachment_ref = "urn:crux:uid::some_attachment_reference"
        mada_seed_json, _ = self.node.execute(
            input_text="Text with attachment",
            origin_hint="AttachmentTest",
            optional_attachments_ref=attachment_ref,
            user_id="TestUser"
        )
        mada_seed = self._parse_mada_seed(mada_seed_json)

        if PYDANTIC_AVAILABLE:
            l1_context = mada_seed.seed_content.L1_startle_reflex.L1_startle_context
            self.assertEqual(len(l1_context.signal_components_metadata_L1), 2)
            
            primary_found = False
            attachment_found = False
            for comp_meta in l1_context.signal_components_metadata_L1:
                if comp_meta.component_role_L1 == "primary_text_content":
                    primary_found = True
                elif comp_meta.component_role_L1 == "attachment_reference":
                    attachment_found = True
                    self.assertEqual(comp_meta.media_type_hint_L1, "text/uri-list") # As per current node logic
                    # Find corresponding raw_signal
                    raw_signal_entry = next((rs for rs in mada_seed.seed_content.raw_signals if rs.raw_input_id == comp_meta.raw_signal_ref_uid_L1), None)
                    self.assertIsNotNone(raw_signal_entry)
                    self.assertEqual(raw_signal_entry.raw_input_signal, attachment_ref)

            self.assertTrue(primary_found)
            self.assertTrue(attachment_found)
            
            self.assertEqual(len(mada_seed.seed_content.raw_signals), 2)


if __name__ == '__main__':
    unittest.main()
