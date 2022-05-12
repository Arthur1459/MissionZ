# 30/04/22 - Version 1.0 - MissionZ
#
# Main program of MissionZ made by Arthur1459 (ytb : ZEDIEU2LAMER)
# This program is a platformer game which use pygame as main library.
# To win the game tou need to complete all level by collect the keys and reach the doors.
#

# ---- Imports ----
import pygame
import Initialization
import config as cf
from time import time
# -----------------

### --------------------------- Game Main Loop --------------------------- ###
def LaunchGame():
    # - Initialization -
    screen, clock, sprites, lvls, lvlsStart, lvlsEnd, musics, lvlsDisplayed, keys_position, keys, endVisuals, = Initialization.Init() # Initialization

    hasBegin = False # if the current level is start or not
    print("-- Programme started ! --")
    lvl = 1  # initialize the current lvl
    total_nb_key = len(keys)  # initialize the nb of key in each level
    t0 = time()  # get the time at the beginning of the game
    cf.screenSize = [screen.get_width(), screen.get_height()]  # set the size of the screen in the public variable files

    running = True  # the bool which allow the pygame to update

    # - Main loop -
    while running: # loop of the game
        clock.tick(cf.fps) # nb of fps  (clock initialize in Init.Init())
        for event in pygame.event.get():  # get all event of pygame
            if event.type == pygame.QUIT:  # if the cross is click -> close the game and open the menu
                running = False # stop the loop
                pygame.mixer.music.fadeout(1) # stop the music
                pygame.QUIT # quit pygame
                GoToMenu()  # Go to the menu
            if event.type == pygame.MOUSEBUTTONUP:    # for developer to get the coord of a mouse click on the screen
                print("-----  MOUSE : ",pygame.mouse.get_pos())   # <- take of the fisrt '#' to use this feature
                pass

        # - level management -
        if hasBegin == False :  # if level isn't start
            startLevel(lvl, lvlsStart, sprites, lvls[lvl-1], keys, keys_position)  # start the level
            PlayMusic(musics[lvl - 1]) # Play the music of the current level
            hasBegin = True  # inform that the level has begin
        else: # if the level has begin
            if isLevelEnded(lvl, lvlsEnd, sprites, total_nb_key) and cf.nb_key >= total_nb_key: # if the player have reach the door with the keys needed
                if lvl == len(lvlsEnd): # if the level was the last
                    print("You have done all levels !! GG !")
                    if round(time()-t0) < cf.record:
                        cf.record = round(time()-t0)
                        t0 = time()
                        PlayEffect('Sounds/NewRecord.wav')
                        if cf.hasCheat is False:
                            file = open('record.txt', 'w')
                            file.truncate()
                            file.write(str(cf.record))
                            file.close()
                    else:
                        PlayEffect('Sounds/FinishGame.wav')
                        t0 = time()
                    lvl = 1  # return to lvl 1
                    PlayMusic(musics[lvl - 1])
                    startLevel(lvl, lvlsStart, sprites, lvls[lvl-1], keys, keys_position)  # start le the level 1
                else: # if the player haven't done all level
                    PlayEffect('Sounds/NewLevel.wav')
                    hasBegin = False  # inform that the level haven'nt begin
                    lvl += 1  # go to the next level

        inputs = getInputs()  # get the keyboard inputs
        # inputs = [right_arrow/D, left_arrow/Q, up_arrow/Z, down_arrow/S, space, k, f]

        # - main function -
        if cf.Pause is False:

            Calculation(sprites, lvl, lvlsStart, lvls[lvl-1], keys, keys_position)  # make the calculation of all things (moovement, checks..)
            DisplayUpdate(screen, lvlsDisplayed[lvl-1], sprites, lvlsEnd[lvl-1], t0, keys, endVisuals, lvl)  # Update the screen with the updated coord

            # - Special Inputs -
            if inputs[4] == 1:  # if space is pressed : reset the current level
                print("Level Reset.")
                for n in keys:  # for all keys
                    n.Restore()   # restore them (show them)
                    n.UpdateState() # update them
                    cf.nb_key = 0   # reset the nb of keys collected by the player
                PlayEffect('Sounds/ResetLevel.wav') # play sound_button effect
                startLevel(lvl, lvlsStart, sprites, lvls[lvl - 1], keys, keys_position)  # restart the level
                pygame.time.delay(100) # wait 100 milliseconds (0.1s)

            if inputs[5] == 1 and cf.cheat is True: # if k is pressed : Cheat Source for developers to complete the current level instantly
                cf.hasCheat = True
                PlayEffect('Sounds/NewLevel.wav')
                for n in keys:    # for all keys
                    n.Restore() # restore them (show them)
                    n.UpdateState() # update them
                    cf.nb_key = 0 # reset the nb of keys collected by the player
                if lvl == len(lvlsEnd):  # if the level is the last
                    print("You have done all levels !! GG !")
                    if round(time() - t0) < cf.record and cf.hasCheat is False:
                        cf.record = round(time() - t0)
                        t0 = time()
                        PlayEffect('Sounds/NewRecord.wav')
                        file = open('record.txt', 'w')
                        file.truncate()
                        print(str(cf.record))
                        file.write(str(cf.record))
                        file.close()
                    else:
                        PlayEffect('Sounds/FinishGame.wav')
                        t0 = time()
                    lvl = 1
                    cf.hasCheat = False
                else:
                    lvl += 1   # go to the next level
                PlayMusic(musics[lvl - 1])  # play the music of the new level
                startLevel(lvl, lvlsStart, sprites, lvls[lvl - 1], keys, keys_position)  # start this new level
                pygame.time.delay(100) # wait 100 milliseconds (0.1s)

        else: # The game is Paused
            screen.blit(pygame.transform.scale(pygame.image.load("Visuals/Pause.png"), (512, 448)), (screen.get_width()/2-(512/2),screen.get_height()/2-(448/2)))
            pygame.display.update()

        if inputs[6] == 1:  # if F is pressed : go to the menu, reset the game
            pygame.mixer.music.fadeout(1)  # stop current music
            return GoToMenu()  # start the menu

        if inputs[7] == 1:  # if G is pressed : turn on/off the music
            if cf.soundMusic:
                pygame.mixer.music.set_volume(0.0)
                cf.soundMusic = False
            else:
                pygame.mixer.music.set_volume(0.5)
                cf.soundMusic = True
            pygame.time.delay(100)

        if inputs[8] == 1:  # if H is pressed : turn on/off the sounds Effects
            if cf.soundEffect:
                PlayEffect('Sounds/SoundEffectOFF.wav')
                cf.soundEffect = False
            else:
                cf.soundEffect = True
                PlayEffect('Sounds/SoundEffectON.wav')
            pygame.time.delay(100)

        if inputs[9] == 1:  # if P is pressed : turn Pause ON / OFF
            if cf.Pause:
                cf.Pause = False
                t0 += round(time() - cf.TimePause)
            else:
                cf.Pause = True
                cf.TimePause = time()
            pygame.time.delay(100)

