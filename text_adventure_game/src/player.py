try:
    from .room import Room
    from .item import Item
except ImportError:
    # Fallback for standalone testing or if the module structure isn't recognized
    # (e.g., when running the file directly without proper PYTHONPATH)
    from room import Room
    from item import Item

class Player:
    """
    Represents the player in the game.
    """
    def __init__(self, starting_room: Room):
        """
        Initializes a Player.

        Args:
            starting_room: The Room object where the player starts.
        """
        self.current_room = starting_room
        self.inventory = []  # List of Item objects

    def move(self, direction: str, game_rooms: dict[str, Room]) -> bool:
        """
        Moves the player to a new room based on the direction.

        Args:
            direction: The direction to move (e.g., 'north', 'south').
            game_rooms: A dictionary mapping room names/IDs to Room objects.

        Returns:
            True if the player successfully moved, False otherwise.
        """
        direction = direction.lower()
        next_room_name = self.current_room.exits.get(direction)

        if next_room_name:
            if next_room_name in game_rooms:
                self.current_room = game_rooms[next_room_name]
                return True
            else:
                print(f"Error: Room '{next_room_name}' (linked from exit '{direction}') not found in game_rooms.")
                print("You can't go that way.") # Or a more specific error for the player
                return False
        else:
            print("You can't go that way.")
            return False

    def take_item(self, item_name: str) -> bool:
        """
        Takes an item from the current room and adds it to the player's inventory.

        Args:
            item_name: The name of the item to take.

        Returns:
            True if the item was successfully taken, False otherwise.
        """
        item = self.current_room.remove_item(item_name)
        if item:
            self.inventory.append(item)
            print(f"You picked up the {item.name}.")
            return True
        else:
            # Check if the item is even in the room to give a more specific message
            # This is implicitly handled by remove_item returning None if not found by name
            print(f"'{item_name}' not found here.")
            return False

    def drop_item(self, item_name: str) -> bool:
        """
        Drops an item from the player's inventory into the current room.

        Args:
            item_name: The name of the item to drop.

        Returns:
            True if the item was successfully dropped, False otherwise.
        """
        item_to_drop = None
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item_to_drop = item
                break
        
        if item_to_drop:
            self.inventory.remove(item_to_drop)
            self.current_room.add_item(item_to_drop)
            print(f"You dropped the {item_to_drop.name}.")
            return True
        else:
            print(f"You don't have '{item_name}'.")
            return False

    def show_inventory(self) -> None:
        """
        Prints the player's current inventory.
        """
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            inventory_item_names = [item.name for item in self.inventory]
            print("Inventory: " + ", ".join(inventory_item_names))

    def use_item(self, item_name: str) -> Item | None:
        """
        Attempts to use an item from the player's inventory.
        The actual effect of using the item is handled by the game loop or the item itself.

        Args:
            item_name: The name of the item to use.

        Returns:
            The Item object if found in inventory, otherwise None.
        """
        item_to_use = None
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item_to_use = item
                break
        
        if item_to_use:
            print(f"You attempt to use the {item_to_use.name}.")
            # The item's own .use() method could be called here or in the game loop
            # e.g., item_to_use.use(self) # Pass player object to item's use method
            return item_to_use
        else:
            print(f"You don't have '{item_name}' in your inventory.")
            return None

    def inventory_get_item(self, item_name: str) -> Item | None:
        """
        Retrieves an item from the player's inventory by its name without using it.

        Args:
            item_name: The name of the item to retrieve.

        Returns:
            The Item object if found in inventory, otherwise None.
        """
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None

# Example Usage (for testing purposes)
if __name__ == '__main__':
    # Setup a mock environment
    kitchen = Room("Kitchen", "A messy kitchen.")
    living_room = Room("Living Room", "A cozy living room.")
    key = Item("Key", "A small silver key.")
    apple = Item("Apple", "A juicy red apple.")

    kitchen.add_item(key)
    kitchen.add_item(apple)
    kitchen.add_exit("north", "Living Room") # Room name as string ID
    living_room.add_exit("south", "Kitchen")

    game_rooms_dict = {
        "Kitchen": kitchen,
        "Living Room": living_room
    }

    player = Player(kitchen)
    
    # Test initial state
    print(player.current_room.describe())
    player.show_inventory() # Expected: Your inventory is empty.

    # Test take_item
    print("\n--- Testing take_item ---")
    player.take_item("Key") # Expected: You picked up the Key.
    player.show_inventory() # Expected: Inventory: Key
    print(player.current_room.describe()) # Key should be gone from room
    player.take_item("NonExistent") # Expected: 'NonExistent' not found here.
    player.take_item("Apple")
    player.show_inventory() # Expected: Inventory: Key, Apple

    # Test move
    print("\n--- Testing move ---")
    player.move("north", game_rooms_dict) # Expected: (No output, but room changes)
    print(player.current_room.describe()) # Expected: Living Room description
    player.move("east", game_rooms_dict) # Expected: You can't go that way.
    player.move("south", game_rooms_dict) # Expected: (No output, but room changes)
    print(player.current_room.describe()) # Expected: Kitchen description (apple should still be there if not taken)

    # Test drop_item
    print("\n--- Testing drop_item ---")
    player.drop_item("Key") # Expected: You dropped the Key.
    player.show_inventory() # Expected: Inventory: Apple
    print(player.current_room.describe()) # Key should be in the kitchen
    player.drop_item("NonExistent") # Expected: You don't have 'NonExistent'.

    # Test use_item
    print("\n--- Testing use_item ---")
    used_item = player.use_item("Apple") # Expected: You attempt to use the Apple.
    if used_item:
        used_item.use(player) # Expected: Nothing interesting happens. (from Item base class)
    player.use_item("Key") # Expected: You don't have 'Key' in your inventory.
    
    player.take_item("Key")
    used_key = player.use_item("Key")
    if used_key:
        used_key.use(player) # Expected: Nothing interesting happens.

    print("\n--- Testing inventory_get_item ---")
    player.show_inventory() # Expected: Inventory: Apple, Key
    retrieved_apple = player.inventory_get_item("Apple")
    print(f"Retrieved: {retrieved_apple.name}" if retrieved_apple else "Not found") # Expected: Apple
    retrieved_non_existent = player.inventory_get_item("Spoon")
    print(f"Retrieved: {retrieved_non_existent.name}" if retrieved_non_existent else "Not found") # Expected: Not found
    player.show_inventory() # Ensure inventory is unchanged by get: Inventory: Apple, Key
    
    print("\n--- Final State ---")
    player.show_inventory()
    print(player.current_room.describe())
