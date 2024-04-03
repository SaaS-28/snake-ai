import pygame, collections
from pygame.math import Vector2
from settings import *

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # Body of the snake
        self.direction = Vector2(0, 0) # Initial direction is 0 so the snake doesn't move
        self.new_block = False # This is used for snake elongation

        self.head_up = pygame.image.load('Python/snake/Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Python/snake/Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Python/snake/Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Python/snake/Images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Python/snake/Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Python/snake/Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Python/snake/Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Python/snake/Images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Python/snake/Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Python/snake/Images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Python/snake/Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Python/snake/Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Python/snake/Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Python/snake/Images/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Python\snake\Sound\crunch.wav')

    # Function that find a path from the starting position to the destination in a rectangular grid, avoiding obstacles, using the search algorithm in width (BFS). 
    # If it finds a valid path, it returns a list of coordinates representing the path. If it does not find any valid path, it returns an empty list.
    def bfs_path(self, start, target, obstacles, cell_number):
        queue = collections.deque([[start]])
        seen = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if Vector2(x, y) == target:
                return path
            for x2, y2 in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= x2 < cell_number and 0 <= y2 < cell_number and (x2, y2) not in obstacles and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
                    obstacles.add((x2, y2))
        return []

    # Function that calculate the direction in which the snake must move to reach the position of the fruit on the grid
    def get_path_to_fruit(self, fruit_position):
        path = []
        snake_head = self.body[0]
        
        # Calculate the direction to be taken on the X axis
        if snake_head.x < fruit_position.x:
            path.append("right")
        elif snake_head.x > fruit_position.x:
            path.append("left")
            
        # Calculate the direction to be taken on the Y axis
        if snake_head.y < fruit_position.y:
            path.append("down")
        elif snake_head.y > fruit_position.y:
            path.append("up")
        
        return path

    # Function that draws the snake
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size) # Create the snake

            # Adding graphic to the snake and seeing where the snake is facing so we can add the correct head, tail, middle and corners
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    # Function that update the head of the snake based on which direction he is facing
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    # Function that update the tail of the snake based on which direction he is facing
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    # Function that adds a block to the snake (or not depending on if he ate the fruit)
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] # Copy the entire body vector so the snake can expand himself
            self.new_block = False
        else:
            body_copy = self.body[:-1] # Copy the body vector except for the last block that need to be eliminated for animation

        body_copy.insert(0, body_copy[0] + self.direction) # Insert the head of the snake for the animation
        self.body = body_copy[:] # Return to the initial situation

    # Function that set the new_block variable to true so the snake can extend
    def add_block(self):
        self.new_block = True

    # Function that plays the sound (apple eaten)
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Function that reset the position of the snake. This is used when the game over on the main class is triggered
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)