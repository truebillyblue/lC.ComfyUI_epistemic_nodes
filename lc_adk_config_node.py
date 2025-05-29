# import os # Removed as os.getenv is no longer used

# Attempt to import the CoreADKAgent
# It's acknowledged that there were issues testing lc_python_core due to its name.
# ComfyUI's runtime environment might handle this path correctly.
# However, given the persistent ModuleNotFoundError: No module named 'lC'
# when sys.path includes /app/lab/modules, it's highly probable this import
# will fail in ComfyUI's environment too if lc_python_core is not renamed.
core_agent_imported = False
try:
    # Assuming ComfyUI's execution environment might have /app/lab/modules in sys.path
    # or a similar mechanism that would make 'lc_python_core' findable if the naming was standard.
    from lc_python_core.lc_adk_agent.adk_core_agent import CoreADKAgent
    if CoreADKAgent is not None:
        core_agent_imported = True
        print("INFO: CoreADKAgent imported successfully into lc_adk_config_node.")
    else:
        print("WARNING: CoreADKAgent was None after import in lc_adk_config_node.")
        CoreADKAgent = object # Placeholder to prevent NameError if import returns None
except ImportError as e:
    print(f"ERROR: Failed to import CoreADKAgent in lc_adk_config_node: {e}")
    print("Ensure lc_python_core is accessible. This might be a path issue related to 'lc_python_core' naming.")
    CoreADKAgent = object # Define a placeholder to allow class definition
except Exception as e: # Catch any other exception during import
    print(f"ERROR: An unexpected error occurred during CoreADKAgent import in lc_adk_config_node: {e}")
    CoreADKAgent = object


class LcADKConfigNode:
    CATEGORY = "LearntCloud/ADK"
    RETURN_TYPES = ("ADK_CONFIG",)
    RETURN_NAMES = ("adk_config",)
    FUNCTION = "configure_agent"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_model_name": ("STRING", {"default": "gemini-pro"}),
                "api_key": ("STRING", {"default": "PASTE_YOUR_GOOGLE_API_KEY_HERE", "multiline": False}), # Modified
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 2048, "min": 1}),
            }
        }

    def configure_agent(self, llm_model_name: str, api_key: str, temperature: float, max_tokens: int): # Modified signature
        """
        Configures the ADK agent settings and returns them as a dictionary.
        The API key is now taken directly as input.
        """
        # Removed os.getenv call and associated error checking for api_key_env_var
        # The api_key parameter is now the direct key value.

        if not api_key or api_key == "PASTE_YOUR_GOOGLE_API_KEY_HERE":
             # It's good practice to check if the user actually changed the default placeholder.
            raise ValueError("API key is missing or still set to the placeholder. Please provide a valid Google API Key.")

        # For now, we are just returning a configuration dictionary.
        # If CoreADKAgent was successfully imported and intended to be used here,
        # this is where it might be instantiated or further configured.
        # However, given the import issues, returning a dictionary is safer.
        
        config = {
            "llm_model_name": llm_model_name,
            "api_key": api_key,  # This is now the direct key value
            "temperature": temperature,
            "max_tokens": max_tokens,
            "core_agent_imported": core_agent_imported # For debugging/info
            # Add any other relevant ADK parameters here
        }
        
        # The tuple is important for ComfyUI's return value handling
        return (config,)

# Example of how this might be registered in __init__.py for the nodes package
# NODE_CLASS_MAPPINGS = {
#     "LcADKConfigNode": LcADKConfigNode
# }
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "LcADKConfigNode": "ADK Configuration Node"
# }

# Print a message to confirm the class definition is processed
print("INFO: LcADKConfigNode class defined with direct API key input.")
