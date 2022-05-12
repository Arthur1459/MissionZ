import pygame

class detector:   # Class detectors : those are object which detecte colors and change of state depending of them. There is 5 detectors on a player : right, left, up, down, down middle
    def __init__(self, size, screen):
        self.coord = [0,0] # coordinate [x, y]
        self.side = [0,0]  # modifier for the coordinate to assign a side at the object (ex: Right -> [16, 0])
        self.state = 0  # will change depending on color detected
        self.size = size # The size of the player to put the detector at the right place
        self.screen = pygame.transform.scale(pygame.image.load("Visuals/structure/lvl_1_250x75.png"), (screen.get_width(), screen.get_height())) # load a default backgound for the detectors
        self.screenSize = [screen.get_width(), screen.get_height()]  # set the size of the screen
        self.palette = [self.screen.get_at((10,10)), self.screen.get_at((30,10)), self.screen.get_at((50,10))]  # get the reference colors -> [nothing, wall, kill]
        self.visual = pygame.image.load("PlayersVisuals/detector.png") # load the default visual of the detectors ( ! feature unuse ! )

    def StateUpdate(self):  # Compare the current pixel at the detectors position the the reference colors and update the state depending of that
        if self.screen.get_at((round(self.coord[0]), round(self.coord[1]))) == self.palette[0]:
            self.state = 0
            self.visual = pygame.image.load("PlayersVisuals/detector.png")
        elif self.screen.get_at((round(self.coord[0]), round(self.coord[1]))) == self.palette[1]:
            self.state = 1
            self.visual = pygame.image.load("PlayersVisuals/detector2.png")
        elif self.screen.get_at((round(self.coord[0]), round(self.coord[1]))) == self.palette[2]:
            self.state = 2
            self.visual = pygame.image.load("PlayersVisuals/detector2.png")
        else:
            self.state = 0
            self.visual = pygame.image.load("PlayersVisuals/detector.png")  # by default

    def UpdateLvl(self, BackLvl):   # load the current lvl structure -> BackLvl
        self.screen = pygame.transform.scale(BackLvl, (self.screenSize[0], self.screenSize[1]))


    def getState(self): # to get the state of the current detector
        return self.state

    def setSide(self, side):  # initialize the side assigned for the current detector
        if side == 0:
            self.side = [round(self.size[0]) + 8, round(self.size[1]/2)]  # right
        elif side == 1:
            self.side = [-4, round(self.size[1]/2)]  # left
        elif side == 2:
            self.side = [round(self.size[0]/2) + 2, 0]   # up
        elif side == 3:
            self.side = [round(self.size[0]/2) + 2, round(self.size[1])*2]  # down
        elif side == 4:
            self.side = [round(self.size[0]/2) + 2, round(self.size[1]) + 12]  # middle down   (used for detect if the player is in the ground)

    def CoordUpdate(self, coord):  # update the coord of the detectors depending the player's coord and the side of the current detector
        self.coord[0] = coord[0] + self.side[0]
        self.coord[1] = coord[1] + self.side[1]
        self.StateUpdate() # (update state at the same time)
