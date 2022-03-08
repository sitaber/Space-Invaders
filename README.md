# Space Invaders
The classic arcade game [Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders) recreated with `Python` and `Pygame`. 

Information from [computerarcheology.com](https://www.computerarcheology.com/Arcade/SpaceInvaders/) was used to make the mechanics closely match the arcade version 

![Screen shot of game play](./images/gameplay2.png "Gameplay")


## How to Play
1. Press <kbd>SPACE</kbd> to start play
2. Use the keyboard to control the player

| Control      | Button              |
|--------------|---------------------|
| Move Left    | <kbd>A</kbd>        |
| Move right   | <kbd>D</kbd>        |
| Fire laser   | <kbd>spacebar</kbd> |

3. Try for the high score!

## Installation
### `Windows` 64 bit systems

- :arrow_down: [Download](https://github.com/sitaber/SpaceInvaders/releases) `SpaceInvaders-windows.zip` and unzip it.
- Run the executable named `spaceinvaders.exe` inside the extracted folder.

### `Linux/Debian` 64 bit based systems

#### Option 1: Download the zipped executable file

- :arrow_down: [Download](https://github.com/sitaber/SpaceInvaders/releases) `SpaceInvaders-linux.zip` and unzip
    - For example, if your download was saved to the `~/Downloads` folder:
    - Press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> to open the shell if you are on `GNU/Linux` based systems and type
    ```bash
    $ unzip ~/Downloads/SpaceInvaders-linux.zip -d ~/Desktop
    ```
    This will unzip the folder to your `Desktop`
- Navigate to the unzipped folder, change the file permissions for the executable and run it
    ```bash
    $ cd ~/Desktop/SpaceInvaders
    $ chmod +x spaceinvaders
    $ ./spaceinvaders
    ```
    
#### Option 2: Run as a script

You need to have `pygame` and _(obviously)_ `python` installed for this option. 

- Install `python`, `pygame`, and all the necessary dependencies. The following is the easiest method:
    ```bash
    $ sudo apt-get install python3-pygame
    ```
- Clone or Download
    - __Clone__
    ```bash
    $ git clone https://github.com/sitaber/SpaceInvaders.git
    $ cd SpaceInvaders/ 
    $ python3 spaceinvaders.py
    ```
    - :arrow_down: [Download](https://github.com/sitaber/SpaceInvaders/archive/refs/heads/main.zip) and unzip

    ```bash
    $ unzip ~/Downloads/SpaceInvaders-main.zip -d ~/Desktop
    $ cd ~/Desktop
    $ ## navigate to the unzipped folder
    $ cd SpaceInvaders-main
    $ python3 spaceinvaders.py
    ```

### `MacOS` 
I don't have an `macOS` system to build the executable or test installing `python` and `pygame`.

You can follow these [instructions](https://webcache.googleusercontent.com/search?q=cache:kyThG2mLWUsJ:https://www.pygame.org/wiki/MacCompile+&cd=1&hl=en&ct=clnk&gl=us&client=ubuntu) from the `pygame` website, or do an internet search for them.


# ENJOY!
