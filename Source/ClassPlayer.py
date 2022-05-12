import pygame
import ClassDetectors
import config as cf

class player:   # Class for the player : control moovement / visual
    def __init__(self, screen):
        self.coord = [0,0] # [x, y]
        self.speed = [0,0] # [Vx, Vy]
        # load all visuals of the player
        self.visuals = [pygame.image.load("PlayersVisuals/stand.png"), pygame.image.load("PlayersVisuals/right1.png"), pygame.image.load("PlayersVisuals/right2.png"), pygame.image.load("PlayersVisuals/left1.png"), pygame.image.load("PlayersVisuals/left2.png")]
        self.visual = self.visuals[0] # set the visual to the default visual
        self.detectors = []  # list which contain all detectors of the player
        self.screen = screen  # get the pygame screen
        self.VisualPhase = 0    # to manage the visual aspect when the player is running
        self.isJumping = False  # to know if the player is in the air or in the ground
        self.wallJump = 0       # to know how many wall-jump the player have done

    def setDetectors(self):  # initialize ans set the detectors of the player
        for i in range(5):
            self.detectors.append(ClassDetectors.detector((self.visual.get_width(), self.visual.get_height()), self.screen)) # append a detector object (class detector)
        for i in range(len(self.detectors)):
            self.detectors[i].setSide(i) # assign a side to each detector

    def UpdateDetectors(self):  # Update detectors coord / state and check if player is in the ground
        for i in self.detectors:
            i.CoordUpdate(self.coord)
            i.StateUpdate()
        if self.detectors[3].getState() == 1:  # check if the player is in the ground
            self.isJumping = False  # set jumps to false
            self.wallJump = 0       # reset nb of current wall jumps to 0
        else:
            self.isJumping = True   # if the player is not on the ground, it means that he is in the air

    def UpdateSpeed(self, inputs):  # Update the speed [Vx, Vy] depending on keyboard inputs and detectors state
        # inputs[right_arrow/d, left_arrow/q, up_arrow/z, down_arrow/s, space, k, f]
        if inputs[0] == 1 and self.speed[0] < cf.maxSpeed:  # Go right
            self.speed[0] += cf.HoriSpeedIncrement
        if inputs[1] == 1 and self.speed[0] > -cf.maxSpeed: # Go left
            self.speed[0] += -cf.HoriSpeedIncrement

        if inputs[2] == 1 and self.detectors[4].getState() == 0 and self.isJumping == False:  # Jump
            self.PlayEffect('Sounds/Jump.wav')  # play sound_button effect without block the thread
            self.speed[1] = -cf.JumpPower # set the speed Vy to jump power

        # Wall jumps : if we are jumping, against a wall, nb of wall_jump < max_nb_wall_jump, up_arrow & left/right_arrow pressed
        if inputs[2] == 1 and inputs[0] == 1 and self.detectors[0].getState() == 1 and self.detectors[3].getState() == 0 and self.isJumping == True and self.wallJump < cf.MaxWallJump:  # Right wall jump
            self.PlayEffect('Sounds/WallJump.wav')
            self.speed[0] = -cf.WallJumpPower
            self.speed[1] = -cf.WallJumpPower
            self.wallJump += 1

        if inputs[2] == 1 and inputs[1] == 1 and self.detectors[1].getState() == 1 and self.detectors[3].getState() == 0 and self.isJumping == True and self.wallJump < cf.MaxWallJump:  # Left wall jump
            self.PlayEffect('Sounds/WallJump.wav')
            self.speed[0] = cf.WallJumpPower
            self.speed[1] = -cf.WallJumpPower
            self.wallJump += 1

        if self.speed[0] > 0:                           # Speed Control horizontal (slow down)
            self.speed[0] += -cf.HoriSpeedIncrement/2
        if self.speed[0] < 0:
            self.speed[0] += cf.HoriSpeedIncrement/2

        if self.speed[1] < cf.maxSpeedVerti:            # Speed Control Vertical (gravity)
            self.speed[1] += cf.VertiSpeedIncrement

        if self.detectors[0].getState() == 1 and self.speed[0] > 0:    # collision depending on detectors state and current speed
            self.speed[0] = 0
        if self.detectors[1].getState() == 1 and self.speed[0] < 0:
            self.speed[0] = 0
        if self.detectors[2].getState() == 1 and self.speed[1] < 0:
            self.speed[1] = 0
        if self.detectors[3].getState() == 1 and self.speed[1] > 0:
            self.speed[1] = 0

        if cf.HoriSpeedIncrement/2 > self.speed[0] > -cf.HoriSpeedIncrement/2:    # Speed Stop round
            self.speed[0] = 0
        if cf.VertiSpeedIncrement/2 > self.speed[1] > -cf.VertiSpeedIncrement/2:
            self.speed[1] = 0

        self.UpdateVisual()  # Update of the displayed visual of the player depending of the current speed

    def UpdateCoord(self):  # Update the coordinate of the player depending of his current speed
        self.coord[0] += self.speed[0]
        self.coord[1] += self.speed[1]
        self.UpdateDetectors() # Update the detectors with the new player's position
        if self.detectors[4].getState() == 1:  # if in the ground
            self.coord[1] += -8                # climb 8 pixel

    def UpdateVisual(self):   # Depending of the current speed, update the displayed visual of the player
        if self.speed[0] > 0: # if go right
            if self.isJumping == True and self.speed[1] < 0: # if jumping and climbing
                self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/RightJump.png"), (16, 32))
            elif self.isJumping == True: # if jumping and go down
                self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/Down.png"), (16, 32))
            else: # if not jumping = if walk right
                if self.VisualPhase < 4:
                    self.VisualPhase += 1
                    self.visual = pygame.transform.scale(self.visuals[1], (16, 32))
                elif self.VisualPhase < 8:
                    self.VisualPhase += 1
                    self.visual = pygame.transform.scale(self.visuals[2], (16, 32))
                elif self.VisualPhase >= 8:
                    self.VisualPhase = 0
        elif self.speed[0] < 0: # if go left
            if self.isJumping == True and self.speed[1] < 0: # if jumping and climbing
                self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/LeftJump.png"), (16, 32))
            elif self.isJumping == True: # if jumping and go down
                self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/Down.png"), (16, 32))
            else: # if not jumping = if walk right
                if self.VisualPhase < 4:
                    self.VisualPhase += 1
                    self.visual = pygame.transform.scale(self.visuals[3], (16, 32))
                elif self.VisualPhase < 8:
                    self.VisualPhase += 1
                    self.visual = pygame.transform.scale(self.visuals[4], (16, 32))
                elif self.VisualPhase >= 8:
                    self.VisualPhase = 0

        elif self.isJumping == True and self.speed[1] < 0:  # if not going right or left but jumping and climbing
            self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/RightJump.png"), (16, 32))
        elif self.isJumping == True:  # if not going right or left but go down
            self.visual = pygame.transform.scale(pygame.image.load("PlayersVisuals/Down.png"), (16, 32))
        else:
            self.visual = pygame.transform.scale(self.visuals[0], (16, 32))

    def PlayEffect(self, path):
        if cf.soundEffect:
            effect = pygame.mixer.Sound(path)
            effect.play()