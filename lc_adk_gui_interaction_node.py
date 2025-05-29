import os

# Attempt to import the CoreADKAgent
core_agent_available = False
CoreADKAgent = None  # Initialize to None

try:
    # Assuming ComfyUI's execution environment might have /app/lab/modules in sys.path
    # or a similar mechanism that would make 'lc_python_core' findable if the naming was standard.
    from lc_python_core.lc_adk_agent.adk_core_agent import CoreADKAgent as ImportedAgent
    if ImportedAgent is not None:
        CoreADKAgent = ImportedAgent # Assign to the global scope if import successful
        core_agent_available = True
        print("INFO: CoreADKAgent imported successfully into lc_adk_gui_interaction_node.")
    else:
        # This case should ideally not happen if the import itself doesn't raise an error
        print("WARNING: CoreADKAgent was None after import in lc_adk_gui_interaction_node.")
        # CoreADKAgent remains None, core_agent_available remains False
except ImportError as e:
    print(f"ERROR: Failed to import CoreADKAgent in GUI Interaction Node: {e}")
    print("Ensure lc_python_core is accessible. This might be a path issue related to 'lc_python_core' naming.")
    # CoreADKAgent remains None, core_agent_available remains False
except Exception as e: # Catch any other exception during import
    print(f"ERROR: An unexpected error occurred during CoreADKAgent import in GUI Interaction Node: {e}")
    # CoreADKAgent remains None, core_agent_available remains False


class LcADKGuiInteractionNode:
    CATEGORY = "LearntCloud/ADK"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("llm_response",)
    FUNCTION = "execute_llm_prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "adk_config": ("ADK_CONFIG",),
                "prompt": ("STRING", {"multiline": True, "default": "Explain quantum computing in simple terms."})
            }
        }

    def execute_llm_prompt(self, adk_config: dict, prompt: str):
        """
        Executes the LLM prompt using the CoreADKAgent.
        """
        if not core_agent_available or CoreADKAgent is None:
            error_message = "CoreADKAgent could not be imported or is not available. Cannot execute LLM prompt."
            print(f"LcADKGuiInteractionNode: {error_message}")
            return (error_message,)

        config_dict = adk_config 
        llm_model = config_dict.get("llm_model_name")
        api_key = config_dict.get("api_key")
        # Optional: temperature = config_dict.get("temperature")
        # Optional: max_tokens = config_dict.get("max_tokens")

        if not llm_model or not api_key:
            error_message = "Error: Missing LLM model name or API key in ADK config."
            print(f"LcADKGuiInteractionNode: {error_message}")
            return (error_message,)
        
        try:
            # Assuming CoreADKAgent constructor takes model_name and api_key.
            # Adjust if it takes the full config dict or other params.
            agent = CoreADKAgent(llm_model_name=llm_model, api_key=api_key)
        except Exception as e:
            error_message = f"Error instantiating CoreADKAgent: {str(e)}"
            print(f"LcADKGuiInteractionNode: {error_message}")
            return (error_message,)

        try:
            response = agent.execute_prompt(prompt)
            return (response,)
        except Exception as e:
            error_message = f"Error during LLM prompt execution: {str(e)}"
            print(f"LcADKGuiInteractionNode: {error_message}")
            return (error_message,)

# Print a message to confirm the class definition is processed
print("INFO: LcADKGuiInteractionNode class defined.")
