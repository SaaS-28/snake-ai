# main.py
import pygame, random, sys
from pygame.math import Vector2
from settings import *
from snake import SNAKE
from fruit import FRUIT
from AI import AI  # Importa la classe AI

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_font = pygame.font.Font('Python\snake\Font\PoetsenOne-Regular.ttf', 25)
        self.apple = pygame.image.load('Python/snake/Images/apple.png').convert_alpha()
        self.ai = AI()  # Crea un'istanza della classe AI

        # List to store training data
        self.training_data = []

    # Function that calculate every possible action needed to eat the fruit, then chooses the best
    def generate_training_data(self):
        fruit_position = self.fruit.pos  # Get the location of the fruit
        game_state = [1 if self.snake.direction == Vector2(x, y) else 0 for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
        game_state.extend([1 if self.snake.body[0] + self.snake.direction == self.fruit.pos else 0])

        # Add other game status details only if needed to reach a size of 11
        while len(game_state) < 11:
            # Length of snake relative to fruit position
            game_state.append(1 if len(self.snake.body) > len(self.snake.get_path_to_fruit(fruit_position)) else 0)
            # Distance X between the head of the snake and the fruit
            game_state.append(self.fruit.pos.x - self.snake.body[0].x)
            # Y distance between the head of the snake and the fruit
            game_state.append(self.fruit.pos.y - self.snake.body[0].y)

        correct_action = self.get_correct_action()

        # "One-hot" encoding for correct action
        target = [0, 0, 0, 0]
        target[correct_action] = 1

        # Training data
        self.training_data.append((game_state, target))

    # Function that permits to get the best action
    def get_correct_action(self):
        # Determines the correct action based on the current state of the game
        possible_actions = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]
        valid_actions = [action for action in possible_actions if
                         (self.snake.direction + action != Vector2(0, 0)) and
                         (self.snake.direction * -1 != action)]
        return random.choice(range(len(valid_actions)))

    # Function that updates the entire game every cicle (While true)
    def update(self):
        self.snake.move_snake() # Moves the snake
        self.check_collision() # Check for possible collisions
        self.check_fail() # Checks for possible fails
        self.generate_training_data() # Update training data

    # Function that updates the direction of the snake
    def update_direction_based_on_path(self):
        start = (int(self.snake.body[0].x), int(self.snake.body[0].y)) # Snake head
        target = (int(self.fruit.pos.x), int(self.fruit.pos.y)) # Fruit
        obstacles = {(int(block.x), int(block.y)) for block in self.snake.body[1:]} # Walls (no head)
        
        path = self.snake.bfs_path(start, target, obstacles, cell_number) # Chooses the shortest path to reach the fruit
        if path and len(path) > 1:
            next_step = path[1]
            new_direction = Vector2(next_step[0] - start[0], next_step[1] - start[1])
            self.snake.direction = new_direction

    # Function that checks for collisions
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize() # Change the position of the fruit
            self.snake.add_block() # Adds a block at the snake
            self.snake.play_crunch_sound()

            # Avoiding the fruit spawns on the snake - really small chance
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    # Function that checks if the snake hit the wall or himself
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            # print("Wall")

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                # print("Myself")

    # Function that restart the game if the snake hits himself or the wall
    def game_over(self):
        self.snake.reset()

    # Function that draws the soil pattern
    def draw_grass(self):
        grass_color = (167, 209, 61)

        # Draws the grass pattern
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    # Function that generate and handles the score
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3) # Initial lenght of the score
        score_surface = self.game_font.render(score_text, True, (56, 74, 12)) # Renders the score
        score_x = int(cell_size * cell_number - 60) # X coordinate for the score
        score_y = int(cell_size * cell_number - 40) # Y coordinate for the score
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = self.apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    # Function that permits to draw all the things
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

# Main function that includes the major functions
def main():
    pygame.mixer.pre_init(44100, -16, 2, 512) # This is used for pre-load the sound
    pygame.init() # Starts all the modules of pygame
    clock = pygame.time.Clock() # Defines how many times the loop can run per second

    SCREEN_UPDATE = pygame.USEREVENT # Defines an event
    pygame.time.set_timer(SCREEN_UPDATE, 150) # Defines how many times (150 ms) the event should be displayed

    main_game = MAIN()
    ai = AI()

    # Infinite game loop
    while True:
        # Getting the current state of the game
        game_state = [
            1 if main_game.snake.direction == Vector2(x, y) else 0
            for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]
        ]
        game_state.extend([1 if main_game.snake.body[0] + main_game.snake.direction == main_game.fruit.pos else 0])

        ai_action = ai.get_action(game_state) # Get the action from AI

        main_game.snake.direction = ai_action # Moves the snake based on the AI action

        main_game.update_direction_based_on_path() # Update snake direction based on path to fruit

        # Checking every possible events
        for event in pygame.event.get():
            # End the game if the user closes the windows
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Moves the snake every time the timer restart
            if event.type == SCREEN_UPDATE:
                main_game.update()

        screen.fill((175, 215, 70)) # Defines the color of the screen
        main_game.draw_elements()

        pygame.display.update() # Draw all our elements
        clock.tick(60) # 60 fps

if __name__ == "__main__":
    main()
