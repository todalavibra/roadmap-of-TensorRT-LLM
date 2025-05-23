import unittest
import sys
import os

# Adjust path to import from src
try:
    from text_adventure_game.src.game import parse_command, initialize_world
    from text_adventure_game.src.room import Room
    from text_adventure_game.src.item import Item # Though not directly used, good for context
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from game import parse_command, initialize_world
    from room import Room
    from item import Item

class TestGame(unittest.TestCase):
    """
    Test cases for game utility functions like parse_command and initialize_world.
    """

    def test_parse_command(self):
        """Test the parse_command function."""
        self.assertEqual(parse_command("go north"), ("go", "north"))
        self.assertEqual(parse_command("look"), ("look", None))
        self.assertEqual(parse_command("LOOK"), ("look", None)) # Test case insensitivity (lower() in func)
        self.assertEqual(parse_command("  take  old scroll  "), ("take", "old scroll"))
        self.assertEqual(parse_command("use rusty key"), ("use", "rusty key"))
        self.assertEqual(parse_command(""), (None, None))
        self.assertEqual(parse_command(" "), (None, None)) # Test with only spaces
        self.assertEqual(parse_command("   drop   "), ("drop", None)) # Verb with spaces around it

    def test_initialize_world(self):
        """Test the initialize_world function."""
        game_rooms, start_room = initialize_world()

        # Check types
        self.assertIsInstance(game_rooms, dict)
        self.assertIsInstance(start_room, Room)

        # Check specific rooms exist
        self.assertIn("Dusty Library", game_rooms)
        self.assertIn("Alchemy Lab", game_rooms)
        self.assertIn("Grand Hallway", game_rooms)
        self.assertIn("Hidden Chamber", game_rooms)
        self.assertIn("Treasure Room", game_rooms)

        # Check starting room
        self.assertEqual(start_room.name, "Dusty Library")
        self.assertIs(game_rooms["Dusty Library"], start_room)

        # Check items in rooms
        library = game_rooms["Dusty Library"]
        self.assertIsNotNone(library.get_item("Old Scroll"))
        self.assertIsNone(library.get_item("Glowing Potion")) # Should not be here

        lab = game_rooms["Alchemy Lab"]
        self.assertIsNotNone(lab.get_item("Glowing Potion"))

        chamber = game_rooms["Hidden Chamber"]
        self.assertIsNotNone(chamber.get_item("Rusty Key"))
        
        treasure_room = game_rooms["Treasure Room"]
        self.assertIsNotNone(treasure_room.get_item("Treasure Chest"))


        # Check exits (spot checks)
        self.assertEqual(library.exits.get("north"), "Alchemy Lab")
        self.assertEqual(library.exits.get("east"), "Grand Hallway")
        self.assertIsNone(library.exits.get("south"))

        grand_hallway = game_rooms["Grand Hallway"]
        self.assertEqual(grand_hallway.exits.get("east"), "Treasure Room")
        
        # Check locked door state
        self.assertTrue(hasattr(grand_hallway, 'is_treasure_door_locked'))
        self.assertTrue(grand_hallway.is_treasure_door_locked)

if __name__ == '__main__':
    unittest.main()
