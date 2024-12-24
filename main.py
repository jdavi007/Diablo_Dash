import pygame
import math
from random import randint
pygame.init()
pygame.mixer.init()

#Setup
screen = pygame.display.set_mode((800, 450))  # Window
pygame.display.set_caption('Diablo Dash')  # Window title
clock = pygame.time.Clock()  # Time
font = pygame.font.Font('fonts/HORNDB__.TTF', 100)
font2 = pygame.font.Font('fonts/HORNDB__.TTF', 30)
WHITE = 'White'  # Font colors
YELLOW = 'Yellow'
running = False
score = 0
backgroundScroll = 0   # For scrolling ground/background positions
backgroundScroll2 = 0  #
backgroundScroll3 = 0  #
groundScroll = 0       #
playerGravity = 0  # For jumps
jumpCount = 0  # For double jump
enemySpawnList = []  # Empty list for enemy spawns
dead = False  # To change "Start" to "Retry"

"""
Notes
ground level = (x, 380)
player start = (200, 380)

Things to do
font
"""

#Surfaces & Sprites
background = pygame.image.load('sprites/background.png')  # Settings
background2 = pygame.image.load('sprites/background2.png')
background3 = pygame.image.load('sprites/background3.png')
platform = pygame.image.load('sprites/largeplatform.png')
playerIdle = pygame.image.load('sprites/impidle.png')  # Player
playerRun1 = pygame.image.load('sprites/newplayerun1.png')
playerRun2 = pygame.image.load('sprites/newplayerun2.png')
playerRunList = [playerRun1, playerRun2]
playerIndex = 0
playerSurface = playerRunList[playerIndex]
playerJump1 = pygame.image.load('sprites/newplayerjump1.png')
playerJump2 = pygame.image.load('sprites/newplayerjump2.png')
playerJumpList = [playerJump2, playerJump1]
playerDeath = pygame.image.load('sprites/playerdeath.png')
enemyRun1 = pygame.image.load('sprites/newenemun1.png')  # Enemy
enemyRun2 = pygame.image.load('sprites/newenemrun2.png')
enemyRunList = [enemyRun1, enemyRun2]
enemyIndex = 0
enemySurface = enemyRunList[enemyIndex]
batFly1 = pygame.image.load('sprites/batfly1.png')  # Bat
batFly2 = pygame.image.load('sprites/batfly2.png')
batFly3 = pygame.image.load('sprites/batfly3.png')
batFly4 = pygame.image.load('sprites/batfly4.png')
batFlyList = [batFly1, batFly2, batFly3, batFly4]
batIndex = 0
batSurface = batFlyList[batIndex]
titleSurface = font.render('Diablo Dash', False, WHITE)   # Text
startSurface = font.render('Start', False, WHITE)
scoreSurface = font2.render(f"Score: {score}", False, WHITE)

#Rectangles
playerRectangle = playerSurface.get_rect(midbottom=(200, 380))
startRectangle = startSurface.get_rect(midbottom=(410, 300))
scoreRectangle = scoreSurface.get_rect(midbottom=(700, 35))
groundRectangle = platform.get_rect(center=(400, 360))

#Timers & Events
enemyTimer = pygame.USEREVENT + 1  # Enemy spawn timer
pygame.time.set_timer(enemyTimer, randint(500, 1500))  # Controls spawn time
enemyAnimTimer = pygame.USEREVENT + 2  # Enemy animation timer
pygame.time.set_timer(enemyAnimTimer, 300)  # Controls enemy frame times
batAnimTimer = pygame.USEREVENT + 3  # Bat animation timer
pygame.time.set_timer(batAnimTimer, 200)  # Controls bat frame times

#Sound
song = pygame.mixer.Sound('sounds/that-halloween-story-20692.mp3')  # Main song
jumpSound = pygame.mixer.Sound('sounds/jump_07.wav')
deathBell = pygame.mixer.Sound('sounds/tubular-bell-of-death-89485.mp3')
song.set_volume(.1)
jumpSound.set_volume(.15)
deathBell.set_volume(.2)
song.play(-1)


#Enemy function
def enemy(enemyList):
    global score, scoreSurface

    if enemyList:
        for enemy in enemyList:
            enemy.x -= 6  # Enemy speed
            if enemy.bottom == 380:  # Chooses sprite based on height of enemy
                screen.blit(enemySurface, enemy)  # Spawns devil
            else:
                screen.blit(batSurface, enemy)  # Spawns bat

        enemyCount = len(enemyList)
        enemyList = [enemy for enemy in enemyList if enemy.x > -10]  # Removes enemies once off-screen
        if enemyCount > len(enemyList):  # Increases score if enemy passes player
            score += 10
            scoreSurface = font2.render(f"Score: {score}", False, WHITE)  # Update score text

        return enemyList
    else:
        return []
#end enemy()


#Player animation function
def playerAnimation():
    global playerSurface, playerIndex

    if playerRectangle.bottom < 300:  # Jump
        playerIndex += 0.02  # Controls shift speed
        if playerIndex >= len(playerJumpList):  # Cycle through jump sprites
            playerIndex = 0  # Goes to beginning of list
        playerSurface = playerJumpList[int(playerIndex)]  # Update sprite
    else:  # Run
        playerIndex += 0.1  # Controls shift speed
        if playerIndex >= len(playerRunList):  # Cycle through run sprites
            playerIndex = 0  # Goes to beginning of list
        playerSurface = playerRunList[int(playerIndex)]  # Update sprite
