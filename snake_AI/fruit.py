import pygame, random
from pygame.math import Vector2
from settings import *

class FRUIT:
    def __init__(self):
        self.randomize()
        self.apple = pygame.image.load('Python/snake/Images/apple.png').convert_alpha()
    
    # Funtion that permit to draw the fruit
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) # Creating the rectangle
        screen.blit(self.apple, fruit_rect) # Draws the images
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    # Function that randomize the spawn of the apple in the "map"
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y) # Stores the coordinates in a vector, which is used for determinate position
