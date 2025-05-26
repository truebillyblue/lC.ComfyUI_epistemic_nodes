class ShowTextNode:
    CATEGORY = "LearntCloud/Utils" # Or just "Utils"
    RETURN_TYPES = () # This node doesn't return anything new to the workflow
    FUNCTION = "execute"
    OUTPUT_NODE = True # Mark as an output node

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}), # Force input
                "label": ("STRING", {"default": "Output:"}) 
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}, # Standard hidden inputs
        }

    def execute(self, text: str, label: str, prompt=None, extra_pnginfo=None):
        # In ComfyUI, "print" statements in the execute method of an OUTPUT_NODE
        # usually appear in the console where ComfyUI is running.
        # For a visual display within ComfyUI, this node would typically prepare
        # data for the UI part of the node (JavaScript) to render.
        # This simple version will print to console.
        # A more advanced version might save text to a file or update UI via websockets.
        
        print(f"--------------------------------")
        print(f"{label}")
        print(f"--------------------------------")
        print(text)
        print(f"--------------------------------")

        # To display in the UI, you'd typically return a dictionary of UI data.
        # For example: return {"ui": {"text": [text]}}
        # This requires a corresponding JavaScript part for the node.
        # For now, we'll keep it simple and rely on console output.
        # If a text preview is desired in a future iteration, that would be added.
        return {} # Must return a dictionary, even if empty for output nodes
