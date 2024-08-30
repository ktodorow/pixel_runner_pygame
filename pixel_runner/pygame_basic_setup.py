import pygame
from sys import exit

#basic pygame setup

pygame.init() # start pygame
screen = pygame.display.set_mode((680, 680)) # set screen size
pygame.display.set_caption("test_game") # set game title
clock = pygame.time.Clock() #defining clock for the framerate 

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # QUIT attribute to check if X is pressed.
            pygame.quit() # quits after X on the window is pressed.
            exit() # breaking the while loop (using sys module)

    #draw elements here
    
    pygame.display.update()
    clock.tick(60) # while loop should not run faster than 60 times per sec