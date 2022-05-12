# ----- imports -----
import pygame
import ClassPlayer
import ClassKeys
import config as cf
import ClassMenuArtefact as ma
# -------------------

def Init():   # Initialisation of the main game

    pygame.init()                   # pygame initialization
    pygame.mixer.init(44100, 16, 16)
    pygame.font.init()

    # Logo / Icon / Name
    logo = pygame.image.load("Visuals/logo16x16.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MissionZ")

    # screen initialisation
    screen_width, screen_height = cf.OriginalScreenSize[0], cf.OriginalScreenSize[1]
    screen = pygame.display.set_mode((screen_width, screen_height))

    # time / clock creation
    clock = pygame.time.Clock() # init clock

    sprites = [ClassPlayer.player(screen)]      # Player Initialisation
    for i in sprites:
        i.setDetectors()  # set the side and position detectors of the player

    # how add a level :
    # - add the level structure + lvl displayed
    # - add the start position + door position
    # - add the keys positions
    # - add the music

    # load the levels : The structure in lvls (for the detectors) and what is shown on lvlsDisplayed
    lvlsDisplayed = [pygame.image.load("Visuals/lvl_1_250x75.png"), pygame.image.load(
        "Visuals/lvl_2_250x75.png"), pygame.image.load("Visuals/lvl_3_250x75.png"), pygame.image.load(
        "Visuals/lvl_4_250x75.png"), pygame.image.load("Visuals/lvl_5_250x75.png"), pygame.image.load(
        "Visuals/lvl_6_250x75.png")]
    lvls = [pygame.image.load("Visuals/structure/lvl_1_250x75.png"), pygame.image.load(
        "Visuals/structure/lvl_2_250x75.png"), pygame.image.load("Visuals/structure/lvl_3_250x75.png"), pygame.image.load(
        "Visuals/structure/lvl_4_250x75.png"), pygame.image.load("Visuals/structure/lvl_5_250x75.png"), pygame.image.load(
        "Visuals/structure/lvl_6_250x75.png")]

    # format : [[x, y], [x, y], ect...]
    #           lvl 1    lvl 2
    lvlsStart = [[60, 620], [60, 620], [60, 100], [100, 650], [1150, 100], [200, 100]] # all position where the player start the level
    # format : [ [ [x1, y1], [x2, y2] ], [ [], [] ] ect...]
    #           lvl1 : borne 1   borne 2, lvl 2 : ...
    lvlsEnd = [[[1100, 300], [1200, 400]], [[1100, 100], [1200, 200]], [[1100, 50], [1200, 150]], [[845, 55], [945, 155]], [[375, 275], [475, 375]], [[200, 600], [300, 700]]] # where the doors is (between the two points)

    # set the position of the keys in each level [ [lvl1 => [key1], [key2]...], [lvl2], ... ]
    keys_position = [[[150,650],[535,455],[810,490],[1030,340]], [[410,190],[655,150],[790,510],[100,350]],  [[390,150],[360,360],[760,400],[870,100]], [[110,360],[510,105],[1170,120],[910,420]], [[210,380],[310,100],[740,500],[560,360]], [[310,100],[780,530],[425,580],[220,270]]]
    keys = [ClassKeys.Key(), ClassKeys.Key(), ClassKeys.Key(), ClassKeys.Key()]

    # load the music of each level
    musics = ['Sounds/MusicLevel1.mp3', 'Sounds/MusicLevel2.mp3', 'Sounds/MusicLevel3.mp3', 'Sounds/MusicLevel4.mp3', 'Sounds/MusicLevel5.mp3', 'Sounds/MusicLevel6.mp3']

    # load the visuals of the door
    endVisuals = [pygame.image.load('Visuals/door/Door0.png'), pygame.image.load(
        'Visuals/door/Door1.png'), pygame.image.load(
        'Visuals/door/Door2.png'), pygame.image.load('Visuals/door/Door3.png'), pygame.image.load(
        'Visuals/door/Door4.png')]

    file = open('record.txt', 'r')
    cf.record = int(file.read())

    return screen, clock, sprites, lvls, lvlsStart, lvlsEnd, musics, lvlsDisplayed, keys_position, keys, endVisuals

def StartGame():  # Initialization of the menu

    pygame.init()                                   # Pygame init
    pygame.mixer.init(44100, 16, 16)
    pygame.font.init()

    # Logo / Icon / Name
    logo = pygame.image.load('Visuals/logo16x16.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MissionZ - Menu")

    # screen initialisation
    screen_width, screen_height = cf.OriginalScreenSize[0], cf.OriginalScreenSize[1]
    screen = pygame.display.set_mode((screen_width, screen_height))

    # time / clock creation
    clock = pygame.time.Clock() # init clock
    Background = [pygame.transform.scale(pygame.image.load('Visuals/MenuBase/Layer_1.png'), cf.OriginalScreenSize), pygame.transform.scale(pygame.image.load(
         'Visuals/MenuBase/Layer_2.png'), cf.OriginalScreenSize), pygame.transform.scale(pygame.image.load(
         'Visuals/MenuBase/Layer_3.png'), cf.OriginalScreenSize), pygame.transform.scale(pygame.image.load(
         'Visuals/MenuBase/Layer_4.png'), cf.OriginalScreenSize), pygame.transform.scale(pygame.image.load(
         'Visuals/MenuBase/Layer_5.png'), cf.OriginalScreenSize), pygame.transform.scale(pygame.image.load(
         'Visuals/MenuBase/Layer_6.png'), cf.OriginalScreenSize)] # load backgound

    artefactsCoord = [[630, 330], [430, 350], [230, 350]]   # initialise the position of the firts artifact
    artefactsVisuals = [[pygame.image.load('Visuals/buttons/play.png'), pygame.image.load(
         'Visuals/buttons/playClicked.png')], [pygame.image.load('Visuals/buttons/info1.png'), pygame.image.load(
         'Visuals/buttons/info2.png')], [pygame.image.load(
         'Visuals/buttons/sound_button/on_sound1.png'), pygame.image.load(
         'Visuals/buttons/sound_button/on_sound2.png'), pygame.image.load(
         'Visuals/buttons/sound_button/off_sound1.png'), pygame.image.load(
         'Visuals/buttons/sound_button/off_sound2.png')]] # load the visuals of each artifact
    MenuArtefacts = [] # init list of each artifact
    for i in range(len(artefactsCoord)):
        MenuArtefacts.append(ma.Artefact(artefactsVisuals, i, artefactsCoord[i]))  # append each artifacts objects

    return screen, clock, Background, MenuArtefacts