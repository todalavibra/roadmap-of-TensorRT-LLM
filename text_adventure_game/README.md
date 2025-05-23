# Text-Based Adventure Game

## Description
Embark on a mini-adventure in this text-based game. Explore a small, mysterious place, interact with objects, and solve a simple puzzle to find the hidden treasure.

## Setting
You find yourself in an old, dusty library, the starting point of your quest. The air is thick with the scent of aged paper and forgotten secrets. Can you uncover the mysteries it holds and find what lies beyond?

## Prerequisites
*   Python 3 (Python 3.7 or newer is recommended).

## How to Run
1.  **Navigate to the project directory:**
    If you have cloned the repository or downloaded the files, open your terminal or command prompt and change to the main game directory:
    ```bash
    cd text_adventure_game
    ```
2.  **Run the game:**
    Execute the main game script located in the `src` directory.
    ```bash
    python src/game.py
    ```
    (Depending on your system configuration, you might need to use `python3 src/game.py`.)

    Alternatively, you can run the game as a module from the directory containing `text_adventure_game` (if it's part of a larger project and your PYTHONPATH is set up accordingly, though for standalone execution the above is typical):
    ```bash
    # python -m text_adventure_game.src.game 
    # (This is less common for direct execution of this project structure)
    ```

## Basic Commands
Here are the commands you can use to interact with the game world:

*   `look`: See details about your current location, including a description of the room, any items present, and available exits.
*   `go [direction]`: Travel in a specified direction. Common directions are `north`, `south`, `east`, and `west`.
    *   Example: `go north`
*   `take [item name]`: Pick up an item from your current room and add it to your inventory.
    *   Example: `take old scroll`
*   `drop [item name]`: Remove an item from your inventory and leave it in the current room.
    *   Example: `drop old scroll`
*   `inventory` (or `i`): Check what items you are currently carrying.
*   `use [item name]`: Attempt to use an item from your inventory. Some items have specific uses in certain locations or can interact with other objects.
    *   Example: `use rusty key`
*   `quit` or `exit`: End your adventure and leave the game.

## Goal of the Game
Your goal is to find the hidden treasure by exploring the environment, collecting items, and solving the main puzzle that guards the path to your reward. Pay attention to item descriptions and room details for clues!

## Running Tests (For Developers/Contributors)
If you wish to run the unit tests for the game, navigate to the root project directory (`text_adventure_game`) and use the following command:
```bash
python -m unittest discover text_adventure_game/tests
```
This will automatically find and run all tests in the `tests` directory.
