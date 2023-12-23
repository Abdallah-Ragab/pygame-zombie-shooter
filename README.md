![poster](https://github.com/Abdallah-Ragab/pygame-zombie-shooter/assets/93019811/bb208290-29c0-4f6a-a76f-2edbeae2bf65)

# Zombie Strike - A 2D Zombie Shooter Game made with Python and Pygame

## Project Documentation

This project is a Python-based game with various modules and components.
This project was a part of college assignment.

The project structure is as follows:


## Modules

### Animation
The Animation module, located in Animation/, contains the classes and functions necessary for handling animations in the game. The main classes in this module are:

- Animation: Handles individual animations.
- AnimationController: Manages multiple animations and transitions between them.
- Frame: Represents a single frame in an animation.
- SequenceAnimation: Handles sequences of animations.
- TransitionRule: Defines the rules for transitioning between animations.

### Character
The Character module, located in Character/, contains the classes and functions necessary for handling characters in the game. The main classes in this module are:

- Player: Represents the player character. This class handles player actions such as walking, shooting, and melee attacks, as well as player states such as idle and die. It also checks for collisions with enemies and handles player perks.
- Enemy: Represents enemy characters.
- Group: Handles groups of characters.
- EnemyManager: Manages multiple enemy characters.

### UI
The UI module, located in UI/, contains the classes and functions necessary for handling the user interface in the game. The main classes in this module are:

- Button: Represents a clickable button in the UI.
- Hud: Handles the heads-up display (HUD) in the game.
- UiElement: Represents a single element in the UI.

### Scene
The Scene module, located in Scene/, contains the classes and functions necessary for handling scenes in the game. The main classes in this module are:

- Level: Represents a level in the game.
- MenuScene: Represents the menu scene in the game.
- Scene: Represents a single scene in the game.

### Video
The Video module, located in Video/, contains the classes and functions necessary for handling video playback in the game. The main class in this module is Video, which handles video playback, seeking, pausing, and drawing.

## Other Files

- camera.py: Contains the Camera class, which handles the game camera.
- cursor.py: Contains the Cursor class, which handles the game cursor.
- director.py: Contains the Director class, which handles the game director.
- game.py: Contains the Game class, which handles the main game logic.
- music.py: Contains the Player class, which handles music and sound effects in the game.
- storage.py: Contains the JsonStorage class, which handles JSON storage for the game.
- requirements.txt: Lists the Python packages required for the project.
- save.json: Contains saved game data.
