# Learnt.Cloud Epistemic OSI Nodes for ComfyUI (`lc_epistemic_nodes`)

This package provides a set of custom nodes for ComfyUI that implement the Learnt.Cloud Epistemic OSI model (Layers L1-L7). These nodes allow users to visually construct and execute epistemic processing pipelines as defined in the `_lC.Core - Common - v0.1.2.2.md` doctrine.

The central data object passed between these nodes is the `MadaSeed`, which is progressively built and processed by each layer.

## Installation

1.  **Place this directory (`lc_epistemic_nodes`)** into your `ComfyUI/custom_nodes/` directory.
2.  **Ensure `lc_python_core` is accessible**: This package depends on the `lc_python_core` package, which contains the underlying Python implementations for the Standard Operating Procedures (SOPs) and the `MadaSeed` Pydantic data models.
    *   The `lc_python_core` directory (expected at `../../lc_python_core/` relative to this README, i.e., in a parallel `frontends` subdirectory) must be in your Python import path. You can achieve this by:
        *   Adding the parent directory (`lab/frontends/` in the typical project structure) to your `PYTHONPATH` environment variable.
        *   Or, by installing `lc_python_core` as a Python package (e.g., using `pip install -e /path/to/lab/frontends/lc_python_core`).
3.  **Install Dependencies**: Some nodes may require additional Python packages. Ensure you have them installed in your ComfyUI's Python environment (e.g., `pip install pydantic requests playwright`). For Playwright, also run `playwright install` to get browser binaries.
4.  **Restart ComfyUI**: After placing the nodes, ensuring `lc_python_core` is accessible, and installing dependencies, restart ComfyUI. The nodes should then appear in the "LearntCloud/EpistemicOSI", "LearntCloud/MADA", "LearntCloud/Backlog", "LearntCloud/Agents", and "LearntCloud/Utils" categories.

## Nodes Provided

### Epistemic OSI Layers & Pipeline

These nodes process the `MadaSeed` object through the Learnt.Cloud epistemic stack.

