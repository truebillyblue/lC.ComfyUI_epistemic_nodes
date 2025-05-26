from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import uuid # For generating session_id

# ADK Imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event # For type hinting if needed

# Import the custom ADK agent
# The '....' relative import should work if lc_python_core is in the Python path
# and both are part of a larger namespace, or if lc_python_core is installed correctly.
# If ComfyUI runs from a context where 'lab.packages.lc_python_core' is the path,
# this needs to be adjusted.
# For ComfyUI custom nodes, typically the dependent packages are expected to be in site-packages
# or PYTHONPATH. Given the requirements.txt change `../lc_python_core`, 
# `lc_python_core` should be importable directly after installation.
try:
    from lc_python_core.adk_agents import StartleAgent
    from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting
except ImportError:
    # Fallback for local execution if lc_python_core is not yet in the path in a specific test environment.
    # This assumes a specific directory structure for fallback.
    # In a proper ComfyUI environment with dependencies installed, this shouldn't be needed.
    import sys
    import os
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up to 'lab/packages/' and then into 'lc_python_core'
    # This is fragile and depends on the script being in 'lc_ComfyUI_epistemic_nodes'
    lc_core_path = os.path.join(current_dir, '..', 'lc_python_core')
    if lc_core_path not in sys.path:
        sys.path.insert(0, lc_core_path)
    from lc_python_core.adk_agents import StartleAgent
    from lc_python_core.schemas.mada_schema import MadaSeed


class LcStartleNode:
    CATEGORY = "LearntCloud/EpistemicOSI_ADK" # Changed category slightly to indicate ADK version
    RETURN_TYPES = ("MADA_SEED", "STRING",) # mada_seed_L1, trace_id
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
        
        # 1. Construct the input_event dictionary (same as before)
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

        # 2. Instantiate the ADK Agent
        startle_agent_instance = StartleAgent() # Using default name and description

        # 3. Setup ADK Runner and Session Service
        # For ComfyUI nodes, InMemorySessionService is likely appropriate for single executions.
        # If session persistence across node executions is needed later, this could change.
        session_service = InMemorySessionService()
        
        # Give the app_name for Runner. This can be a generic name.
        runner = Runner(
            agent=startle_agent_instance,
            app_name="ComfyUI_ADK_Runner", 
            session_service=session_service
        )

        # 4. Prepare session and initial state
        # A unique session ID for each execution.
        session_id = str(uuid.uuid4())
        
        # The initial state for the ADK agent.
        # The StartleAgent expects "input_event" in the state.
        initial_state_dict = {"input_event": input_event_dict}

        try:
            # Create the session with initial state
            # (user_id and session_id are mandatory for create_session)
            session = session_service.create_session(
                app_name=runner.app_name, # Use app_name from runner
                user_id=user_id, 
                session_id=session_id,
                state=initial_state_dict
            )
            print(f"LcStartleNode (ADK): Created session {session_id} with initial state.")

            # 5. Run the agent
            # The `new_message` parameter for `runner.run()` is often used to pass user input.
            # Since we are putting all necessary data into `initial_state`, 
            # `new_message` can be minimal or a placeholder if required by `run()`.
            # Let's use a minimal content object.
            from google.genai.types import Content, Part
            placeholder_message = Content(role="user", parts=[Part(text="Run StartleAgent")])
            
            # The runner.run() method expects user_id and session_id.
            # It will use the agent and session_service configured in the runner.
            events: List[Event] = list(runner.run(
                user_id=user_id, 
                session_id=session_id,
                new_message=placeholder_message
                # initial_state is handled by session creation.
            ))
            
            print(f"LcStartleNode (ADK): StartleAgent execution completed. Events count: {len(events)}")

            # 6. Retrieve results from the session state
            # The session object should be updated by the service after the run.
            updated_session = session_service.get_session(
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
            # Fallback error values
            mada_seed_output = None 
            trace_id_output = f"ERROR_ADK_EXECUTION_{type(e).__name__}"
            # Optionally, re-raise or handle more gracefully depending on ComfyUI error patterns
            # For now, we'll return the error trace_id and None for mada_seed

        # 7. Return results (MadaSeed object and trace_id string)
        if not isinstance(trace_id_output, str):
            trace_id_output = str(trace_id_output) # Ensure trace_id is a string

        return (mada_seed_output, trace_id_output)