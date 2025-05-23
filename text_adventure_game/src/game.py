import sys

try:
    from .player import Player
    from .room import Room
    from .item import Item
except ImportError:
    # Fallback for running game.py directly for testing,
    # assuming player.py, room.py, item.py are in the same directory or PYTHONPATH.
    from player import Player
    from room import Room
    from item import Item

def initialize_world() -> tuple[dict[str, Room], Room]:
    """
    Creates all rooms, items, and their connections.

    Returns:
        A tuple containing (game_rooms_dict, starting_room_object).
    """
    # Create Rooms
    library = Room("Dusty Library", "Shelves line the walls, covered in cobwebs and ancient tomes. A large, ornate desk sits in the center.")
    lab = Room("Alchemy Lab", "Bubbling concoctions and strange instruments fill the tables. A faint smell of sulfur hangs in the air.")
    hallway = Room("Grand Hallway", "A long, echoing hallway with high ceilings and portraits of stern-looking figures. Doors lead off in several directions.")
    chamber = Room("Hidden Chamber", "A small, dark chamber, seemingly untouched for centuries. The air is heavy with dust.")
    treasure_room = Room("Treasure Room", "Piles of gold coins, sparkling jewels, and ancient artifacts fill this magnificent room. It's an adventurer's dream!")

    # Create Items
    old_scroll = Item("Old Scroll", "An ancient, brittle scroll, covered in faded script.")
    glowing_potion = Item("Glowing Potion", "A potion that emits a soft, ethereal glow.")
    rusty_key = Item("Rusty Key", "A small, very rusty key.")
    treasure = Item("Treasure Chest", "A magnificent chest overflowing with gold and jewels!")

    # Add Items to Rooms
    library.add_item(old_scroll)
    lab.add_item(glowing_potion)
    chamber.add_item(rusty_key)
    treasure_room.add_item(treasure) # The main treasure

    # Define Exits
    # Library: north to "Alchemy Lab", east to "Grand Hallway"
    library.add_exit("north", lab.name) # Using room.name as the identifier
    library.add_exit("east", hallway.name)

    # Alchemy Lab: south to "Dusty Library"
    lab.add_exit("south", library.name)

    # Grand Hallway: west to "Dusty Library", south to "Hidden Chamber", east to "Treasure Room" (locked)
    hallway.add_exit("west", library.name)
    hallway.add_exit("south", chamber.name)
    hallway.add_exit("east", treasure_room.name) # This exit is initially locked

    # Hidden Chamber: north to "Grand Hallway"
    chamber.add_exit("north", hallway.name)

    # Treasure Room: west to "Grand Hallway"
    treasure_room.add_exit("west", hallway.name)

    # Store rooms in a dictionary
    game_rooms = {
        library.name: library,
        lab.name: lab,
        hallway.name: hallway,
        chamber.name: chamber,
        treasure_room.name: treasure_room
    }

    # Special handling for the locked door
    hallway.is_treasure_door_locked = True # Custom attribute on the Room object

    starting_room = library
    return game_rooms, starting_room

def parse_command(command_string: str) -> tuple[str | None, str | None]:
    """
    Parses a command string into a verb and an optional noun.

    Args:
        command_string: The raw command input from the user.

    Returns:
        A tuple (verb, noun). Verb can be None if input is empty.
        Noun can be None if no noun is provided.
    """
    command_string = command_string.lower().strip()
    if not command_string:
        return None, None

    parts = command_string.split(maxsplit=1)
    verb = parts[0]
    noun = parts[1] if len(parts) > 1 else None
    
    return verb, noun

# --- Game Loop and Main execution will be added below ---
# For now, let's test the initialization and parsing
if __name__ == '__main__':
    print("Initializing world...")
    rooms, start_node = initialize_world()
    print(f"Starting room: {start_node.name}")
    for name, room_obj in rooms.items():
        print(f"\n--- {name} ---")
        print(room_obj.describe())
        if hasattr(room_obj, 'is_treasure_door_locked'):
            print(f"Treasure door locked: {room_obj.is_treasure_door_locked}")

    print("\n--- Testing parse_command ---")
    commands_to_test = [
        "go north",
        "take scroll",
        "use key",
        "look",
        "inventory",
        "quit",
        "  drop  potion  ",
        "",
        "use rusty key"
    ]
    for cmd_str in commands_to_test:
        v, n = parse_command(cmd_str)
        print(f"Raw: '{cmd_str}' -> Verb: '{v}', Noun: '{n}'")

