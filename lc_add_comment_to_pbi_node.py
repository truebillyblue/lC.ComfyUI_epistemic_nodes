import json
from typing import Optional, Tuple, Dict, Any

# Attempt to import the backend service
try:
    # Adjust path based on actual ComfyUI loading and project structure
    from lc_python_core.services.lc_mem_service import add_comment_to_pbi
except ImportError:
    print("\n!!! lc_add_comment_to_pbi_node.py: Failed to import add_comment_to_pbi from default path. !!!")
    print("!!! Ensure lc_python_core is in PYTHONPATH or adjust import path. !!!\n")
    # Dummy for ComfyUI registration
    def add_comment_to_pbi(*args, **kwargs) -> Dict[str, Any]:
        return {
            "status": "Error: lc_mem_service.add_comment_to_pbi not found. Backend not imported.",
            "pbi_uid": kwargs.get("pbi_uid"),
            "comment_id": None,
        }

# Define a minimal MadaSeed type string for ComfyUI type system
MADA_SEED_TYPE = "MADA_SEED"


class LcAddCommentToPbiNode:
    """
    A ComfyUI node to add a comment to a Product Backlog Item (PBI)
    using the lc_mem_service.
    """

    NODE_NAME = "MADA Add Comment to PBI" 
    RETURN_TYPES = (MADA_SEED_TYPE, "STRING", "STRING") # mada_seed_out, comment_id, status
    RETURN_NAMES = ("mada_seed_out", "comment_id", "status")
    FUNCTION = "execute_add_comment"
    CATEGORY = "LearntCloud/Backlog"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pbi_uid": ("STRING", {"multiline": False, "default": ""}),
                "comment_text": ("STRING", {"multiline": True, "default": ""}),
                "author_persona_uid": ("STRING", {"multiline": False, "default": "urn:crux:uid::ComfyUIUser"}),
            },
            "optional": {
                "requesting_persona_context_json": ("STRING", {"multiline": True, "default": "{}"}),
                "mada_seed_in": (MADA_SEED_TYPE,),
            }
        }

    def execute_add_comment(
        self,
        pbi_uid: str,
        comment_text: str,
        author_persona_uid: str,
        requesting_persona_context_json: str = "{}",
        mada_seed_in: Optional[Any] = None
    ) -> Tuple[Optional[Any], Optional[str], str]:
        """
        Executes the PBI comment addition operation.
        """
        if not pbi_uid or not pbi_uid.strip():
            status_out = "Error: PBI UID is required."
            print(f"[LcAddCommentToPbiNode] {status_out}")
            return (mada_seed_in, None, status_out)
        
        if not comment_text or not comment_text.strip():
            status_out = "Error: Comment text is required."
            print(f"[LcAddCommentToPbiNode] {status_out}")
            return (mada_seed_in, None, status_out)

        if not author_persona_uid or not author_persona_uid.strip():
            status_out = "Error: Author Persona UID is required."
            print(f"[LcAddCommentToPbiNode] {status_out}")
            return (mada_seed_in, None, status_out)

        persona_context_dict: Optional[Dict[str, Any]] = None
        if requesting_persona_context_json and requesting_persona_context_json.strip() and requesting_persona_context_json != '{}':
            try:
                persona_context_dict = json.loads(requesting_persona_context_json)
            except json.JSONDecodeError as e:
                status_out = f"Error: Invalid JSON in requesting_persona_context_json: {e}"
                print(f"[LcAddCommentToPbiNode] {status_out}")
                return (mada_seed_in, None, status_out)
        
        try:
            result = add_comment_to_pbi(
                pbi_uid=pbi_uid,
                comment_text=comment_text,
                author_persona_uid=author_persona_uid,
                requesting_persona_context=persona_context_dict
            )
        except Exception as e:
            error_message = f"Error calling add_comment_to_pbi service: {type(e).__name__} - {str(e)}"
            print(f"[LcAddCommentToPbiNode] {error_message}")
            return (mada_seed_in, None, error_message)

        comment_id_out = result.get("comment_id")
        status_out = result.get("status", "Error: Status not returned from backend.")
        
        print(f"[LcAddCommentToPbiNode] PBI UID: {pbi_uid}, Author: {author_persona_uid}, CommentID: {comment_id_out}, Status: {status_out}")

        return (mada_seed_in, comment_id_out, status_out)


# ComfyUI mapping for custom nodes
NODE_CLASS_MAPPINGS = {
    "LcAddCommentToPbiNode": LcAddCommentToPbiNode
}

# Optional: A display name mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "LcAddCommentToPbiNode": "LC Add Comment to PBI"
}

