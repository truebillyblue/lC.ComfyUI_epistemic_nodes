# ADK LLM Integration Nodes for ComfyUI

This document describes ComfyUI custom nodes designed to integrate Large Language Model (LLM) capabilities using Google's Agent Development Kit (ADK). These nodes interact with the `CoreADKAgent` defined in `lC.pythonCore.lc_adk_agent`.

**Important Note on Imports:**
These nodes attempt to import `CoreADKAgent` from `lC.pythonCore.lc_adk_agent.adk_core_agent`. Due to a known issue with Python's import resolution for directories containing a dot (like `lC.pythonCore`), this import may fail at runtime when ComfyUI attempts to load these nodes, resulting in a `ModuleNotFoundError: No module named 'lC'`. This behavior was observed during unit testing of the core library. The nodes themselves log this import attempt. Successful operation depends on ComfyUI's runtime environment or a future fix for the underlying path resolution.

## 1. ADK Configuration Node (`LcADKConfigNode`)

-   **Purpose:** Configures the parameters for interacting with an LLM via the ADK. This node typically provides its output to other ADK nodes.
-   **Location:** `lc_adk_config_node.py`
-   **Inputs:**
    -   `llm_model_name` (STRING): The identifier of the LLM to use (e.g., "gemini-pro", "gemini-1.5-pro-latest"). Default: "gemini-pro".
    -   `api_key_env_var` (STRING): The **name of the environment variable** that holds the API key for the LLM service (e.g., "GOOGLE_API_KEY"). Default: "GOOGLE_API_KEY". The node will read the value from this environment variable.
    -   `temperature` (FLOAT): The sampling temperature for the LLM (Min: 0.0, Max: 1.0). Default: 0.7.
    -   `max_tokens` (INT): The maximum number of tokens for the LLM response. Default: 2048.
-   **Output:**
    -   `adk_config` (ADK_CONFIG): A dictionary containing the resolved configuration values (including the actual API key read from the environment).

## 2. ADK GUI Interaction Node (`LcADKGuiInteractionNode`)

-   **Purpose:** Provides a direct GUI interface to send a text prompt to an LLM configured by `LcADKConfigNode`.
-   **Location:** `lc_adk_gui_interaction_node.py`
-   **Inputs:**
    -   `adk_config` (ADK_CONFIG): The configuration output from an `LcADKConfigNode`.
    -   `prompt` (STRING): The text prompt to send to the LLM (multiline input enabled).
-   **Output:**
    -   `llm_response` (STRING): The text response from the LLM.

---
*This documentation was created separately as `README_ADK_LLM_Nodes.md` due to technical difficulties updating the main `README.md` in this directory.*
