import json
from typing import Optional, Tuple, Dict, Any

# Attempt to import the backend service
try:
    # Adjust path based on actual ComfyUI loading and project structure
    from ....lc_python_core.services.lc_mem_service import link_pbis 
except ImportError:
    print("\n!!! lc_link_pbi_node.py: Failed to import link_pbis from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # Dummy for ComfyUI registration
    def link_pbis(*args, **kwargs) -> Dict[str, Any]:
        return {
            "status": "Error: lc_mem_service.link_pbis not found. Backend not imported.",
            "source_pbi_uid": kwargs.get("source_pbi_uid"),
            "target_pbi_uid": kwargs.get("target_pbi_uid"),
            "link_type": kwargs.get("link_type"),
        }

# Define a minimal MadaSeed type string for ComfyUI type system
MADA_SEED_TYPE = "MADA_SEED"
VALID_LINK_TYPES = ["depends_on", "blocks", "relates_to"]


class LcLinkPbiNode:
    """
    A ComfyUI node to link two Product Backlog Items (PBIs)
    using the lc_mem_service.
    """

    NODE_NAME = "MADA Link PBIs" 
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING")
    RETURN_NAMES = ("mada_seed_out", "status")
    FUNCTION = "execute_link_pbis"
    CATEGORY = "LearntCloud/Backlog"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_pbi_uid": ("STRING", {"multiline": False, "default": ""}),
                "target_pbi_uid": ("STRING", {"multiline": False, "default": ""}),
                "link_type": (VALID_LINK_TYPES, {"default": "relates_to"}),
            },
            "optional": {
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_link_pbis(
        self,
        source_pbi_uid: str,
        target_pbi_uid: str,
        link_type: str,
        requesting_persona_context_json: str = "{}",
        mada_seed_in: Optional[Any] = None  # MadaSeed can be any type for passthrough
    ) -> Tuple[Optional[Any], str]:
        """
        Executes the PBI linking operation.
        """
        if not source_pbi_uid or not source_pbi_uid.strip():
            status_out = "Error: Source PBI UID is required."
            print(f"[LcLinkPbiNode] {status_out}")
            return (mada_seed_in, status_out)
        
        if not target_pbi_uid or not target_pbi_uid.strip():
            status_out = "Error: Target PBI UID is required."
            print(f"[LcLinkPbiNode] {status_out}")
            return (mada_seed_in, status_out)

        if source_pbi_uid.strip() == target_pbi_uid.strip():
            status_out = "Error: Source and Target PBI UIDs cannot be the same."
            print(f"[LcLinkPbiNode] {status_out}")
            return (mada_seed_in, status_out)

        persona_context_dict: Optional[Dict[str, Any]] = None
        if requesting_persona_context_json and requesting_persona_context_json.strip() and requesting_persona_context_json != '{}':
            try:
                persona_context_dict = json.loads(requesting_persona_context_json)
            except json.JSONDecodeError as e:
                status_out = f"Error: Invalid JSON in requesting_persona_context_json: {e}"
                print(f"[LcLinkPbiNode] {status_out}")
                return (mada_seed_in, status_out)
        
        try:
            result = link_pbis(
                source_pbi_uid=source_pbi_uid,
                target_pbi_uid=target_pbi_uid,
                link_type=link_type,
                requesting_persona_context=persona_context_dict
            )
        except Exception as e:
            error_message = f"Error calling link_pbis service: {type(e).__name__} - {str(e)}"
            print(f"[LcLinkPbiNode] {error_message}")
            return (mada_seed_in, error_message)

        status_out = result.get("status", "Error: Status not returned from backend.")
        
        print(f"[LcLinkPbiNode] Source: {source_pbi_uid}, Target: {target_pbi_uid}, Type: {link_type}, Status: {status_out}")

        return (mada_seed_in, status_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcLinkPbiNode": LcLinkPbiNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcLinkPbiNode": "LC Link PBIs Node"
}

if __name__ == "__main__":
    print("Testing LcLinkPbiNode locally...")

    # Mock the backend service if not available
    if "link_pbis" not in globals() or globals()["link_pbis"] is None:
        def mock_backend_link_pbis(source_pbi_uid: str, target_pbi_uid: str, link_type: str, 
                                   requesting_persona_context: Optional[Dict[str, Any]] = None):
            print(f"Mock Backend: Called link_pbis for source '{source_pbi_uid}', target '{target_pbi_uid}', type '{link_type}' with context: {requesting_persona_context}")
            if source_pbi_uid == "src-001" and target_pbi_uid == "tgt-001":
                if source_pbi_uid == target_pbi_uid: # Should be caught by node
                     return {"status": "Error: Cannot link a PBI to itself (mock backend)"}
                return {"status": "Success: PBIs linked (mocked)"}
            elif source_pbi_uid == "src-fail" or target_pbi_uid == "tgt-fail":
                return {"status": "Error: PBI(s) not found (mocked)"}
            return {"status": "Error: Unknown mock failure"}
        
        link_pbis = mock_backend_link_pbis
        print("Using mock backend for link_pbis.")

    node = LcLinkPbiNode()

    # Test case 1: Successful link
    print("\n--- Test Case 1: Successful Link ---")
    persona_ctx_str1 = json.dumps({"user": "linker_user"})
    result1 = node.execute_link_pbis(
        source_pbi_uid="src-001", 
        target_pbi_uid="tgt-001", 
        link_type="depends_on",
        requesting_persona_context_json=persona_ctx_str1
    )
    print(f"Result 1 (Success): {result1}")
    assert result1[1] == "Success: PBIs linked (mocked)"

    # Test case 2: Source PBI UID empty
    print("\n--- Test Case 2: Source PBI UID Empty ---")
    result2 = node.execute_link_pbis(source_pbi_uid="", target_pbi_uid="tgt-001", link_type="relates_to")
    print(f"Result 2 (Empty Source UID): {result2}")
    assert result2[1] == "Error: Source PBI UID is required."

    # Test case 3: Target PBI UID empty
    print("\n--- Test Case 3: Target PBI UID Empty ---")
    result3 = node.execute_link_pbis(source_pbi_uid="src-001", target_pbi_uid="", link_type="blocks")
    print(f"Result 3 (Empty Target UID): {result3}")
    assert result3[1] == "Error: Target PBI UID is required."

    # Test case 4: Source and Target PBI UIDs are the same
    print("\n--- Test Case 4: Same Source and Target PBI UIDs ---")
    result4 = node.execute_link_pbis(source_pbi_uid="src-001", target_pbi_uid="src-001", link_type="depends_on")
    print(f"Result 4 (Same UIDs): {result4}")
    assert result4[1] == "Error: Source and Target PBI UIDs cannot be the same."
    
    # Test case 5: Invalid JSON for persona context
    print("\n--- Test Case 5: Invalid Persona Context JSON ---")
    invalid_persona_json = '{"user": "test_user_2", "broken_json": True' # Intentionally broken
    result5 = node.execute_link_pbis(
        source_pbi_uid="src-001", 
        target_pbi_uid="tgt-001", 
        link_type="relates_to",
        requesting_persona_context_json=invalid_persona_json
    )
    print(f"Result 5 (Invalid JSON): {result5}")
    assert "Error: Invalid JSON" in result5[1]

    # Test case 6: Backend service reports PBI not found
    print("\n--- Test Case 6: Backend PBI Not Found ---")
    result6 = node.execute_link_pbis(source_pbi_uid="src-fail", target_pbi_uid="tgt-001", link_type="depends_on")
    print(f"Result 6 (Backend Not Found): {result6}")
    assert result6[1] == "Error: PBI(s) not found (mocked)"

    # Test case 7: mada_seed_in passthrough
    print("\n--- Test Case 7: Mada Seed Passthrough ---")
    mock_mada_seed = {"seed_value": "alpha_beta_gamma"}
    result7 = node.execute_link_pbis(
        source_pbi_uid="src-001", 
        target_pbi_uid="tgt-001", 
        link_type="relates_to",
        mada_seed_in=mock_mada_seed
    )
    print(f"Result 7 (Mada Seed): {result7}")
    assert result7[0] is mock_mada_seed
    assert result7[1] == "Success: PBIs linked (mocked)"
    
    # Test case 8: Default (empty) persona context JSON
    print("\n--- Test Case 8: Default Persona Context JSON ('{}') ---")
    result8 = node.execute_link_pbis(
        source_pbi_uid="src-001", 
        target_pbi_uid="tgt-001", 
        link_type="depends_on",
        requesting_persona_context_json="{}" # Default empty JSON
    )
    print(f"Result 8 (Default Persona Context): {result8}")
    # Mock backend should receive None for persona_context_dict in this case
    assert result8[1] == "Success: PBIs linked (mocked)"


    print("\nLocal testing finished.")
