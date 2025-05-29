# Example ComfyUI Workflow: Basic ADK LLM Prompting

This workflow demonstrates how to use the `LcADKConfigNode` and `LcADKGuiInteractionNode` to configure an LLM and send a prompt to it.

## Nodes:

1.  **`LcADKConfigNode` (ADK Configuration Node)**
    *   **Purpose:** Sets up the LLM model and API key.
    *   **Settings:**
        *   `llm_model_name`: (e.g., "gemini-1.5-pro-latest")
        *   `api_key_env_var`: (e.g., "GOOGLE_API_KEY" - ensure this environment variable is set where ComfyUI is running)
        *   `temperature`: (e.g., 0.7)
        *   `max_tokens`: (e.g., 1024)
    *   **Output:** `adk_config`

2.  **`LcADKGuiInteractionNode` (ADK GUI Interaction Node)**
    *   **Purpose:** Sends a user-defined prompt to the configured LLM.
    *   **Inputs:**
        *   `adk_config`: Connect this to the `adk_config` output of the `LcADKConfigNode`.
        *   `prompt`: (User-defined text, e.g., "What is the learnt.cloud project about in one sentence?")
    *   **Output:** `llm_response`

3.  **`ShowTextNode` (or any text display node in ComfyUI)**
    *   **Purpose:** Displays the LLM's response.
    *   **Input:** Connect this to the `llm_response` output of the `LcADKGuiInteractionNode`.

## Workflow Steps:

1.  Add an `LcADKConfigNode` to your ComfyUI graph.
2.  Configure its parameters, especially `llm_model_name` and `api_key_env_var`. Make sure the environment variable specified by `api_key_env_var` is actually set in your system environment where ComfyUI is running and contains a valid API key.
3.  Add an `LcADKGuiInteractionNode`.
4.  Connect the `adk_config` output of the config node to the `adk_config` input of the GUI interaction node.
5.  Type your desired prompt into the `prompt` field of the `LcADKGuiInteractionNode`.
6.  (Optional but Recommended) Add a text display node (like ComfyUI's built-in `ShowTextNode` if available, or a custom one) and connect its input to the `llm_response` output of the `LcADKGuiInteractionNode`.
7.  Queue the prompt. The LLM response should appear in the text display node.

## Expected Behavior:

The workflow will initialize an ADK LLM agent based on the configuration, send the specified prompt, and display the LLM's textual response. If there are issues with API key setup or LLM access, error messages might appear in the ComfyUI console or in the output of the GUI interaction node. The known import issue for `CoreADKAgent` might also prevent the nodes from loading or running correctly.
