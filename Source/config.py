# This file is like a constant / public variable file

maxSpeed = 8.0                  # Mouvement constant
maxSpeedVerti = 14.0
HoriSpeedIncrement = 1.5
VertiSpeedIncrement = 1.0
JumpPower = 14.0
WallJumpPower = 10.0
MaxWallJump = 3
DownPower = 0.1

nb_key = 0  # current nb off key during a level

fps = 120  # nb of fps -> nb of update each seconds

OriginalScreenSize = [1250, 750]   # Do not change !
screenSize = [1250, 750]        # Do not change !

Quit = True         # If the game is quit or not

GameStart = False          # if the game have begin   => False -> Menu
                #[play,  info,  sound_button]
ButtonsClicked = [False, False, False]   # If a button of the menu is clicked
MouseClick = False         # if the mouse is click

inMenu = False   # inform that the user is in the menu
MenuBackPhase = 0    # the phase for the "gif" for the menu
soundEffect = True   # Turn ON/OFF effects (sfx)
soundMusic = True    # Turn ON/ODD music

Pause = False
TimePause = 0

record = None    # The current record
cheat = True     # True -> allow cheat
hasCheat = False  # If the player has cheat during a game