def game_loop(player: Player, game_rooms: dict[str, Room]):
    """
    Main loop for the game.
    """
    print("\nWelcome to the Text Adventure Game!")
    print("Type 'quit' to exit at any time.")
    print("Common commands: go [direction], take [item], use [item], inventory, look.")
    # treasure_room_unlocked is implicitly handled by game_rooms["Grand Hallway"].is_treasure_door_locked

    while True:
        print("\n" + "="*30) # Separator for clarity
        print(player.current_room.describe())

        # Win Condition Check
        if player.current_room.name == "Treasure Room":
            # The room description itself might be enough, or add a special message
            print("\nCongratulations, you've found the treasure!")
            print("The adventure is complete!")
            break

        raw_command = input("> ").strip()
        if not raw_command:
            continue

        verb, noun = parse_command(raw_command)

        if verb is None: # Should not happen if raw_command is not empty, but good check
            continue

        if verb in ["quit", "exit"]:
            print("Thanks for playing!")
            sys.exit()
        elif verb == "look":
            # Description is printed at the start of the loop.
            # Could add more detailed looking here if desired in future.
            print("(You look around the room again.)") # Optional feedback
        elif verb == "go":
            if noun:
                # Special handling for locked Treasure Room door
                if player.current_room.name == "Grand Hallway" and \
                   noun == "east" and \
                   hasattr(game_rooms["Grand Hallway"], 'is_treasure_door_locked') and \
                   game_rooms["Grand Hallway"].is_treasure_door_locked:
                    print("The grand door to the east is locked. It needs a key.")
                else:
                    player.move(noun, game_rooms)
            else:
                print("Go where? (e.g., 'go north')")
        elif verb == "take":
            if noun:
                player.take_item(noun)
            else:
                print("Take what?")
        elif verb == "drop":
            if noun:
                player.drop_item(noun)
            else:
                print("Drop what?")
        elif verb in ["inventory", "i"]:
            player.show_inventory()
        elif verb == "use":
            if noun:
                item_to_use_obj = player.inventory_get_item(noun) # Use the new method
                if item_to_use_obj:
                    # Specific item interactions
                    if item_to_use_obj.name == "Old Scroll":
                        print("The scroll reads: 'Where shadows play and secrets stay, a southern path will light the way.'")
                    elif item_to_use_obj.name == "Glowing Potion":
                        if player.current_room.name == "Grand Hallway":
                            print("The potion illuminates a faint crack on the south wall, revealing it as a passage! Perhaps you can 'go south' now.")
                        else:
                            item_to_use_obj.use(player) # Default "Nothing interesting happens."
                    elif item_to_use_obj.name == "Rusty Key":
                        if player.current_room.name == "Grand Hallway":
                            print("You try the rusty key on the grand door to the east...")
                            grand_hallway_room = game_rooms["Grand Hallway"]
                            if hasattr(grand_hallway_room, 'is_treasure_door_locked') and grand_hallway_room.is_treasure_door_locked:
                                grand_hallway_room.is_treasure_door_locked = False
                                print("It fits! The lock clicks open. The way to the Treasure Room is clear!")
                            else:
                                print("The door is already unlocked.")
                        else:
                            print("This key doesn't seem to fit any locks here.")
                            # item_to_use_obj.use(player) # Or default use message
                    else:
                        item_to_use_obj.use(player) # Default action for other items
                else:
                    print(f"You don't have '{noun}' in your inventory.") # Message from inventory_get_item might be sufficient or this is more direct.
            else:
                print("Use what?")
        else:
            print("I don't understand that command. Try 'go', 'take', 'use', 'drop', 'look', 'inventory', or 'quit'.")

if __name__ == '__main__':
    game_rooms_dict, starting_room_obj = initialize_world()
    game_player = Player(starting_room_obj)
    game_loop(game_player, game_rooms_dict)
