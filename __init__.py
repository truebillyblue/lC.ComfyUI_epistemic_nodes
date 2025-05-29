from .l1_startle_node import LcStartleNode
from .l2_frame_click_node import LcFrameClickNode
from .l3_keymap_click_node import LcKeymapClickNode
from .l4_anchor_click_node import LcAnchorClickNode
from .l5_field_click_node import LcFieldClickNode
from .l6_reflect_boom_node import LcReflectBoomNode
from .l7_apply_done_node import LcApplyDoneNode
from .show_text_node import ShowTextNode
from .pipeline_node import LcEpistemicPipelineNode
from .get_mada_object_node import GetMadaObjectNode
from .store_mada_object_node import StoreMadaObjectNode
from .initiate_oia_node import InitiateOiaNode
from .view_oia_cycle_node import ViewOiaCycleNode
from .add_observation_node import AddObservationNode
from .add_interpretation_node import AddInterpretationNode
from .add_application_node import AddApplicationNode
from .initiate_rdsotm_cycle_node import InitiateRDSOTMCycleNode
from .create_rdsotm_component_node import CreateRDSOTMComponentNode
from .view_rdsotm_cycle_details_node import ViewRDSOTMCycleDetailsNode
from .create_pbi_node import CreatePbiNode
from .query_pbis_node import QueryPbisNode
from .update_pbi_node import UpdatePbiNode # Add this
from .lc_mem_write_node import LcMemWriteNode
from .lc_get_pbi_details_node import LcGetPbiDetailsNode # New import
from .lc_link_pbi_node import LcLinkPbiNode # New import for Link PBI node
from .lc_add_comment_to_pbi_node import LcAddCommentToPbiNode # New import for Add Comment node
from .lc_api_llm_agent_node import LcApiLlmAgentNode # New import for API LLM Agent node
from .lc_web_llm_agent_node import LcWebLlmAgentNode # New import for Web LLM Agent node
from .lc_adk_config_node import LcADKConfigNode # Import for ADK Config Node
from .lc_adk_gui_interaction_node import LcADKGuiInteractionNode # Import for ADK GUI Interaction Node

NODE_CLASS_MAPPINGS = {
    "LcADKConfigNode": LcADKConfigNode, # ADK Config Node
    "LcADKGuiInteractionNode": LcADKGuiInteractionNode, # ADK GUI Interaction Node
    "LcStartleNode": LcStartleNode,
    "LcFrameClickNode": LcFrameClickNode,
    "LcKeymapClickNode": LcKeymapClickNode,
    "LcAnchorClickNode": LcAnchorClickNode,
    "LcFieldClickNode": LcFieldClickNode,
    "LcReflectBoomNode": LcReflectBoomNode,
    "LcApplyDoneNode": LcApplyDoneNode,
    "ShowTextNode": ShowTextNode,
    "LcEpistemicPipelineNode": LcEpistemicPipelineNode,
    "GetMadaObjectNode": GetMadaObjectNode,
    "StoreMadaObjectNode": StoreMadaObjectNode,
    "InitiateOiaNode": InitiateOiaNode,
    "ViewOiaCycleNode": ViewOiaCycleNode,
    "AddObservationNode": AddObservationNode,
    "AddInterpretationNode": AddInterpretationNode,
    "AddApplicationNode": AddApplicationNode,
    "InitiateRDSOTMCycleNode": InitiateRDSOTMCycleNode,
    "CreateRDSOTMComponentNode": CreateRDSOTMComponentNode,
    "ViewRDSOTMCycleDetailsNode": ViewRDSOTMCycleDetailsNode,
    "CreatePbiNode": CreatePbiNode,
    "QueryPbisNode": QueryPbisNode,
    "UpdatePbiNode": UpdatePbiNode, # Add this
    "LcMemWriteNode": LcMemWriteNode,
    "LcGetPbiDetailsNode": LcGetPbiDetailsNode, # New class mapping
    "LcLinkPbiNode": LcLinkPbiNode, # New class mapping for Link PBI node
    "LcAddCommentToPbiNode": LcAddCommentToPbiNode, # New class mapping for Add Comment node
    "LcApiLlmAgentNode": LcApiLlmAgentNode, # New class mapping for API LLM Agent node
    "LcWebLlmAgentNode": LcWebLlmAgentNode, # New class mapping for Web LLM Agent node
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LcADKConfigNode": "ADK Configuration Node", # ADK Config Node
    "LcADKGuiInteractionNode": "ADK GUI Interaction Node", # ADK GUI Interaction Node
    "LcStartleNode": "lC L1 Startle",
    "LcFrameClickNode": "lC L2 FrameClick",
    "LcKeymapClickNode": "lC L3 KeymapClick",
    "LcAnchorClickNode": "lC L4 AnchorClick",
    "LcFieldClickNode": "lC L5 FieldClick",
    "LcReflectBoomNode": "lC L6 ReflectBoom",
    "LcApplyDoneNode": "lC L7 ApplyDone",
    "ShowTextNode": "Show Text (lC)",
    "LcEpistemicPipelineNode": "lC Epistemic Pipeline (L1-L7)",
    "GetMadaObjectNode": "Get Mada Object (lC)",
    "StoreMadaObjectNode": "Store Mada Object (lC)",
    "InitiateOiaNode": "Initiate OIA Cycle (lC)",
    "ViewOiaCycleNode": "View OIA Cycle (lC)",
    "AddObservationNode": "Add OIA Observation (lC)",
    "AddInterpretationNode": "Add OIA Interpretation (lC)",
    "AddApplicationNode": "Add OIA Application (lC)",
    "InitiateRDSOTMCycleNode": "Initiate RDSOTM Cycle (lC)",
    "CreateRDSOTMComponentNode": "Create RDSOTM Component (lC)",
    "ViewRDSOTMCycleDetailsNode": "View RDSOTM Cycle Details (lC)",
    "CreatePbiNode": "Create PBI (lC)",
    "QueryPbisNode": "Query PBIs (lC)",
    "UpdatePbiNode": "Update PBI (lC)", # Add this
    "LcMemWriteNode": "lC Mem Write",
    "LcGetPbiDetailsNode": "lC Get PBI Details", # New display name mapping
    "LcLinkPbiNode": "lC Link PBIs", # New display name mapping for Link PBI node
    "LcAddCommentToPbiNode": "lC Add Comment to PBI", # New display name mapping for Add Comment node
    "LcApiLlmAgentNode": "lC API LLM Agent", # New display name mapping for API LLM Agent node
    "LcWebLlmAgentNode": "lC Web LLM Agent", # New display name mapping for Web LLM Agent node
}

# This is how we'll refer to the madaSeed object type in ComfyUI
# We are telling ComfyUI that "MADA_SEED" is a valid type, and it will be a Python object.
COMFYUI_CUSTOM_TYPES = {
    "MADA_SEED": {
        "input": ["*"], 
        "output": ["*"] 
    }
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'COMFYUI_CUSTOM_TYPES']
