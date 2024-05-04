import pygame
import os
import random
import time
import math

pygame.init()

#fonts 
SCORE_FONT = pygame.font.SysFont("Calibri", 30)
#constants

WIDTH, HEIGHT = 1200, 800
BLOB_X, BLOB_Y = 620, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)
FPS = 120
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PLAYER_COLORS = [RED, BLUE, GREEN, ORANGE, PINK]
START_TIME = time.time()

#images
RED_FOOD = pygame.image.load(os.path.join('agario', 'red.png'))
BLUE_FOOD = pygame.image.load(os.path.join('agario', 'blue.png'))
GREEN_FOOD = pygame.image.load(os.path.join('agario', 'green.png'))
ALGAE_BLOB = pygame.transform.scale(GREEN_FOOD, (750, 750))
ORANGE_FOOD = pygame.image.load(os.path.join('agario', 'orange.png'))
PINK_FOOD = pygame.image.load(os.path.join('agario', 'pink.png'))
YELLOW_FOOD = pygame.image.load(os.path.join('agario', 'yellow.png'))
FOOD_COLORS = [RED_FOOD, BLUE_FOOD, GREEN_FOOD, ORANGE_FOOD, PINK_FOOD, YELLOW_FOOD]

#sfx

#player variables
radius = 25
last_radius = 0
score = 0
user_text = ""

#game variables
blockSize = 40

#classes
class ObjectInterface():
    def __init__(self, xpos, ypos, img):
        self.xpos = xpos
        self.ypos = ypos
        self.img = img
    def update(self, x, y):
        window.blit(self.img, (x, y))
    def getXpos(self):
        return self.xpos
    def getYpos(self):
        return self.ypos
    def changeXpos(self, amount):
        self.xpos += amount
    def changeYpos(self, amount):
        self.ypos += amount

class Food(ObjectInterface):
    pass

#window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scuffed Agario")

#functions
def drawGrid(xdir, ydir, color, blockSize):
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect((x + xdir) % 1200, (y + ydir) % 800, blockSize, blockSize)
            pygame.draw.rect(window, color, rect, 1)

def draw_window(xdir, ydir, radius, foodArr, player_color, scene, rect2, user_text, playrect, algaeArr):
    if scene == 1:
        global score
        window.fill(WHITE)
        drawGrid(xdir, ydir, LIGHT_GRAY, blockSize)
        for i in algaeArr:
            i.update((i.getXpos() + xdir) % 1200, (i.getYpos() + ydir) % 800)
        for i in foodArr:
            i.update((i.getXpos() + xdir) % 1200, (i.getYpos() + ydir) % 800)
        score_text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
        rect = pygame.Rect(0, 750, 150, 50)
        pygame.draw.rect(window, BLACK, rect)
        window.blit(score_text, (0, 750))
        pygame.draw.circle(window, player_color, (BLOB_X, BLOB_Y), radius)
        name_text = SCORE_FONT.render(user_text, True, BLACK)
        window.blit(name_text, (BLOB_X - 20 - (len(user_text) * 3), BLOB_Y - 20))
    else:
        window.fill((215, 215, 215))
        drawGrid(0, 0, BLACK, 40)
        rect = pygame.Rect(425, 100, 350, 500)
        pygame.draw.rect(window, WHITE, rect)
        pygame.draw.rect(window, BLACK, rect2, 1)
        window.blit(RED_FOOD, (100, 200))
        window.blit(ORANGE_FOOD, (200, 270))
        window.blit(YELLOW_FOOD, (300, 320))
        window.blit(GREEN_FOOD, (65, 400))
        window.blit(BLUE_FOOD, (30, 120))
        window.blit(PINK_FOOD, (912, 400))
        window.blit(RED_FOOD, (1020, 200))
        window.blit(RED_FOOD, (164, 700))
        window.blit(ORANGE_FOOD, (200, 650))
        window.blit(YELLOW_FOOD, (340, 220))
        window.blit(GREEN_FOOD, (1000, 450))
        window.blit(BLUE_FOOD, (61, 150))
        window.blit(PINK_FOOD, (912, 20))
        window.blit(RED_FOOD, (230, 141))
        window.blit(RED_FOOD, (464, 660))
        window.blit(ORANGE_FOOD, (980, 760))
        window.blit(YELLOW_FOOD, (890, 450))
        window.blit(GREEN_FOOD, (1100, 234))
        window.blit(BLUE_FOOD, (145, 750))
        window.blit(PINK_FOOD, (1058, 399))
        window.blit(RED_FOOD, (80, 61))
        username = SCORE_FONT.render("Username: " + user_text, True, BLACK)
        window.blit(username, (435, 123))
        play = SCORE_FONT.render("Play?", True, BLACK)
        pygame.draw.rect(window, GREEN, playrect)
        window.blit(play, (565, 200))
    pygame.display.update()

