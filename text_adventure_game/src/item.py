class Item:
    """
    Represents an item in the game that can be picked up, dropped, or used.
    """
    def __init__(self, name: str, description: str):
        """
        Initializes an Item.

        Args:
            name: The name of the item.
            description: A short description of the item.
        """
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """
        Returns the name of the item.
        """
        return self.name

    def use(self, player) -> None:
        """
        Defines the default action for using an item.
        This method is a placeholder and can be overridden by subclasses for specific item behaviors.

        Args:
            player: The player using the item. (Currently unused in base class)
        """
        print("Nothing interesting happens.")

# Example Usage (for testing purposes, typically removed or commented out in production)
if __name__ == '__main__':
    key = Item("Key", "A small rusty key.")
    print(key)
    print(key.description)
    key.use(None) # Player object would be passed here in a real scenario

    potion = Item("Potion", "A bubbling green liquid.")
    print(potion)
    print(potion.description)
    potion.use(None)