#end playerAnimation()


#Collision function
def collision(target, colliders):
    if colliders:
        for collider in colliders:
            if target.colliderect(collider):
                return False
    return True
#end collision()


#Game loop
while True:
    #Event Loop
    for event in pygame.event.get():
        mousePosition = pygame.mouse.get_pos()  # Mouse position

        #Click Start
        if event.type == pygame.MOUSEBUTTONDOWN:  # Gets mouse click for menu
            if startRectangle.collidepoint(mousePosition):
                running = True

        #In-game Events
        if running:
            # Jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jumpCount < 2:  # Jump
                    jumpSound.play()
                    jumpCount += 1  # Increase jump count
                    playerGravity = -20  # Jump

            # Enemy Spawns
            if event.type == enemyTimer:
                #Adds enemy to enemy list
                if randint(0,2):
                    enemySpawnList.append(enemySurface.get_rect(midbottom=(randint(810, 850), 380)))
                else:
                    enemySpawnList.append(batSurface.get_rect(midbottom=(randint(810, 850), 240)))

            #Enemy animation
            if event.type == enemyAnimTimer:
                if enemyIndex == 0:
                    enemyIndex = 1
                else:
                    enemyIndex = 0
                enemySurface = enemyRunList[enemyIndex]

            #Bat animation
            if event.type == batAnimTimer:
                if batIndex > 2:
                    batIndex = 0
                else:
                    batIndex += 1
                batSurface = batFlyList[batIndex]

        #Quit
        if event.type == pygame.QUIT:
            running = False
            exit()

    if not running:
        score = 0

        #Images
        screen.blit(background3, (0, 0))  #
        screen.blit(background2, (0, 0))  # Backgrounds
        screen.blit(background, (0, 0))   #
        screen.blit(platform, (0, 260))  # Ground
        if dead:
            playerSurface = playerDeath
            playerRectangle.bottom = 410
        else:
            playerSurface = playerIdle  # For start screen
        screen.blit(playerSurface, playerRectangle)

        #Text
        screen.blit(titleSurface, (250, 110))  # Label
        screen.blit(startSurface, startRectangle)  # Start button

        #Highlights start button with mouse hover
        if startRectangle.collidepoint(mousePosition):
            if dead:
                startSurface = font.render('Retry', False, YELLOW)
            else:
                startSurface = font.render('Start', False, YELLOW)
        else:
            if dead:
                startSurface = font.render('Retry', False, WHITE)
            else:
                startSurface = font.render('Start', False, WHITE)

    if running:
        dead = False

        #Scrolling backgrounds
        backgroundWidth = background.get_width()
        backgroundWidth2 = background2.get_width()
        backgroundWidth3 = background3.get_width()
        tiles = math.ceil(800/backgroundWidth) + 1  # Rounds up and adds 1 for padding

        for i in range(0, tiles):
            screen.blit(background3, (i * backgroundWidth3 + backgroundScroll3, 0))  # Back
        backgroundScroll3 -= 0.25  # Speed
        if abs(backgroundScroll3) > backgroundWidth3:
            backgroundScroll3 = 0  # Reset

        for i in range(0, tiles):
            screen.blit(background2, (i * backgroundWidth2 + backgroundScroll2, 0))  # Middle
        backgroundScroll2 -= 0.5  # Speed
        if abs(backgroundScroll2) > backgroundWidth2:
            backgroundScroll2 = 0  # Reset

        for i in range(0,tiles):
            screen.blit(background, (i * backgroundWidth + backgroundScroll, 0))  # Closest
        backgroundScroll -= 1  # Speed
        if abs(backgroundScroll) > backgroundWidth:
            backgroundScroll = 0  # Reset

        # Scrolling ground
        ground_width = platform.get_width()
        for i in range(0, 2):
            screen.blit(platform, (i * ground_width + groundScroll, 260))  # Ground
        groundScroll -= 5  # Speed
        if abs(groundScroll) > ground_width:
            groundScroll = 0  # Reset

        #Score
        scoreSurface = font2.render(f"Score: {score}", False, WHITE)
        screen.blit(scoreSurface, scoreRectangle)

        #Player
        playerGravity += 1.5
        playerRectangle.y += playerGravity  # Gives the player gravity
        if playerRectangle.bottom >= 380:  # "Ground"
            jumpCount = 0  # Reset jump count
            playerRectangle.bottom = 380  # Puts player on ground
        playerAnimation()  # Animates player
        screen.blit(playerSurface, playerRectangle)

        #Enemies - Spawns/Removes enemies
        enemySpawnList = enemy(enemySpawnList)

        #Collision Checks - Returns False if player collides with enemy
        running = collision(playerRectangle, enemySpawnList)

        #Death
        if not running:
            dead = True  # Displays Retry button
            enemySpawnList = []  # Remove all enemies
            deathBell.play()
            titleSurface = font.render(f"Final Score: {score}", False, WHITE)
            playerRectangle.bottom = 380  # Put player on ground if still jumping
            screen.blit(playerSurface, playerRectangle)

    pygame.display.update()
    clock.tick(60)  # FPS
