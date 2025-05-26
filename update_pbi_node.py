class UpdatePbiNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ()
    FUNCTION = "run"

    def run(self):
        return ()

NODE_CLASS_MAPPINGS = {"UpdatePbiNode": UpdatePbiNode}
