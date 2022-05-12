import pygame

class Key:  # class for the keys in the level. Each level have 4 keys, player need to collect them to complete the level
    def __init__(self):
        self.coord = [0, 0] #[x, y]
        self.state = 0      # if shown or not (0 -> show / 1 -> hide)
        self.taken = 0      # if taken or note during a level
        self.visual = pygame.transform.scale(pygame.image.load('Visuals/key16x16.png'), (32, 32))  # visual of the key

    def SetCoord(self, coord):  # set the coordinate depending of the level
        self.coord[0] = coord[0]
        self.coord[1] = coord[1]

    def UpdateState(self):  # upadte it state if the key is taken
        if self.taken == 0:
            self.state = 0
        else:
            self.state = 1

    def TakeKey(self):  # if the key is taken
        self.taken = 1

    def Restore(self):  # if the key isn't taken
        self.taken = 0

    def getState(self): # get the current state of the key
        return self.state
