try:
    from .item import Item
except ImportError:
    # This allows the file to be run standalone for testing,
    # assuming item.py is in the same directory or PYTHONPATH is configured.
    from item import Item

class Room:
    """
    Represents a location in the game world.
    """
    def __init__(self, name: str, description: str):
        """
        Initializes a Room.

        Args:
            name: The name of the room.
            description: A textual description of the room.
        """
        self.name = name
        self.description = description
        self.exits = {}  # e.g., {'north': 'Living Room', 'south': 'Garden'}
        self.items = []  # List of Item objects in the room

    def add_item(self, item: Item) -> None:
        """
        Adds an item to the room.

        Args:
            item: The Item object to add.
        """
        self.items.append(item)

    def remove_item(self, item_name: str) -> Item | None:
        """
        Removes and returns an item from the room by its name.

        Args:
            item_name: The name of the item to remove.

        Returns:
            The Item object if found and removed, otherwise None.
        """
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                return item
        return None

    def get_item(self, item_name: str) -> Item | None:
        """
        Returns an item from the room by its name without removing it.

        Args:
            item_name: The name of the item to get.

        Returns:
            The Item object if found, otherwise None.
        """
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def add_exit(self, direction: str, room_name: str) -> None:
        """
        Adds an exit to the room.

        Args:
            direction: The direction of the exit (e.g., 'north', 'south', 'east', 'west').
            room_name: The name or ID of the room that this exit leads to.
        """
        self.exits[direction.lower()] = room_name

    def describe(self) -> str:
        """
        Generates a multi-line string description of the room.

        Returns:
            A string detailing the room's name, description, items, and exits.
        """
        description_parts = [
            self.name,
            self.description,
        ]

        if self.items:
            item_names = [item.name for item in self.items]
            description_parts.append(f"Items here: {', '.join(item_names)}")
        else:
            description_parts.append("No items here.")

        if self.exits:
            exit_directions = list(self.exits.keys())
            description_parts.append(f"Exits: {', '.join(exit_directions)}")
        else:
            description_parts.append("No obvious exits.")

        return "\n".join(description_parts)

# Example Usage (for testing purposes)
if __name__ == '__main__':
    kitchen = Room("Kitchen", "A small, cluttered kitchen.")
    key = Item("Rusty Key", "An old key, covered in rust.")
    apple = Item("Red Apple", "A shiny red apple.")

    kitchen.add_item(key)
    kitchen.add_item(apple)
    kitchen.add_exit("north", "Living Room")
    kitchen.add_exit("west", "Pantry")

    print(kitchen.describe())
    # Expected:
    # Kitchen
    # A small, cluttered kitchen.
    # Items here: Rusty Key, Red Apple
    # Exits: north, west

    print("\nTaking apple...")
    taken_item = kitchen.remove_item("Red Apple")
    if taken_item:
        print(f"Removed: {taken_item.name}")
    print(kitchen.describe())
    # Expected:
    # Kitchen
    # A small, cluttered kitchen.
    # Items here: Rusty Key
    # Exits: north, west

    print("\nLooking for apple...")
    found_item = kitchen.get_item("Red Apple")
    print(f"Found: {found_item.name}" if found_item else "Found: None")
    # Expected: Found: None

    print("\nLooking for key...")
    found_item = kitchen.get_item("Rusty Key")
    print(f"Found: {found_item.name}" if found_item else "Found: None")
    # Expected: Found: Rusty Key
    print(kitchen.describe()) # Ensure get_item didn't remove it
    # Expected:
    # Kitchen
    # A small, cluttered kitchen.
    # Items here: Rusty Key
    # Exits: north, west
