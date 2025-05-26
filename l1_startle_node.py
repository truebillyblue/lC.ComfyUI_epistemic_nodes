from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import uuid
import asyncio

# ADK Imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event
from google.genai.types import Content, Part

# Startle agent and MadaSeed model
from lc_python_core.adk_agents import StartleAgent
from lc_python_core.schemas.mada_schema import MadaSeed

class LcStartleNode:
    CATEGORY = "LearntCloud/EpistemicOSI_ADK"
    RETURN_TYPES = ("MADA_SEED", "STRING",)
    RETURN_NAMES = ("mada_seed_L1", "trace_id",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "origin_hint": ("STRING", {"multiline": False, "default": "ComfyUI_LcStartleNode_ADK"}),
                "optional_attachments_ref": ("STRING", {"multiline": False, "default": ""}),
                "user_id": ("STRING", {"multiline": False, "default": "ComfyUI_User"}),
            }
        }

    def execute(self, input_text: str, origin_hint: Optional[str] = None,
                optional_attachments_ref: Optional[str] = None, user_id: Optional[str] = "ComfyUI_User"):
        return asyncio.run(self._run_async(input_text, origin_hint, optional_attachments_ref, user_id))

    async def _run_async(self, input_text: str, origin_hint: Optional[str], 
                         optional_attachments_ref: Optional[str], user_id: str):

        input_event_dict = {
            "reception_timestamp_utc_iso": datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'),
            "origin_hint": origin_hint,
            "data_components": [
                {
                    "role_hint": "primary_text_content", 
                    "content_handle_placeholder": input_text,
                    "size_hint": len(input_text.encode('utf-8')), 
                    "type_hint": "text/plain"
                }
            ]
        }
        if optional_attachments_ref:
            input_event_dict["data_components"].append({
                "role_hint": "attachment_reference",
                "content_handle_placeholder": optional_attachments_ref,
                "size_hint": len(optional_attachments_ref.encode('utf-8')),
                "type_hint": "text/uri-reference"
            })

        print(f"LcStartleNode (ADK): Preparing to run StartleAgent with input_event: {input_event_dict}")

        startle_agent_instance = StartleAgent()
        session_service = InMemorySessionService()
        runner = Runner(agent=startle_agent_instance, app_name="ComfyUI_ADK_Runner", session_service=session_service)
        session_id = str(uuid.uuid4())
        initial_state_dict = {"input_event": input_event_dict}

        try:
            session = await session_service.create_session(
                app_name=runner.app_name, user_id=user_id, session_id=session_id, state=initial_state_dict
            )
            print(f"LcStartleNode (ADK): Created session {session_id} with initial state.")

            placeholder_message = Content(role="user", parts=[Part(text="Run StartleAgent")])
            events: List[Event] = []
            async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=placeholder_message):
                events.append(event)

            print(f"LcStartleNode (ADK): StartleAgent execution completed. Events count: {len(events)}")

            updated_session = await session_service.get_session(
                app_name=runner.app_name, user_id=user_id, session_id=session_id
            )

            mada_seed_output: Optional[MadaSeed] = None
            trace_id_output: str = "ERROR_TRACE_ID_NOT_RETRIEVED"

            if updated_session and updated_session.state:
                mada_seed_output = updated_session.state.get("mada_seed_output")
                trace_id_output = updated_session.state.get("trace_id", "ERROR_TRACE_ID_MISSING_IN_STATE")
                print(f"LcStartleNode (ADK): Retrieved from updated session state. Trace ID: {trace_id_output}")
            else:
                print("LcStartleNode (ADK): Failed to retrieve updated session or state from session service.")

        except Exception as e:
            print(f"LcStartleNode (ADK): Error during ADK agent execution: {e}")
            mada_seed_output = None 
            trace_id_output = f"ERROR_ADK_EXECUTION_{type(e).__name__}"

        if not isinstance(trace_id_output, str):
            trace_id_output = str(trace_id_output)

        return (mada_seed_output, trace_id_output)
