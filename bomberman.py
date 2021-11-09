from __future__ import print_function, division
import pygame, random

class player:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == UP:
            self.y -= 40
        elif direction == DOWN:
            self.y += 40
        elif direction == LEFT:
            self.x -= 40
        elif direction == RIGHT:
            self.x += 40

    def plant_bomb(self):
        stage[y][x] = bomb(self.x,self.y,2)

class bomb:

    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power
        self.explode_time = playtime + 2


HEIGHT = 480
WIDTH = 640
S_HEIGHT = 480//40
S_WIDTH = 640//40

UP = 0
DOWN = 1
LEFT = 3
RIGHT = 4

BLANK = 0
HARD_WALL = 1
SOFT_WALL = 2
BOMB = 3

# Initialize Pygame.
pygame.init()
# Set size of pygame window.
screen=pygame.display.set_mode((WIDTH,HEIGHT))
# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill((255, 255, 255))
# Convert Surface object to make blitting faster.
background = background.convert()
# Copy background to screen (position (0, 0) is upper left corner).
screen.blit(background, (0,0))
# Create Pygame clock object.  
clock = pygame.time.Clock()

mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 60
# How many seconds the "game" is played.
playtime = 0.0

stage = [[0 for x in range(S_WIDTH)] for y in range(S_HEIGHT)]
for i in range(0,S_WIDTH):
    for j in range(0,S_HEIGHT):
        stage[j][i] = BLANK

# make player 1
p1 = player(40, 40)

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_UP:
                p1.move(UP)
            elif event.key == pygame.K_DOWN:
                p1.move(DOWN)
            elif event.key == pygame.K_LEFT:
                p1.move(LEFT)
            elif event.key == pygame.K_RIGHT:
                p1.move(RIGHT)
            elif event.key == pygame.K_SPACE:
                p1.plant_bomb()

    # draw stage
    for i in range(0,S_WIDTH):
        for j in range(0,S_HEIGHT):
            if stage[j][i] == BLANK:
                pygame.draw.rect(screen, (255,255,255), (i*40,j*40,40,40), 0)
                pygame.draw.rect(screen, (211,211,211), (i*40,j*40,40,40), 1)
            elif isinstance(stage[j][i], bomb):
                if playtime < stage[j][i].explode_time:
                    pygame.draw.circle(screen, (0,0,255), (stage[j][i].x+20, stage[j][i].y+20), 20)
                elif stage[j][i].explode_time < playtime and playtime < stage[j][i].explode_time+1:
                    for i in range(0, stage[j][i].power):
                        pygame.draw.rect(screen, (255,0,0), (stage[j][i].x-i*40, stage[j][i].y, 40, 40), 0)
                        pygame.draw.rect(screen, (255,0,0), (stage[j][i].x+i*40, stage[j][i].y, 40, 40), 0)
                        pygame.draw.rect(screen, (255,0,0), (stage[j][i].x, stage[j][i].y-i*40, 40, 40), 0)
                        pygame.draw.rect(screen, (255,0,0), (stage[j][i].x, stage[j][i].y+i*40, 40, 40), 0)
                else:
                    stage[j][i] = BLANK

    # draw player1
    pygame.draw.rect(screen, (0,0,0), (p1.x, p1.y, 40, 40), 0)


    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()