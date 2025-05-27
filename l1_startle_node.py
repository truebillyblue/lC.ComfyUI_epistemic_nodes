import asyncio
import json
from typing import Any
from google.adk.sessions import InMemorySessionService
from lc_python_core.adk_agents import StartleAgent

class LcStartleNode:
    RETURN_TYPES = ("MADA_SEED", "STRING",)
    RETURN_NAMES = ("mada_seed_L1", "trace_id",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        print("[LcStartleNode] INPUT_TYPES() called")
        return {
            "required": {
                "input_text": ("STRING", {"default": "startle reflex"}),
                "origin_hint": ("STRING", {"default": "ComfyUI_LcStartleNode_ADK"}),
                "optional_attachments_ref": ("STRING", {"default": ""}),
                "user_id": ("STRING", {"default": "ComfyUI_User"}),
            }
        }

    def execute(self, input_text: str, origin_hint: str, optional_attachments_ref: str, user_id: str):
        print("=== [LcStartleNode] ENTERING execute() ===")
        print(f"[LcStartleNode] input_text = '{input_text}'")
        print(f"[LcStartleNode] origin_hint = '{origin_hint}'")
        print(f"[LcStartleNode] optional_attachments_ref = '{optional_attachments_ref}'")
        print(f"[LcStartleNode] user_id = '{user_id}'")
        try:
            result = asyncio.run(self._run_async(input_text, origin_hint, optional_attachments_ref, user_id))
            print("=== [LcStartleNode] EXITING execute() successfully ===")
            return result
        except Exception as e:
            print(f"[LcStartleNode] ERROR in execute(): {e}")
            return ({}, "ERROR_EXECUTE")

    async def _run_async(self, input_text: str, origin_hint: str, optional_attachments_ref: str, user_id: str):
        print("=== [LcStartleNode] ENTERING _run_async() ===")
        session_service = InMemorySessionService()
        print("[LcStartleNode] Created InMemorySessionService")

        session = await session_service.create_session(app_name="lc_startle", user_id=user_id)
        print(f"[LcStartleNode] Created session")

        initial_state = {
            "input_event": {
                "reception_timestamp_utc_iso": "2025-05-26T18:32:56Z",
                "origin_hint": origin_hint,
                "data_components": [
                    {
                        "role_hint": "primary_text_content",
                        "content_handle_placeholder": input_text,
                        "size_hint": len(input_text.encode("utf-8")),
                        "type_hint": "text/plain"
                    }
                ]
            }
        }

        print(f"[LcStartleNode] Initial session state = {initial_state}")
        session.state.update(initial_state)
        print("[LcStartleNode] Updated session with initial state")

        try:
            startle_agent_instance = StartleAgent()
            print("[LcStartleNode] Instantiated StartleAgent")

            await startle_agent_instance.run(session)
            print("[LcStartleNode] Finished running StartleAgent")

            updated_session = await session_service.get_session(session=session)
            print("[LcStartleNode] Retrieved updated session")
            print(f"[LcStartleNode] Updated session state keys: {list(updated_session.state.keys())}")

            trace_id = updated_session.state.get("trace_id", "NO_TRACE_ID")
            mada_seed_output = updated_session.state.get("mada_seed_output", None)

            print(f"[LcStartleNode] Output trace_id: {trace_id}")
            print(f"[LcStartleNode] Output mada_seed_output present? {'YES' if mada_seed_output else 'NO'}")
            print("=== [LcStartleNode] EXITING _run_async() ===")
            return (mada_seed_output, trace_id)

        except Exception as e:
            print(f"[LcStartleNode] ERROR during _run_async(): {e}")
            return ({}, "ERROR_RUN_ASYNC")
