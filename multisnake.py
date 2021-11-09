from __future__ import print_function, division
import pygame, random

def rotate(l, n):
    return l[-n:] + l[:-n]

class snake:   

    def __init__(self, segs, d, nhx, nhy, ohx, ohy, c):
        self.segs = segs
        self.d = d
        self.nhx = nhx
        self.nhy = nhy
        self.ohx = ohx
        self.ohy = ohy
        self.c = c

    def move_head(self):
        (self.ohx, self.ohy) = self.segs[0]
        (self.otx, self.oty) = self.segs[len(self.segs)-1]

        self.segs = rotate(self.segs, 1)

        if self.d == UP:
            self.segs[0] = (self.ohx, self.ohy-1)
        elif self.d == DOWN:
            self.segs[0] = (self.ohx, self.ohy+1)
        elif self.d == LEFT:
            self.segs[0] = (self.ohx-1, self.ohy)
        elif self.d == RIGHT:
            self.segs[0] = (self.ohx+1, self.ohy)

        (self.nhx, self.nhy) = self.segs[0]

        if self.check_collision():
            print("Collision!")
            pygame.quit()

    def check_collision(self):
        return ((self.segs[0] in self.segs[1:len(self.segs)] or self.nhx < 0 or 
            self.nhx >= S_WIDTH or self.nhy < 0 or self.nhy >= S_HEIGHT)
            or (MULTIPLAYER and (self.segs[0] in p1.segs[1:len(p1.segs)]
                                or self.segs[0] in p2.segs[1:len(p2.segs)]
                                or self.nhx < 0 or self.nhx >= S_WIDTH
                                or self.nhy < 0 or self.nhy >= S_HEIGHT)))

    def eat(self):
        if stage[self.nhy][self.nhx] == FOOD:
            self.segs.append((self.otx,self.oty))
            stage[self.nhy][self.nhx] = BLANK
            spawn_food()

    def draw_snake(self):
        for place, (x, y) in enumerate(self.segs):
            pygame.draw.rect(screen, self.c, (x*10,y*10,10,10), 0)


def spawn_food():
    stage[random.randint(0,S_HEIGHT-1)][random.randint(0,S_WIDTH-1)] = FOOD

HEIGHT = 480
WIDTH = 640
S_HEIGHT = 480//10
S_WIDTH = 640//10

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
STOP = 4

BLANK = 0
FOOD = 1
WALL = 2

MULTIPLAYER = False

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
FPS = 20
# How many seconds the "game" is played.
playtime = 0.0

stage = [[0 for x in range(S_WIDTH)] for y in range(S_HEIGHT)]
for i in range(0,S_WIDTH):
    for j in range(0,S_HEIGHT):
        stage[j][i] = BLANK
spawn_food()

# smaller index -> closer to head
p1 = snake([(S_WIDTH*2//3, S_HEIGHT//3)], STOP, 0, 0, 0, 0, (0,0,0))
p2 = snake([(S_WIDTH//3, S_HEIGHT*2//3)], STOP, 0, 0, 0, 0, (0,0,255))


while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 

    for i in range(0,S_WIDTH):
        for j in range(0,S_HEIGHT):
            if stage[j][i] == BLANK:
                pygame.draw.rect(screen, (255,255,255), (i*10,j*10,10,10), 0)
                pygame.draw.rect(screen, (211,211,211), (i*10,j*10,10,10), 1)
            elif stage[j][i] == FOOD:
                pygame.draw.rect(screen, (0,225,0), (i*10,j*10,10,10), 0)

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_UP:
                if p1.d != DOWN:
                    p1.d = UP
            elif event.key == pygame.K_DOWN:
                if p1.d != UP:
                    p1.d = DOWN
            elif event.key == pygame.K_LEFT:
                if p1.d != RIGHT:
                    p1.d = LEFT
            elif event.key == pygame.K_RIGHT:
                if p1.d != LEFT:
                    p1.d = RIGHT
            if MULTIPLAYER:
                if event.key == pygame.K_w:
                    if p2.d != DOWN:
                        p2.d = UP
                elif event.key == pygame.K_s:
                    if p2.d != UP:
                        p2.d = DOWN
                elif event.key == pygame.K_a:
                    if p2.d != RIGHT:
                        p2.d = LEFT
                elif event.key == pygame.K_d:
                    if p2.d != LEFT:
                        p2.d = RIGHT

    if not MULTIPLAYER:
        # move snake
        p1.move_head()

        # eat food
        p1.eat()

        # draw snake
        p1.draw_snake()
                 
        # Print framerate and playtime in titlebar.
        text = "Score: " + str(len(p1.segs)) + "   FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    elif MULTIPLAYER:
        # move snake
        p1.move_head()
        p2.move_head()

        # eat food
        p1.eat()
        p2.eat()

        # draw snake
        p1.draw_snake()
        p2.draw_snake()
                 
        # Print framerate and playtime in titlebar.
        text = "P1: " + str(len(p1.segs)) + "   P2: " + str(len(p2.segs)) +"   FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)


    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("Your score is " + str(len(p1.segs)))