import unittest
from unittest.mock import patch
import sys
import os

# Adjust path to import from src
try:
    from text_adventure_game.src.player import Player
    from text_adventure_game.src.room import Room
    from text_adventure_game.src.item import Item
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from player import Player
    from room import Room
    from item import Item

class TestPlayer(unittest.TestCase):
    """
    Test cases for the Player class.
    """

    def setUp(self):
        """Set up common test fixtures."""
        self.room1 = Room("Room 1", "First room")
        self.room2 = Room("Room 2", "Second room")
        self.room1.add_exit("east", "Room 2") # Room 2's name as string ID
        self.room2.add_exit("west", "Room 1") # Room 1's name as string ID

        self.game_rooms = {"Room 1": self.room1, "Room 2": self.room2}
        
        self.player = Player(self.room1)
        
        self.sample_item_potion = Item("potion", "A healing potion")
        self.room1.add_item(self.sample_item_potion) # Add potion to Room 1

    def test_player_creation(self):
        """Test that a player is created in the correct room with an empty inventory."""
        self.assertIs(self.player.current_room, self.room1)
        self.assertEqual(self.player.inventory, [])

    def test_move_successful(self):
        """Test successful player movement."""
        moved = self.player.move("east", self.game_rooms)
        self.assertTrue(moved)
        self.assertIs(self.player.current_room, self.room2)

    @patch('builtins.print')
    def test_move_invalid_direction(self, mock_print):
        """Test moving in a direction where there is no exit."""
        moved = self.player.move("west", self.game_rooms) # No 'west' exit from room1
        self.assertFalse(moved)
        self.assertIs(self.player.current_room, self.room1)
        mock_print.assert_called_with("You can't go that way.")

    @patch('builtins.print')
    def test_move_invalid_room_in_map(self, mock_print):
        """Test moving to an exit that leads to a room not in the game_rooms map."""
        self.room1.add_exit("north", "Missing Room") # "Missing Room" is not in self.game_rooms
        moved = self.player.move("north", self.game_rooms)
        self.assertFalse(moved)
        self.assertIs(self.player.current_room, self.room1)
        mock_print.assert_any_call("Error: Room 'Missing Room' (linked from exit 'north') not found in game_rooms.")
        mock_print.assert_any_call("You can't go that way.")


    @patch('builtins.print')
    def test_take_item_successful(self, mock_print):
        """Test successfully taking an item."""
        taken = self.player.take_item("potion")
        self.assertTrue(taken)
        self.assertIn(self.sample_item_potion, self.player.inventory)
        self.assertNotIn(self.sample_item_potion, self.room1.items)
        mock_print.assert_called_with(f"You picked up the {self.sample_item_potion.name}.")

    @patch('builtins.print')
    def test_take_item_non_existent(self, mock_print):
        """Test taking an item that is not in the room."""
        taken = self.player.take_item("sword")
        self.assertFalse(taken)
        self.assertNotIn("sword", [item.name for item in self.player.inventory])
        mock_print.assert_called_with("'sword' not found here.")

    @patch('builtins.print')
    def test_drop_item_successful(self, mock_print):
        """Test successfully dropping an item."""
        self.player.take_item("potion") # First, player needs the item
        mock_print.reset_mock() # Reset mock after take_item's print

        dropped = self.player.drop_item("potion")
        self.assertTrue(dropped)
        self.assertNotIn(self.sample_item_potion, self.player.inventory)
        self.assertIn(self.sample_item_potion, self.room1.items)
        mock_print.assert_called_with(f"You dropped the {self.sample_item_potion.name}.")

    @patch('builtins.print')
    def test_drop_item_not_in_inventory(self, mock_print):
        """Test dropping an item that is not in the inventory."""
        dropped = self.player.drop_item("shield")
        self.assertFalse(dropped)
        mock_print.assert_called_with("You don't have 'shield'.")

    @patch('builtins.print')
    def test_show_inventory_empty(self, mock_print):
        """Test showing an empty inventory."""
        self.player.show_inventory()
        mock_print.assert_called_with("Your inventory is empty.")

    @patch('builtins.print')
    def test_show_inventory_with_item(self, mock_print):
        """Test showing an inventory with items."""
        self.player.take_item("potion")
        mock_print.reset_mock() # Reset after take_item's print

        self.player.show_inventory()
        mock_print.assert_called_with("Inventory: potion")

    def test_inventory_get_item(self):
        """Test retrieving an item from inventory using inventory_get_item."""
        self.player.take_item("potion")
        
        retrieved_item = self.player.inventory_get_item("potion")
        self.assertIs(retrieved_item, self.sample_item_potion)

        retrieved_item_case = self.player.inventory_get_item("POTION")
        self.assertIs(retrieved_item_case, self.sample_item_potion)

        non_existent_item = self.player.inventory_get_item("shield")
        self.assertIsNone(non_existent_item)
        # Ensure inventory is unchanged
        self.assertIn(self.sample_item_potion, self.player.inventory)


    @patch('builtins.print')
    def test_use_item_in_inventory(self, mock_print):
        """Test using an item that is in the inventory."""
        self.player.take_item("potion")
        mock_print.reset_mock() # Reset after take_item's print

        used_item_obj = self.player.use_item("potion")
        self.assertIs(used_item_obj, self.sample_item_potion)
        mock_print.assert_called_with(f"You attempt to use the {self.sample_item_potion.name}.")

    @patch('builtins.print')
    def test_use_item_not_in_inventory(self, mock_print):
        """Test using an item that is not in the inventory."""
        used_item_obj = self.player.use_item("shield")
        self.assertIsNone(used_item_obj)
        mock_print.assert_called_with("You don't have 'shield' in your inventory.")

if __name__ == '__main__':
    unittest.main()
