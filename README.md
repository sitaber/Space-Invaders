# Space Invaders
A [Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders) clone made with python and pygame utilizing information found at [computerarcheology.com](https://www.computerarcheology.com/Arcade/SpaceInvaders/) to make an accurate clone (as close as possible at least)

![Screen shot of game play](./images/gameplay.png "Gameplay")

## Requirements

Requires python 3.7 or higher, and pygame 2.x to run the python script.
Or download an executable packaged with pyinstaller for your operating system

First download/fork the repo, than install the required packages by using pip and the provided _requirements.txt_:
```bash
pip install -r requirements.txt
```

Or by creating a new conda environment with _environment.yml_:
```
conda env create -f environment.yml
```

Once your environment is setup, activate it (if using conda):
```bash
conda activate si
```
__NOTE__: the default conda environment name is *__si__*. You can change this in _environment.yml_

Navigate to the top level directory of the repository via the command line and run the script with the following command:
```
python spaceinvaders.py
```
## Executable

An executable file is available for the following 64 bit operating systems: 
- Ubuntu 16.0 or higher  [LINK](https://drive.google.com/file/d/12zjT6GZFb96UReCOf2yHxugJ0xJauC9z/view?usp=sharing)
- Windows 7/10 [LINK](https://drive.google.com/file/d/1k90gq6PHvEMPehrr0eNGvnjqvOXS7xSk/view?usp=sharing)

# How to Play

Once you can run the game _(NOTE: the executable takes a bit to load)_ you will be presented with an intro screen.

- Press _SPACE_ to start play
- The _A_ keyboard key moves the player left
- The _D_ keyboard key moves the player right
- Use _SPACE_ bar to shoot
- Try for the high score!

# CODE

The code is poorly structured and non-modular. It a bunch of classes and functions called in a while loop.
Future attempts may be made to improve the code. Feel free to fork and make your own modifications!

ENJOY!