### -------------------------------------------------------------------------------------------------------- ###

def DisplayUpdate(screen, back_level, sprites, lvlsEnd, t0, keys, endVisuals, lvl): # Update the displayed window
    screen.blit(pygame.transform.scale(back_level, (screen.get_width(), screen.get_height())), (0, 0))  # add the background depending of the level
    screen.blit(pygame.transform.scale(endVisuals[cf.nb_key], ((lvlsEnd[1][0]-lvlsEnd[0][0]), (lvlsEnd[1][1]-lvlsEnd[0][1]))), (lvlsEnd[0][0], lvlsEnd[0][1])) # add the door depending of nb of keys collected

    Text(('time : ' + str(round(time()-t0)) + ' s'), [screen.get_width()-176, 4], 24, screen)  # add the timer
    Text(('level : ' + str(lvl)), [screen.get_width()-84, screen.get_height() - 24], 14, screen)
    Text(('Pause : P'), [screen.get_width() - 84, screen.get_height() - 40], 14, screen)
    if cf.hasCheat is False:
        Text(('record : ' + str(cf.record) + 's'), [16, 4], 24, screen)  # add the time record
    else:
        Text(('You Cheated.'), [16, 4], 24, screen)  # add the time record
    if cf.soundMusic is True:
        Text('Music : ON', [10, screen.get_height()-24], 12, screen)
    else:
        Text('Music : OFF', [10, screen.get_height() - 24], 12, screen)
    if cf.soundEffect is True:
        Text('/  SFX : ON', [86, screen.get_height() - 24], 12, screen)
    else:
        Text('/  SFX : OFF', [86, screen.get_height() - 24], 12, screen)

    for i in keys:  # for all keys
        if i.state == 0: # if the key isn't already taken
            screen.blit(i.visual, i.coord)  # add the key
    for i in sprites: # for all players (1 actually)
        screen.blit(i.visual, (i.coord)) # add the player with his appearance
    pygame.display.update()  # Update the window with all modification above