if __name__ == "__main__":
    print("Testing LcAddCommentToPbiNode locally...")

    # Mock the backend service if not available
    if "add_comment_to_pbi" not in globals() or globals()["add_comment_to_pbi"] is None:
        def mock_backend_add_comment(pbi_uid: str, comment_text: str, author_persona_uid: str, 
                                     requesting_persona_context: Optional[Dict[str, Any]] = None):
            print(f"Mock Backend: Called add_comment_to_pbi for PBI '{pbi_uid}', author '{author_persona_uid}', text '{comment_text[:30]}...' with context: {requesting_persona_context}")
            if pbi_uid == "pbi-exists-001":
                if not comment_text.strip(): # Handled by node
                    return {"status": "Error: Comment text cannot be empty (mock backend)", "pbi_uid": pbi_uid, "comment_id": None}
                new_comment_id = f"cmt_mock_{hash(comment_text)[:6]}"
                return {"status": "Success: Comment added (mocked)", "pbi_uid": pbi_uid, "comment_id": new_comment_id}
            elif pbi_uid == "pbi-not-found-002":
                return {"status": "Error: PBI not found (mocked)", "pbi_uid": pbi_uid, "comment_id": None}
            return {"status": "Error: Unknown mock failure for add_comment"}
        
        add_comment_to_pbi = mock_backend_add_comment
        print("Using mock backend for add_comment_to_pbi.")

    node = LcAddCommentToPbiNode()

    # Test case 1: Successful comment addition
    print("\n--- Test Case 1: Successful Comment Addition ---")
    persona_ctx_str1 = json.dumps({"user_id": "commenter_001"})
    result1 = node.execute_add_comment(
        pbi_uid="pbi-exists-001", 
        comment_text="This is a test comment.",
        author_persona_uid="persona-user-123",
        requesting_persona_context_json=persona_ctx_str1
    )
    print(f"Result 1 (Success): {result1}")
    assert result1[2] == "Success: Comment added (mocked)"
    assert result1[1] is not None # comment_id should be returned

    # Test case 2: PBI UID empty
    print("\n--- Test Case 2: PBI UID Empty ---")
    result2 = node.execute_add_comment(pbi_uid="", comment_text="A comment.", author_persona_uid="user-x")
    print(f"Result 2 (Empty PBI UID): {result2}")
    assert result2[2] == "Error: PBI UID is required."
    assert result2[1] is None

    # Test case 3: Comment text empty
    print("\n--- Test Case 3: Comment Text Empty ---")
    result3 = node.execute_add_comment(pbi_uid="pbi-exists-001", comment_text="   ", author_persona_uid="user-y")
    print(f"Result 3 (Empty Comment Text): {result3}")
    assert result3[2] == "Error: Comment text is required."
    assert result3[1] is None

    # Test case 4: Author Persona UID empty
    print("\n--- Test Case 4: Author Persona UID Empty ---")
    result4 = node.execute_add_comment(pbi_uid="pbi-exists-001", comment_text="Valid comment.", author_persona_uid="")
    print(f"Result 4 (Empty Author UID): {result4}")
    assert result4[2] == "Error: Author Persona UID is required."
    assert result4[1] is None
    
    # Test case 5: Invalid JSON for persona context
    print("\n--- Test Case 5: Invalid Persona Context JSON ---")
    invalid_persona_json = '{"user_id": "commenter_002", "malformed_json": True' 
    result5 = node.execute_add_comment(
        pbi_uid="pbi-exists-001", 
        comment_text="Another comment.",
        author_persona_uid="persona-user-456",
        requesting_persona_context_json=invalid_persona_json
    )
    print(f"Result 5 (Invalid JSON): {result5}")
    assert "Error: Invalid JSON" in result5[2]
    assert result5[1] is None

    # Test case 6: Backend service reports PBI not found
    print("\n--- Test Case 6: Backend PBI Not Found ---")
    result6 = node.execute_add_comment(
        pbi_uid="pbi-not-found-002", 
        comment_text="Comment for a ghost PBI.",
        author_persona_uid="persona-user-789"
    )
    print(f"Result 6 (Backend PBI Not Found): {result6}")
    assert result6[2] == "Error: PBI not found (mocked)"
    assert result6[1] is None

    # Test case 7: mada_seed_in passthrough
    print("\n--- Test Case 7: Mada Seed Passthrough ---")
    mock_mada_seed = {"data_point": "comment_seed_XYZ"}
    result7 = node.execute_add_comment(
        pbi_uid="pbi-exists-001", 
        comment_text="Comment with a seed.",
        author_persona_uid="persona-user-seeded",
        mada_seed_in=mock_mada_seed
    )
    print(f"Result 7 (Mada Seed): {result7}")
    assert result7[0] is mock_mada_seed
    assert result7[2] == "Success: Comment added (mocked)"
    assert result7[1] is not None

    print("\nLocal testing finished.")
