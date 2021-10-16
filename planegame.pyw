
import pygame
import sys
import webbrowser
import os
from tkinter import *
from tkinter import messagebox
# Simple pygame program
cwd = os.getcwd()
print(cwd)
PID = os.getpid()
print(PID)
# Import and initialize the pygame library
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
print(WIDTH,HEIGHT)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
