import pygame
import config as cf

class Artefact:   # Class to use button/artefact in the menu page
    def __init__(self, artifactsVisuals, type, coord):
        self.coord = coord   # position : [x, y]
        self.state = 0       # if the cursor is on it
        self.type = type     # Type refere to the button (0 -> play button)
        self.visuals = artifactsVisuals     # all visuals of all buttons/artifacts
        self.visual = self.visuals[type][0]    # visual of the current object, depend of his type
        self.OriginalSize = [self.visual.get_width(), self.visual.get_height()]  # register the original size of the visual


    def VisualUpdate(self, iscontact):
        if iscontact: # if the mouse/cursor touch it
            self.visual = pygame.transform.scale(self.visuals[self.type][1], (self.OriginalSize[0]*5, self.OriginalSize[1]*5))  # set the visual to his first position and enlarge the visual by 20
            if self.state == 0:
                if cf.soundEffect:
                    if cf.soundEffect:
                        effect = pygame.mixer.Sound('Sounds/ButtonOverview.wav')
                        effect.play()
                self.state = 1
        else:
            self.visual = pygame.transform.scale(self.visuals[self.type][0], (self.OriginalSize[0]*5, self.OriginalSize[1]*5)) # set the visual to his second position and enlarge the visual by 20
            self.state = 0

        if self.type == 2:  # if it's the the sound_button button
            if cf.soundMusic:
                if iscontact:
                    self.visual = pygame.transform.scale(self.visuals[self.type][1], (self.OriginalSize[1]*5, self.OriginalSize[1]*5))
                else:
                    self.visual = pygame.transform.scale(self.visuals[self.type][0], (self.OriginalSize[0]*5, self.OriginalSize[1]*5))
            else:
                if iscontact:
                    self.visual = pygame.transform.scale(self.visuals[self.type][3], (self.OriginalSize[1]*5, self.OriginalSize[1]*5))
                else:
                    self.visual = pygame.transform.scale(self.visuals[self.type][2], (self.OriginalSize[1]*5, self.OriginalSize[1]*5))

    def isClick(self, iscontact, click):
        cf.ButtonsClicked[self.type] = False
        if iscontact and click: # if the mouse/cursor touch it and the mouse button is clicked
            cf.ButtonsClicked[self.type] = True   # in config.py modify the list of button pressed, depend of his type
