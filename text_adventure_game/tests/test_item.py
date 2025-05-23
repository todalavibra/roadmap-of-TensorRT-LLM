import unittest
from unittest.mock import patch
import sys
import os

# Adjust path to import from src
try:
    from text_adventure_game.src.item import Item
except ImportError:
    # This allows running tests directly from the 'tests' directory or project root
    # by adding the 'src' directory to the Python path.
    # Assumes the test file is in 'text_adventure_game/tests/' and 'src' is a sibling of 'tests'.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from item import Item


class TestItem(unittest.TestCase):
    """
    Test cases for the Item class.
    """

    def test_item_creation(self):
        """Test that an item is created with the correct name and description."""
        item_name = "Magic Wand"
        item_description = "A wand buzzing with magical energy."
        item = Item(item_name, item_description)
        self.assertEqual(item.name, item_name)
        self.assertEqual(item.description, item_description)

    def test_item_str(self):
        """Test that str(item) returns the item's name."""
        item_name = "Mystic Amulet"
        item_description = "An amulet that hums faintly."
        item = Item(item_name, item_description)
        self.assertEqual(str(item), item_name)

    @patch('builtins.print')
    def test_item_use_placeholder(self, mock_print):
        """Test the placeholder use() method prints the correct message."""
        item = Item("Generic Item", "Just an item.")
        item.use(None)  # Player argument is not used by the placeholder
        mock_print.assert_called_once_with("Nothing interesting happens.")

if __name__ == '__main__':
    unittest.main()
