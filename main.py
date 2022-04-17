import random  # For generating random numbers
import sys
import pygame
from pygame.locals import *  # Basic pygame imports
# Global Variables for the game
FPS = 32
SCREENWIDTH = 390
SCREENHIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHIGHT))
GROUNDY = SCREENHIGHT * 0.7
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'img/bird.png'
BACKGROUND = 'img/backgroung.png'
PIPE = 'img/pipe.png'


def welcomeScreen():
    '''
    Shows welcom images on the screen
    '''
    playerx = int(SCREENWIDTH/9)
    playery = int((SCREENHIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHIGHT*0.10)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user click on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/9)
    playery = int(SCREENHIGHT/2)
    basex = 0

    # Creat 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]
    # my List of loweer pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping

    playerFlapped = False  # it is true onle when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUND['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUND['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True
    return False

def getRandomPipe():
    '''
    generate positions of two pipe(one bottom straight and one top rotated) for bliting on the screen
    '''
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHIGHT -
                                   GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe

        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == '__main__':
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by CodeWithSwaraj')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('img/0.png').convert_alpha(),
        pygame.image.load('img/1.png').convert_alpha(),
        pygame.image.load('img/2.png').convert_alpha(),
        pygame.image.load('img/3.png').convert_alpha(),
        pygame.image.load('img/4.png').convert_alpha(),
        pygame.image.load('img/5.png').convert_alpha(),
        pygame.image.load('img/6.png').convert_alpha(),
        pygame.image.load('img/7.png').convert_alpha(),
        pygame.image.load('img/8.png').convert_alpha(),
        pygame.image.load('img/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'img/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('img/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    # Game sounds
    GAME_SOUND['die'] = pygame.mixer.Sound('music/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('music/jump.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('music/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('music/flay.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('music/point.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to user until he presses a button
        mainGame()  # This is the main game function
