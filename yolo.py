from __future__ import print_function, division
import pygame, random

def rotate(l, n):
    return l[-n:] + l[:-n]

def move_head(snake, direction):
    if direction == UP:
        snake[0] = (old_head_x, old_head_y-1)
    elif direction == DOWN:
        snake[0] = (old_head_x, old_head_y+1)
    elif direction == LEFT:
        snake[0] = (old_head_x-1, old_head_y)
    elif direction == RIGHT:
        snake[0] = (old_head_x+1, old_head_y)

def spawn_food():
    stage[random.randint(0,S_HEIGHT-1)][random.randint(0,S_WIDTH-1)] = FOOD

def check_collision():
    if (snake[0] in snake[1:len(snake)] or new_head_x < 0 or 
        new_head_x >= S_WIDTH or new_head_y < 0 or new_head_y >= S_HEIGHT):
        return True
    else:
        return False

HEIGHT = 480
WIDTH = 640
S_HEIGHT = 480//10
S_WIDTH = 640//10

UP = 0
DOWN = 1
LEFT = 3
RIGHT = 4
BLANK = 0
FOOD = 1
WALL = 2

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
snake = [(S_WIDTH//2, S_HEIGHT//2)]
direction = LEFT

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
                pygame.draw.rect(screen, (0,255,0), (i*10,j*10,10,10), 0)

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_UP:
                if direction != DOWN:
                    direction = UP
            elif event.key == pygame.K_DOWN:
                if direction != UP:
                    direction = DOWN
            elif event.key == pygame.K_LEFT:
                if direction != RIGHT:
                    direction = LEFT
            elif event.key == pygame.K_RIGHT:
                if direction != LEFT:
                    direction = RIGHT

    # storing positions
    (old_head_x, old_head_y) = snake[0]
    (old_tail_x, old_tail_y) = snake[len(snake)-1]
    
    # move snake
    snake = rotate(snake,1)
    move_head(snake, direction)
    (new_head_x, new_head_y) = snake[0]
    
    if (check_collision()):
        break

    # eating food
    if stage[new_head_y][new_head_x] == FOOD:
        snake.append((old_tail_x,old_tail_y))
        stage[new_head_y][new_head_x] = BLANK
        spawn_food()

    for place, (x, y) in enumerate(snake):
        pygame.draw.rect(screen, (0,0,0), (x*10,y*10,10,10), 0)
             
    # Print framerate and playtime in titlebar.
    text = "Score: " + str(len(snake)) + "   FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("Your score is " + str(len(snake)))