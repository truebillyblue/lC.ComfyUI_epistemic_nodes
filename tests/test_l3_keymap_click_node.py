import unittest
from unittest.mock import patch, MagicMock

from lc_python_core.schemas.mada_schema import MadaSeed # For type hinting and creating mock instances
from lc_comfyui_epistemic_nodes.l3_keymap_click_node import LcKeymapClickNode

class TestLcKeymapClickNode(unittest.TestCase):

    def test_node_attributes(self):
        """Test basic attributes of the LcKeymapClickNode."""
        self.assertEqual(LcKeymapClickNode.CATEGORY, "LearntCloud/EpistemicOSI")
        self.assertEqual(LcKeymapClickNode.RETURN_TYPES, ("MADA_SEED",))
        self.assertEqual(LcKeymapClickNode.RETURN_NAMES, ("mada_seed_L3",))
        self.assertEqual(LcKeymapClickNode.FUNCTION, "execute")

    def test_input_types(self):
        """Test the INPUT_TYPES class method."""
        input_types = LcKeymapClickNode.INPUT_TYPES()
        self.assertIn("required", input_types)
        self.assertIn("mada_seed_in", input_types["required"])
        self.assertEqual(input_types["required"]["mada_seed_in"], ("MADA_SEED",))

    @patch('lc_comfyui_epistemic_nodes.l3_keymap_click_node.keymap_click_process')
    def test_execute_method(self, mock_keymap_click_process_sop):
        """Test the execute method of LcKeymapClickNode."""
        node = LcKeymapClickNode()

        # Create a mock MadaSeed object for input
        mock_input_mada_seed = MagicMock(spec=MadaSeed)
        mock_input_mada_seed.seed_id = "test_input_seed"

        # Create a mock MadaSeed object to be returned by the mocked SOP
        mock_output_mada_seed = MagicMock(spec=MadaSeed)
        mock_output_mada_seed.seed_id = "test_output_seed_l3"
        
        # Configure the mocked keymap_click_process SOP to return the mock output MadaSeed
        # Since asyncio.run is used inside the node, the mock for keymap_click_process
        # doesn't need to be async itself from the perspective of this test.
        mock_keymap_click_process_sop.return_value = mock_output_mada_seed

        # Call the execute method
        result_tuple = node.execute(mada_seed_in=mock_input_mada_seed)

        # Assert that the mocked keymap_click_process was called once with the input MadaSeed
        mock_keymap_click_process_sop.assert_called_once_with(mada_seed_input=mock_input_mada_seed)

        # Assert that the result is a tuple containing the output MadaSeed
        self.assertIsInstance(result_tuple, tuple)
        self.assertEqual(len(result_tuple), 1)
        self.assertIs(result_tuple[0], mock_output_mada_seed)
        self.assertEqual(result_tuple[0].seed_id, "test_output_seed_l3")

if __name__ == '__main__':
    unittest.main()