def Calculation(sprites, lvl, lvlsStart, backLevel, keys, keys_position):  # make the calculation of quite everything
    for i in sprites: # for all players
        for u in i.detectors: # for all detectors of all players
            if u.getState() == 2: # if the detectors is touching a killing surface
                PlayEffect('Sounds/PlayerDeath.wav')  # play sound_button effect
                startLevel(lvl, lvlsStart, sprites, backLevel, keys, keys_position) # restart level
                for n in keys:  # for all key
                    n.Restore() # restore them
                    n.UpdateState() # update them
                    cf.nb_key = 0 # reset the nb of keys taken by the player
        i.UpdateSpeed(getInputs()) # Update the current player speed
        i.UpdateCoord() # Update the current player position depending of his speed
        for u in keys: # for all keys
            if u.coord[0] < i.coord[0] + 4 < u.coord[0] + 32 and u.coord[1] < i.coord[1] + 8 < u.coord[1] + 32 and u.getState() == 0: # if player touch the key
                PlayEffect('Sounds/key.wav') # play sound_button effect
                u.TakeKey() # collect the key (hide the key)
                u.UpdateState() # update the state of the key (inform it is taken)
                cf.nb_key += 1 # add 1 to the nb of key taken by the player

def getInputs(): # Get the keyboard inputs
    Total_inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # initialize a list to save the current inputs
    inputs = pygame.key.get_pressed() # get all keyboard inputs
    if inputs[pygame.K_RIGHT] or inputs[pygame.K_d] or inputs[pygame.K_a]: # if right_arrow or D or A is pressed
        Total_inputs[0] = 1 # register it in the list
    if inputs[pygame.K_LEFT] or inputs[pygame.K_q]: # if left_arrow or Q pressed
        Total_inputs[1] = 1 # register it in the list
    if inputs[pygame.K_UP] or inputs[pygame.K_z] or inputs[pygame.K_w]: # if up_arrow or Z or W is pressed
        Total_inputs[2] = 1 # register it in the list
    if inputs[pygame.K_DOWN] or inputs[pygame.K_s]: # if down_arrow or S pressed
        Total_inputs[3] = 1 # register it in the list
    if inputs[pygame.K_SPACE]: # if space pressed
        Total_inputs[4] = 1 # register it in the list
    if inputs[pygame.K_k]: # if K pressed
        Total_inputs[5] = 1 # register it in the list
    if inputs[pygame.K_f]: # switch the value, if F pressed (for the menu)
        Total_inputs[6] = 1 # register it in the list
    if inputs[pygame.K_g]: # switch the value, if G pressed (for the sound_button)
        Total_inputs[7] = 1 # register it in the list
    if inputs[pygame.K_h]: # switch the value, if H pressed (for the sound_button)
        Total_inputs[8] = 1 # register it in the list
    if inputs[pygame.K_p]: # switch the value, if H pressed (for the sound_button)
        Total_inputs[9] = 1 # register it in the list
    return Total_inputs

