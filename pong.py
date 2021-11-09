import pygame

class player(x, y):

# dimensions in pixels
HEIGHT = 480
WIDTH = 640

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

while mainloop:
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    # Update Pygame display.
    pygame.display.flip()

pygame.quit()
