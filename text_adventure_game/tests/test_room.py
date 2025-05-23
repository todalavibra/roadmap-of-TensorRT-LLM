import unittest
import sys
import os

# Adjust path to import from src
try:
    from text_adventure_game.src.room import Room
    from text_adventure_game.src.item import Item
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from room import Room
    from item import Item

class TestRoom(unittest.TestCase):
    """
    Test cases for the Room class.
    """

    def setUp(self):
        """Set up common test fixtures."""
        self.sample_item = Item("widget", "A simple widget")
        self.room = Room("Test Chamber", "A plain room for testing.")

    def test_room_creation(self):
        """Test that a room is created with the correct name, description, and empty exits/items."""
        self.assertEqual(self.room.name, "Test Chamber")
        self.assertEqual(self.room.description, "A plain room for testing.")
        self.assertEqual(self.room.exits, {})
        self.assertEqual(self.room.items, [])

    def test_add_get_remove_item(self):
        """Test adding, getting, and removing items from a room."""
        # Add item
        self.room.add_item(self.sample_item)
        self.assertIn(self.sample_item, self.room.items)
        self.assertEqual(len(self.room.items), 1)

        # Get item (normal case)
        retrieved_item = self.room.get_item("widget")
        self.assertIs(retrieved_item, self.sample_item)
        self.assertIn(self.sample_item, self.room.items) # Ensure get_item didn't remove it

        # Get item (lowercase)
        retrieved_item_lower = self.room.get_item("widget")
        self.assertIs(retrieved_item_lower, self.sample_item)

        # Get item (uppercase)
        retrieved_item_upper = self.room.get_item("WIDGET")
        self.assertIs(retrieved_item_upper, self.sample_item)
        
        # Get non-existent item
        non_existent_item = self.room.get_item("gadget")
        self.assertIsNone(non_existent_item)

        # Remove item (normal case)
        removed_item = self.room.remove_item("widget")
        self.assertIs(removed_item, self.sample_item)
        self.assertNotIn(self.sample_item, self.room.items)
        self.assertEqual(len(self.room.items), 0)

        # Re-add item for further tests
        self.room.add_item(self.sample_item)

        # Remove item (lowercase)
        removed_item_lower = self.room.remove_item("widget")
        self.assertIs(removed_item_lower, self.sample_item)
        self.assertNotIn(self.sample_item, self.room.items)

        # Re-add item
        self.room.add_item(self.sample_item)
        
        # Remove item (uppercase)
        removed_item_upper = self.room.remove_item("WIDGET")
        self.assertIs(removed_item_upper, self.sample_item)
        self.assertNotIn(self.sample_item, self.room.items)

        # Remove non-existent item
        non_existent_removed_item = self.room.remove_item("gadget")
        self.assertIsNone(non_existent_removed_item)

    def test_add_exit(self):
        """Test adding an exit to a room."""
        self.room.add_exit("north", "Corridor")
        self.assertIn("north", self.room.exits)
        self.assertEqual(self.room.exits["north"], "Corridor")

        self.room.add_exit("WEST", "Another Room") # Test case normalization
        self.assertIn("west", self.room.exits)
        self.assertEqual(self.room.exits["west"], "Another Room")


    def test_describe(self):
        """Test the describe() method for various room configurations."""
        # Room with no items, no exits
        room_empty = Room("Empty Void", "An endless expanse of nothing.")
        desc_empty = room_empty.describe()
        self.assertIn("Empty Void", desc_empty)
        self.assertIn("An endless expanse of nothing.", desc_empty)
        self.assertIn("No items here.", desc_empty)
        self.assertIn("No obvious exits.", desc_empty)

        # Room with items, no exits
        room_items_only = Room("Cluttered Closet", "Full of old clothes and boxes.")
        item1 = Item("Dusty Hat", "A hat covered in dust.")
        item2 = Item("Moth-eaten Scarf", "A scarf with many holes.")
        room_items_only.add_item(item1)
        room_items_only.add_item(item2)
        desc_items_only = room_items_only.describe()
        self.assertIn("Cluttered Closet", desc_items_only)
        self.assertIn("Full of old clothes and boxes.", desc_items_only)
        self.assertIn("Items here: Dusty Hat, Moth-eaten Scarf", desc_items_only)
        self.assertNotIn("Moth-eaten Scarf, Dusty Hat", desc_items_only) # Check order if specific, though current implementation doesn't guarantee
        self.assertIn("Dusty Hat", desc_items_only)
        self.assertIn("Moth-eaten Scarf", desc_items_only)
        self.assertIn("No obvious exits.", desc_items_only)

        # Room with no items, with exits
        room_exits_only = Room("Junction", "A meeting point of several paths.")
        room_exits_only.add_exit("north", "PathA")
        room_exits_only.add_exit("south", "PathB")
        desc_exits_only = room_exits_only.describe()
        self.assertIn("Junction", desc_exits_only)
        self.assertIn("A meeting point of several paths.", desc_exits_only)
        self.assertIn("No items here.", desc_exits_only)
        self.assertIn("Exits: north, south", desc_exits_only) # Order might vary, check individual presence
        self.assertIn("north", desc_exits_only)
        self.assertIn("south", desc_exits_only)


        # Room with items and exits
        self.room.add_item(self.sample_item)
        self.room.add_exit("east", "Main Hall")
        desc_full = self.room.describe()
        self.assertIn("Test Chamber", desc_full)
        self.assertIn("A plain room for testing.", desc_full)
        self.assertIn(f"Items here: {self.sample_item.name}", desc_full)
        self.assertIn("Exits: east", desc_full) # If only one exit
        self.assertIn("east", desc_full)

if __name__ == '__main__':
    unittest.main()