def startLevel(lvl, lvlsStart, sprites, backLevel, keys, keys_position):  # Initialize and Start a level
    print("Level started :", lvl)
    for i in sprites: # teleport the player to the beginning of the level
        i.coord[0] = lvlsStart[lvl-1][0] # x
        i.coord[1] = lvlsStart[lvl-1][1] # y
        i.speed = [0, 0] # reset the player's speed
        for u in i.detectors: # Upadte the structure level for the detectors
            u.UpdateLvl(backLevel)
        i.UpdateDetectors() # Update the coord and state of the detectors
    cf.nb_key = 0 # reset the number of key taken by the player
    for i in range(len(keys)): # For all keys
        keys[i].SetCoord(keys_position[lvl-1][i]) # set the coordinate of each key
        keys[i].Restore() # inform they are not taken
        keys[i].UpdateState() # Update their state (show them)

def isLevelEnded(lvl, lvlsEnd, sprites, total_nb_key):  # check if the player touch the door and have all keys
    for i in sprites: # for all players
        # if player's coord are in the square made by the door
        if i.coord[0] > lvlsEnd[lvl-1][0][0] and i.coord[0] < lvlsEnd[lvl-1][1][0] and i.coord[1] > lvlsEnd[lvl-1][0][1] and i.coord[1] < lvlsEnd[lvl-1][1][1]:
            if cf.nb_key >= total_nb_key: # check if the player have collected all keys
                return True # return that the player have ended the level
    return False # return that the player haven't ended the level

def PlayMusic(path):  # play music
    pygame.mixer.music.fadeout(1) # stop music which is playing
    pygame.mixer.music.load(path) # load the new music
    if cf.soundMusic:
        pygame.mixer.music.set_volume(0.5) # set the volume of the music to 0.5
    pygame.mixer.music.play(-1) # Play it indefinitely (loop)

def PlayEffect(path):
    if cf.soundEffect:
        effect = pygame.mixer.Sound(path)
        effect.play()

def Text(msg, coord, size, screen): # blit to the screen a text
    Grey = pygame.Color("white") # set the color of the text
    font = pygame.font.Font("Font/MinecraftBold.otf", size) # set the font
    return screen.blit(font.render(msg, True, Grey), coord) # return and blit the text on the screen

def GoToMenu(): # start the menu
    cf.GameStart = False # inform the game have stop
    cf.ButtonsClicked[0] = False # reset the button in charge of the game start
    cf.hasCheat = False
    main() # start the menu

### --------------------------------------  Menu Main Loop -------------------------------------- ###