def checkAddDot(foodArr):
    if len(foodArr) < 50:
        food = Food(random.randint(0, 1175), random.randint(0, 775), FOOD_COLORS[random.randint(0, len(FOOD_COLORS) - 1)])
        foodArr.append(food)

def checkAddAlgae(algaeArr, elapsedTime):
    if len(algaeArr) < 2 and elapsedTime % 10 == 0:
        algae = Food(random.randint(0, 1175), random.randint(0, 775), ALGAE_BLOB)
        algaeArr.append(algae)

def checkAlgaeCollision(algaeArr, xdir, ydir):
    global radius
    for i in algaeArr:
        if (math.pi * (radius ** 2)) > 9000 and (BLOB_X - radius) <= ((i.getXpos() + xdir) % 1200) <= (BLOB_X + radius) and (BLOB_Y - radius) <= ((i.getYpos() + ydir) % 800) <= (BLOB_Y + radius):
            algaeArr.remove(i)
            area = math.pi * (radius ** 2)
            area -= 1000
            radius = math.sqrt(area / math.pi)

def checkCollision(foodArr, xdir, ydir):
    global radius, score, last_radius, blockSize
    for i in foodArr:
        if (BLOB_X - radius) <= ((i.getXpos() + xdir) % 1200) <= (BLOB_X + radius) and (BLOB_Y - radius) <= ((i.getYpos() + ydir) % 800) <= (BLOB_Y + radius):
            foodArr.remove(i)
            area = math.pi * (radius ** 2)
            area += 25
            if radius > last_radius:
                score += 1
            last_radius = max(last_radius, radius)
            radius = math.sqrt(area / math.pi)
def main():
    global user_text
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True
    foodArr = []
    algaeArr = []
    player_color = PLAYER_COLORS[random.randint(0, len(PLAYER_COLORS) - 1)]
    l = False
    r = False
    u = False
    d = False
    active = False
    scene = 0
    xdir = 0.1
    ydir = 0.1
    rect2 = pygame.Rect(575, 125, 200, 25)
    playrect = pygame.Rect(550, 200, 100, 30)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if rect2.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
                if playrect.collidepoint(event.pos):
                    scene = 1
            elif event.type == pygame.KEYDOWN: 
                if active and event.key == pygame.K_BACKSPACE: 
                    user_text = user_text[:-1]  
                elif active and len(user_text) <= 10: 
                    user_text += event.unicode
        if scene == 1:
            elapsedTime = int(time.time() - START_TIME)
            checkAddDot(foodArr)
            checkAddAlgae(algaeArr, elapsedTime)
            checkAlgaeCollision(algaeArr, xdir, ydir)
            checkCollision(foodArr, xdir, ydir)
            pos = pygame.mouse.get_pos()
            if pos[0] < BLOB_X:
                l = True
                r = False
            elif pos[0] > BLOB_X:
                l = False
                r = True
            if pos[1] < BLOB_Y:
                d = False
                u = True
            elif pos[1] > BLOB_Y:
                d = True
                u = False
            if l:
                xdir += (abs(pos[0] - BLOB_X)) * (1 / (radius * 8))
            if r:
                xdir -= (abs(pos[0] - BLOB_X)) * (1 / (radius * 8))
            if u:
                ydir += (abs(pos[1] - BLOB_Y)) * (1 / (radius * 8))
            if d:
                ydir -= (abs(pos[1] - BLOB_Y)) * (1 / (radius * 8))
        draw_window(xdir, ydir, radius, foodArr, player_color, scene, rect2, user_text, playrect, algaeArr)
    pygame.quit()

if __name__ == "__main__":
    main()

#things to do 
    #- algae (make smaller)
    #- bots




