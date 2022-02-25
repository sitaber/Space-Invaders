# Space Invaders
A [Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders) clone made with python and pygame utilizing information found at [computerarcheology.com](https://www.computerarcheology.com/Arcade/SpaceInvaders/) to make an accurate clone (as close as possible at least)

![Screen shot of game play](./images/gameplay.png "Gameplay")

## Requirements

Requires python 3.7 or higher, and pygame 2.x to run the python script.

Or download an [executable](#binary-files) packaged with [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) for your operating system

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
## Binary Files
Binary releases for 64 bit Ubuntu 16.0+ and Windows 7/10 - [LINK](https://github.com/sitaber/Space-Invaders/releases)

### For Ubuntu: 
1. download the zip file from the above link
2. unzip 
3. open a terminal and navigate to root directory of the unzipped folder. 
4. Make sure the file has permissions to run by entering
  ```bash
  sudo chmod +x spaceinvaders
  ```
  Or right-click on the file, select Properties > Permissions and check the box "Allow this file to run a program"

5.Than enter following command:
  ```bash
  ./spaceinvaders
  ```
### For Windows: 
1. download
2. unzip
3. navigate to the root folder 
4. double-click on the binary

# How to Play
Once you can run the game _(NOTE: the executable takes a bit to load)_ you will be presented with an intro screen.

- Press _SPACE_ to start play
- The _A_ keyboard key moves the player left
- The _D_ keyboard key moves the player right
- Use _SPACE_ bar to shoot
- Try for the high score!

# ENJOY!