def main(): # This is the main function for the menu.

    screen, clock, background, Artifacts = Initialization.StartGame() # initialize some varaibles (pygame, artifacts)
    cf.inMenu = True
    pygame.time.delay(50)
    PlayMusic('Sounds/Menu.mp3') # play the music's menu

    while True: # while the menu isn't quit
        clock.tick(cf.fps) # fps
        cf.MouseClick = False  # inform that the mouse's button isn't clicked
        for event in pygame.event.get(): # for all pygame's events
            if event.type == pygame.QUIT: # if cross is clicked
                cf.GameStart = False  # inform the game isn't start yet
                cf.ButtonsClicked[0] = False # inform the play button isn't click yet
                pygame.mixer.quit() # stop all pygame's sounds
                cf.Quit = True # inform the program is quit
                return pygame.QUIT # return and quit pygame
            if event.type == pygame.MOUSEBUTTONUP: # if click
                cf.MouseClick = True # inform that the mouse's button is clicked
                #print("-----  MOUSE : ", pygame.mouse.get_pos())  # print the mouse position (! feature unuse !)

        CalculationMenu(Artifacts) # make all calculation about artifact in the menu
        DisplayUpdateMenu(screen, background, Artifacts) # Update the window

        if cf.ButtonsClicked[0]: # if Artifact 'Play' is clicked : cf.ButtonsClicked('Play', ...)
            cf.GameStart = True  # Start the game

        if cf.ButtonsClicked[1] is True or getInputs()[6] == 1:
            if cf.inMenu:
                cf.inMenu = False
                pygame.time.delay(200)
            else:
                cf.inMenu = True
                pygame.time.delay(200)
            cf.ButtonsClicked[1] = False

        if cf.ButtonsClicked[2] is True or getInputs()[7] == 1:
            if cf.soundMusic:
                cf.soundMusic = False
                pygame.mixer.music.set_volume(0.0)
                pygame.time.delay(100)
            else:
                cf.soundMusic = True
                cf.musicVolume = 0.5
                pygame.mixer.music.set_volume(0.5)
                pygame.time.delay(100)
            cf.ButtonsClicked[2] = False

        if getInputs()[8] == 1:
            if cf.soundEffect:
                PlayEffect('Sounds/SoundEffectOFF.wav')
                cf.soundEffect = False
            else:
                cf.soundEffect = True
                PlayEffect('Sounds/SoundEffectON.wav')
            pygame.time.delay(80)

        if cf.GameStart == True: # if the game is start
            PlayEffect('Sounds/Start.wav') # play sound_button effect
            return LaunchGame() # return and start the main fonction of the game

### ------------------------------------------------------------------------------------------------ ###

def DisplayUpdateMenu(screen, background, Artifacts):  # Update the menu's window
    if cf.inMenu:
        screen.blit(pygame.transform.scale(background[round(cf.MenuBackPhase/10)], (screen.get_width(), screen.get_height())), (0,0)) # add the menu's background
        Text('Menu', [screen.get_width()-82, screen.get_height() - 42], 24, screen)
    else:
        screen.blit(pygame.transform.scale(pygame.transform.scale(pygame.image.load('Visuals/MenuBase/InfoBack.png') , cf.screenSize), (screen.get_width(), screen.get_height())), (0,0)) # add the menu's background
        Text('Press F : Menu', [screen.get_width() - 158, screen.get_height() - 20], 18, screen)

    if cf.soundMusic is True:
        Text('Music : ON', [10, screen.get_height()-24], 12, screen)
    else:
        Text('Music : OFF', [10, screen.get_height() - 24], 12, screen)
    if cf.soundEffect is True:
        Text('/  SFX : ON', [86, screen.get_height() - 24], 12, screen)
    else:
        Text('/  SFX : OFF', [86, screen.get_height() - 24], 12, screen)

    if cf.inMenu:
        for i in Artifacts: # for all artifacts (buttons)
            screen.blit(i.visual, i.coord) # add the current artifact visual
    pygame.display.update() # update the window

def CalculationMenu(Artifacts): # Make the calculation/check for the artifacts
    if cf.MenuBackPhase < 50:
        cf.MenuBackPhase += 1
    else:
        cf.MenuBackPhase = 0
    if cf.inMenu:
        for i in Artifacts: # for all artifacts
            i.VisualUpdate(isMouseOnIt(i)) # Update there visual
            i.isClick(isMouseOnIt(i), cf.MouseClick) # inform there are clicked


def isMouseOnIt(Artifact): # check if the mouse/cursor touch the current artifact
    mouse = pygame.mouse.get_pos() # get the coord of the mouse
    # if mouse/cursor touch the artifact
    if  Artifact.coord[0] < mouse[0] < Artifact.coord[0]+Artifact.OriginalSize[0]*5 and Artifact.coord[1] < mouse[1] < Artifact.coord[1]+Artifact.OriginalSize[1]*5:
        return True # return 'yes the mouse touch the artifact'
    else:
        return False # return 'no...'


if __name__ == "__main__" and cf.Quit == True: # if the game is quit (isn't start) and the program is execute
    cf.Quit = False # Inform the program is start (isn't quit)
    main() # start the main menu of the game