*   **lC Epistemic Pipeline (L1-L7) (`LcEpistemicPipelineNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `input_text` (STRING), and optional overrides for each layer (e.g., `l1_origin_hint`, `l2_communication_context_hints`, etc.).
    *   Outputs: `final_mada_seed` (MADA_SEED), `trace_id` (STRING), `l6_reflection_summary` (STRING), `l7_application_summary` (STRING), `l7_next_steps` (STRING).
    *   Description: Encapsulates the entire L1-L7 epistemic processing pipeline into a single node for convenience. It internally calls the SOPs from `lc_python_core` in sequence.

*   **lC L1 Startle (`LcStartleNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `input_text` (STRING), `origin_hint` (STRING, optional), `optional_attachments_ref` (STRING, optional).
    *   Outputs: `mada_seed_L1` (MADA_SEED), `trace_id` (STRING).
    *   Description: Initiates a new `MadaSeed` based on raw input.

*   **lC L2 FrameClick (`LcFrameClickNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED), `communication_context_hints` (STRING, JSON format, optional).
    *   Outputs: `mada_seed_L2` (MADA_SEED).
    *   Description: Performs structural framing and validation.

*   **lC L3 KeymapClick (`LcKeymapClickNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED).
    *   Outputs: `mada_seed_L3` (MADA_SEED).
    *   Description: Conducts surface semantic mapping.

*   **lC L4 AnchorClick (`LcAnchorClickNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED), `persona_profile_uid` (STRING, optional).
    *   Outputs: `mada_seed_L4` (MADA_SEED).
    *   Description: Performs perspectival anchoring and AAC assessability mapping.

*   **lC L5 FieldClick (`LcFieldClickNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED), `field_instance_uid_override` (STRING, optional).
    *   Outputs: `mada_seed_L5` (MADA_SEED).
    *   Description: Activates/updates epistemic field and maps dynamics.

*   **lC L6 ReflectBoom (`LcReflectBoomNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED), `presentation_intent_override` (STRING, optional).
    *   Outputs: `mada_seed_L6` (MADA_SEED), `reflection_text_summary` (STRING).
    *   Description: Reflects field state and prepares a presentation payload.

*   **lC L7 ApplyDone (`LcApplyDoneNode`)**:
    *   Category: `LearntCloud/EpistemicOSI`
    *   Inputs: `mada_seed_in` (MADA_SEED), `l7_action_intent_override` (STRING, optional).
    *   Outputs: `final_mada_seed` (MADA_SEED), `application_summary_text` (STRING), `next_step_options_text` (STRING).
    *   Description: Applies action based on reflection and finalizes the `MadaSeed`.
    *   **Note on ADK Agent Invocation**: If `l7_action_intent_override` is set to "ProcessWithADKAgent", this node's underlying L7 SOP in `lc_python_core` will attempt to call the `lc_adk_agent` to process a query derived from the L6 reflection payload. The ADK agent's string output will be included in one of the `seed_outputs` of the final `MadaSeed`.

### MADA Interaction Nodes (Local File-System Backend)

These nodes allow basic interaction with the Memory-Aware Data Architecture (MADA).
**Note:** These nodes interact with a local file-system-based MADA service provided by `lc_python_core.services.lc_mem_service.py`. Data objects are stored in the `lab/.data/mada_vault/objects/` directory in your local repository. This is an initial implementation step towards a full MADA backend.

*   **Get Mada Object (lC) (`GetMadaObjectNode`)**:
    *   Category: `LearntCloud/MADA`
    *   Inputs: `object_uid` (STRING), `requesting_persona_context_json` (STRING, JSON format).
    *   Outputs: `mada_object_content` (STRING, JSON format), `retrieval_status` (STRING).
    *   Description: Attempts to retrieve a MADA object by its CRUX UID using the `lc_mem_service.py`. (Note: This node currently uses a mock service).

*   **Store Mada Object (lC) (`StoreMadaObjectNode`)**:
    *   Category: `LearntCloud/MADA`
    *   Inputs: `object_payload_json` (STRING, JSON format), `object_type` (STRING), `requesting_persona_context_json` (STRING, JSON format), `initial_metadata_json` (STRING, JSON format, optional).
    *   Outputs: `new_object_uid` (STRING), `storage_status` (STRING).
    *   Description: Simulates storing a MADA object and generating a new CRUX UID using the `lc_mem_service.py`. (Note: This node currently uses a mock service for object creation).

*   **MADA Write Object (`LcMemWriteNode`)**:
    *   Category: `LearntCloud/MADA`
    *   Purpose: To write data to MADA (create new or update existing MADA objects).
    *   Inputs: `object_payload_json (STRING)`, `object_type (STRING)`, `requesting_persona_context_json (STRING, optional)`, `object_uid_to_update (STRING, optional)`, `initial_metadata_json (STRING, optional)`, `update_metadata_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `object_uid (STRING)`, `storage_status (STRING)`, `version (STRING)`.
    *   Description: Creates a new MADA object or updates an existing one using the `lc_mem_service.py`. This service stores objects as JSON files in the local file system (`lab/.data/mada_vault/objects/`).

### Backlog Management Nodes (Local File-System Backend)

These nodes facilitate the management of Product Backlog Items (PBIs).
**Note:** These nodes interact with the local file-system-based MADA service (`lc_mem_service.py`). PBI data is stored in the `lab/.data/mada_vault/pbis/` directory in your local repository.

*   **LC Get PBI Details Node (`LcGetPbiDetailsNode`)**:
    *   Category: `LearntCloud/Backlog`
    *   Purpose: Retrieves details for a Product Backlog Item (PBI).
    *   Inputs: `pbi_uid (STRING)`, `requesting_persona_context_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `pbi_details_json (STRING)`, `status (STRING)`.
    *   Description: Fetches the full details of a PBI given its UID.

*   **LC Link PBIs Node (`LcLinkPbiNode`)**:
    *   Category: `LearntCloud/Backlog`
    *   Purpose: Links two PBIs with a specified relationship type.
    *   Inputs: `source_pbi_uid (STRING)`, `target_pbi_uid (STRING)`, `link_type (COMBO: "depends_on", "blocks", "relates_to")`, `requesting_persona_context_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `status (STRING)`.
    *   Description: Creates a link (e.g., "depends_on") between two PBIs. Updates both PBI files to reflect the relationship.

*   **LC Add Comment to PBI (`LcAddCommentToPbiNode`)**:
    *   Category: `LearntCloud/Backlog`
    *   Purpose: Adds a comment to a PBI.
    *   Inputs: `pbi_uid (STRING)`, `comment_text (STRING)`, `author_persona_uid (STRING)`, `requesting_persona_context_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `comment_id (STRING)`, `status (STRING)`.
    *   Description: Appends a new comment to the specified PBI's comment list.

### Agent Interaction Nodes

These nodes allow interaction with external agents or services.

*   **LLM API Agent (`LcApiLlmAgentNode`)**:
    *   Category: `LearntCloud/Agents`
    *   Purpose: To interact with LLM agents via direct API calls.
    *   Inputs: `api_endpoint_url (STRING)`, `prompt_text (STRING)`, `api_key_env_var (STRING, optional)`, `request_payload_template_json (STRING, optional)`, `conversation_history_json (STRING, optional)`, `response_extraction_path (STRING, optional)`, `request_parameters_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `agent_response_text (STRING)`, `full_api_response_json (STRING)`, `status (STRING)`.
    *   Description: Constructs and sends a request to an LLM API endpoint and processes the response. Uses `lc_api_agent_service.py`.

*   **Web LLM Agent (`LcWebLlmAgentNode`)**:
    *   Category: `LearntCloud/Agents`
    *   Purpose: To interact with web pages or web-based LLM agents via browser automation.
    *   Inputs: `target_url (STRING)`, `interaction_script_json (STRING)`, `browser_control_params_json (STRING, optional)`, `mada_seed_in (MADA_SEED, optional)`.
    *   Outputs: `mada_seed_out (MADA_SEED)`, `extracted_data_json (STRING)`, `interaction_log_json (STRING)`, `status (STRING)`.
    *   Description: Uses Playwright (via `lc_web_agent_service.py`) to perform a sequence of actions on a web page, such as navigation, typing, clicking, and extracting text or attributes.

### OIA Cycle Interaction Nodes (Local File-System Backend)

These nodes facilitate the management of Observe-Interpret-Apply (OIA) cycles. They interact with OIA cycle management SOPs defined in `lc_python_core.sops.meta_sops.sop_oia_cycle_management` which, in turn, use the local file-system-based MADA service to persist OIA cycle data.

*   **Initiate OIA Cycle (lC) (`InitiateOiaNode`)**:
    *   Inputs: `cycle_name` (STRING, optional), `initial_focus_prompt` (STRING, optional), `related_trace_id` (STRING, optional).
    *   Output: `oia_cycle_uid` (STRING).
    *   Description: Creates a new OIA cycle MADA object and returns its UID.

*   **Add OIA Observation (lC) (`AddObservationNode`)**:
    *   Inputs: `oia_cycle_uid` (STRING), `summary` (STRING), `data_source_mada_uid` (STRING, optional), `raw_observation_ref` (STRING, optional).
    *   Outputs: `oia_cycle_uid` (STRING), `observation_id` (STRING).
    *   Description: Adds an observation component to the specified OIA cycle.

*   **Add OIA Interpretation (lC) (`AddInterpretationNode`)**:
    *   Inputs: `oia_cycle_uid` (STRING), `summary` (STRING), `timeless_principles_extracted_str` (STRING, semicolon-separated, optional), `incongruence_flags_str` (STRING, semicolon-separated, optional), `references_observation_ids_str` (STRING, semicolon-separated, optional).
    *   Outputs: `oia_cycle_uid` (STRING), `interpretation_id` (STRING).
    *   Description: Adds an interpretation component to the specified OIA cycle.

*   **Add OIA Application (lC) (`AddApplicationNode`)**:
    *   Inputs: `oia_cycle_uid` (STRING), `summary_of_action` (STRING), `target_mada_uid` (STRING, optional), `outcome_mada_seed_trace_id` (STRING, optional), `references_interpretation_ids_str` (STRING, semicolon-separated, optional).
    *   Outputs: `oia_cycle_uid` (STRING), `application_id` (STRING).
    *   Description: Adds an application component to the specified OIA cycle.

*   **View OIA Cycle (lC) (`ViewOiaCycleNode`)**:
    *   Input: `oia_cycle_uid` (STRING).
    *   Output: `oia_cycle_summary` (STRING, JSON formatted).
    *   Description: Retrieves and displays the current state of an OIA cycle as a JSON string. (Output node, also prints to console).

### RDSOTM Cycle & Component Interaction Nodes (Local File-System Backend)

These nodes facilitate the management of r(DSOTM) (reality, Doctrine, Strategy, Operations, Tactics, Missions) cycles and their components. They interact with SOPs defined in `lc_python_core.sops.meta_sops.sop_rdsotm_management` which use the local file-system-based MADA service to persist r(DSOTM) data.

*   **Initiate RDSOTM Cycle (lC) (`InitiateRDSOTMCycleNode`)**:
    *   Inputs: `cycle_name` (STRING, optional).
    *   Output: `cycle_linkage_uid` (STRING).
    *   Description: Creates a new r(DSOTM) cycle linkage MADA object and returns its UID.

*   **Create RDSOTM Component (lC) (`CreateRDSOTMComponentNode`)**:
    *   Inputs: `cycle_linkage_uid` (STRING), `component_type` (COMBO: Doctrine, Strategy, etc.), `name` (STRING), `description` (STRING), `content_text` (STRING), `related_component_uids_str` (STRING, semicolon-separated, optional), `specific_fields_json` (STRING, JSON, optional).
    *   Outputs: `cycle_linkage_uid` (STRING, passthrough), `component_uid` (STRING).
    *   Description: Creates a new r(DSOTM) component (e.g., a Doctrine or Strategy document), stores its main content in a separate MADA text object, links it to the specified cycle, and returns the new component's UID.

*   **View RDSOTM Cycle Details (lC) (`ViewRDSOTMCycleDetailsNode`)**:
    *   Inputs: `cycle_linkage_uid` (STRING), `resolve_component_summaries` (BOOLEAN, default: True).
    *   Output: `cycle_details_json` (STRING, JSON formatted).
    *   Description: Retrieves and displays the details of an r(DSOTM) cycle, optionally including summaries of its linked components, as a JSON string. (Output node, also prints to console).

### Utility Nodes

*   **Show Text (lC) (`ShowTextNode`)**:
    *   Inputs: `text` (STRING), `label` (STRING, optional).
    *   Outputs: None (Output Node).
    *   Description: Prints the input text to the console where ComfyUI is running. Useful for debugging string outputs from other nodes.

## Workflow Example

Sample workflows are provided in the `ComfyUI/workflows/` directory (relative to the main project root):
*   `lc_epistemic_pipeline.json`: Demonstrates the L1-L7 epistemic pipeline.
*   `lc_oia_cycle_test_workflow.json`: Demonstrates creating and managing an OIA cycle.
*   `lc_rdsotm_test_workflow.json`: Demonstrates creating and managing r(DSOTM) cycles and components.

## Dependencies

*   **`lc_python_core` package**: Contains the Python SOP implementations and `MadaSeed` Pydantic models. This must be installed or available in the `PYTHONPATH`.
*   **External Libraries**: Some nodes or underlying services may require libraries like `requests`, `playwright`, etc. Ensure these are installed in your Python environment (e.g., `pip install requests playwright pydantic`). For Playwright, you also need to install browser binaries using `playwright install`.
#   l C . C o m f y U I _ e p i s t e m i c _ n o d e s  
 