#from __future__ import print_function, division
import pygame, random

class pacman:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.curr_direction = STOP
        self.next_direction = STOP
        self.score = 0

    def move(self):
        if not self.hit_wall(self.next_direction):
            self.curr_direction = self.next_direction
        elif self.hit_wall(self.curr_direction):
            self.curr_direction = STOP

        if self.curr_direction == UP:
            self.y -= 2
        elif self.curr_direction == DOWN:
            self.y += 2
        elif self.curr_direction == LEFT:
            self.x -= 2
        elif self.curr_direction == RIGHT:
            self.x += 2

        if self.x <= 10:
            self.x = WIDTH-10
        elif self.x >= WIDTH-10:
            self.x = 10

        #print(self.x,self.y)

    def hit_wall(self, d):
        return ((d == UP and (stage[(self.x-10)//20][(self.y-12)//20] == WALL or stage[(self.x+8)//20][(self.y-12)//20] == WALL))
                or (d == DOWN and (stage[(self.x-10)//20][(self.y+10)//20] == WALL or stage[(self.x+8)//20][(self.y+10)//20] == WALL))
                or (d == LEFT and (stage[(self.x-12)//20][(self.y-10)//20] == WALL or stage[(self.x-12)//20][(self.y+8)//20] == WALL))
                or (d == RIGHT and (stage[(self.x+10)//20][(self.y-10)//20] == WALL or stage[(self.x+10)//20][(self.y+8)//20] == WALL)))

    def eat(self):
        if stage[self.x//20][self.y//20] == FOOD:
            stage[self.x//20][self.y//20] = BLANK
            self.score += 5

class ghost:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = STOP

    def move(self):
        while self.hit_wall(self.direction):
            self.direction = random.randint(0,3)

        # TODO: change directions at intersections

        if self.direction == UP:
            self.y -= 2
        elif self.direction == DOWN:
            self.y += 2
        elif self.direction == LEFT:
            self.x -= 2
        elif self.direction == RIGHT:
            self.x += 2

        self.check_kill()

    def check_kill(self):
        if ((player.x-14 <= self.x and self.x <= player.x-6)
            and (player.y-14 <= self.y and self.y <= player.y-6)):
                print("You died. Score: " + str(player.score))
                pygame.quit()

    def hit_wall(self, d):
        #print(self.x, self.y)
        return ((d == UP and stage[(self.x)//20][(self.y-2)//20] == WALL)
                or (d == DOWN and stage[(self.x)//20][(self.y+20)//20] == WALL)
                or (d == LEFT and stage[(self.x-2)//20][(self.y)//20] == WALL)
                or (d == RIGHT and stage[(self.x+20)//20][(self.y)//20] == WALL))



# dimensions in pixels
HEIGHT = 620
WIDTH = 560

# grid dimensions
S_HEIGHT = HEIGHT//20
S_WIDTH = WIDTH//20

# layout
BLANK = 0
FOOD = 1
WALL = 2

# directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
STOP = 4

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
background = background.convert()
screen.blit(background, (0,0))
clock = pygame.time.Clock()

mainloop = True
FPS = 60
playtime = 0.0

player = pacman(6*20+10,18*20+10)
pac = [0]*9
pac[0] = pygame.image.load('pac1.bmp')
pac[1] = pygame.image.load('pac2.bmp')
pac[2] = pygame.image.load('pac3.bmp')
pac[3] = pygame.image.load('pac4.bmp')
pac[4] = pygame.image.load('pac5.bmp')
pac[5] = pac[3]
pac[6] = pac[2]
pac[7] = pac[1]
pac[8] = pac[0]
pac_anim = 0.0
angle = 90

ghost1 = ghost(20,20)
ghost1.direction = RIGHT
ghost1_pic = pygame.image.load('ghost1.bmp')

ghost2 = ghost(520,20)
ghost2.direction = DOWN
ghost2_pic = pygame.image.load('ghost2.bmp')

ghost3 = ghost(520,580)
ghost3.direction = LEFT
ghost3_pic = pygame.image.load('ghost3.bmp')

ghost4 = ghost(20,580)
ghost4.direction = UP
ghost4_pic = pygame.image.load('ghost4.bmp')

# make stage
with open('./mapview.txt') as file:
     stage = [[int(digit) for digit in line.strip()] for line in file]

while mainloop:
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_UP:
                player.next_direction = UP
            elif event.key == pygame.K_DOWN:
                player.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                player.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                player.next_direction = RIGHT

    player.move()
    player.eat()

    ghost1.move()
    ghost2.move()
    ghost3.move()
    ghost4.move()

    # draw
    pygame.draw.rect(screen, (0,0,0), (0,0,560,620), 0)
    for j in range(0,S_HEIGHT):
        for i in range(0,S_WIDTH):
            # grid
            pygame.draw.rect(screen, (44,44,44), (i*20,j*20,20,20), 1)
            if stage[i][j] == FOOD:
                pygame.draw.rect(screen, (255,255,0), (8+i*20,8+j*20,4,4), 0)
            elif stage[i][j] == WALL:
                pygame.draw.rect(screen, (0,0,255), (i*20,j*20,20,20), 1)
    #pygame.draw.circle(screen, (255,255,0), (player.x,player.y), 10)

    screen.blit(ghost1_pic, (ghost1.x,ghost1.y))
    screen.blit(ghost2_pic, (ghost2.x,ghost2.y))
    screen.blit(ghost3_pic, (ghost3.x,ghost3.y))
    screen.blit(ghost4_pic, (ghost4.x,ghost4.y))

    if player.curr_direction == UP:
        angle = -90
    elif player.curr_direction == DOWN:
        angle = 90
    elif player.curr_direction == LEFT:
        angle = 0
    elif player.curr_direction == RIGHT:
        angle = -180

    screen.blit(pygame.transform.rotate(pac[int(pac_anim%9)],angle),(player.x-10,player.y-10))
    pac_anim += .5

    # Print framerate and playtime in titlebar.
    text = "Score: " + str(player.score) + "   FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

pygame.quit()
