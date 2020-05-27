# Minimal pygame example
import pygame
import time
import random
import math
pygame.init()
screen = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()
scoreFont = pygame.font.SysFont('DejaVu Sans Mono', 90)
dashedline = pygame.image.load("dashedline.png")
captionFont = pygame.font.SysFont('DejaVu Sans Mono', 15)


paddlePlayer = 225
paddleAI = 225
ballPosition = (250, 250)
ballVelocity = (1,1)
randomDelay = 0
serveDirection = 1
scorePlayer = 0
scoreAI = 0
paused = False
pauseButtonPressed = False
def collision():
    return (math.fabs(ballPosition[0] - 20) < 2 and ballPosition[1] > paddlePlayer and ballPosition[1] < paddlePlayer + 50) or\
        (math.fabs(ballPosition[0] - 480) < 2 and ballPosition[1] > paddleAI and ballPosition[1] < paddleAI + 50)
def outBound():
    global scorePlayer, scoreAI
    if ballPosition[0] < 0:
        scoreAI = scoreAI + 1
        return True
    elif ballPosition[0] > 500:
        scorePlayer = scorePlayer + 1
        return True
    else:
        return False
# draws paddles and ball onto screen
def render():
    screen.fill((255, 220, 255))
    screen.blit(dashedline, (247, 0))
    pygame.draw.rect(screen, (220, 100, 200), (480, round(paddleAI), 15, 50), 0)
    pygame.draw.rect(screen, (220, 100, 200), (5, round(paddlePlayer), 15, 50), 0)
    pygame.draw.circle(screen, (220, 100, 200), (round(ballPosition[0]), round(ballPosition[1])), 10)
    drawText(str(scorePlayer), scoreFont, 100, 100)
    drawText(str(scoreAI), scoreFont, 400, 100)
    drawText("Please use W and S to move, P to pause.", captionFont, 5, 5)
    pygame.display.flip()
def bouncyBorders():
    return (ballPosition[1] < 0) or (ballPosition[1] > 500)
def drawText(text, font, x, y):
    surface = font.render(text, False, (220, 100, 200))
    screen.blit(surface, (x, y))

running = True
while running:
    # stops the game if the user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed_keys=pygame.key.get_pressed()
    render()
    if pressed_keys[pygame.K_p]:
        if not pauseButtonPressed:
            paused = not paused 
        pauseButtonPressed = not pauseButtonPressed
    if not paused:

        if pressed_keys[pygame.K_s]:
            paddlePlayer = paddlePlayer + 1.2
        if pressed_keys[pygame.K_w]:
            paddlePlayer = paddlePlayer - 1.2
        ballPosition = (ballPosition[0] + ballVelocity[0], ballPosition[1] + ballVelocity[1])
        if collision():
            randomDelay = random.randint(10, 101)
            ballVelocity = (ballVelocity[0] * -1, ballVelocity[1])
        if bouncyBorders():
            ballVelocity = (ballVelocity[0], ballVelocity[1] * -1)

        # the code that begins the new round and serves the ball
        if outBound():
            ballPosition = (250, 250)
            paddlePlayer = 225
            paddleAI = 225
            render()
            time.sleep(3)
            serveDirection = serveDirection * -1
            angle = random.uniform(-1, 1)
            speed = random.uniform(0.8, 1.4)
            ballVelocity = (math.cos(angle) * serveDirection * speed, math.sin(angle) * speed)
        # if the ball is above the AI, paddle moves up and vice versa
        if randomDelay > 0:
            randomDelay = randomDelay - 1
        elif ballPosition[1] <= paddleAI:
            paddleAI = paddleAI - 1.2
        elif ballPosition[1] >= paddleAI + 50:
            paddleAI = paddleAI + 1.2
    clock.tick(500)

pygame.quit()