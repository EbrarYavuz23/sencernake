import json 
import os
import random
import time
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_1, K_2, K_3, K_4, K_5, K_RETURN

SCREEN_SIZE = 800
BLOCK_WIDTH = 40

menu_items = ["Start Game", "Credits", "Quit"]
selected_index = 0

# Title Image With My Friends
title_img = pygame.image.load("resources/title.png")  

def draw_menu():
    game.surface.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 36)

    # Title Image Area
    img_rect = title_img.get_rect(center=(SCREEN_SIZE // 2, 120))
    game.surface.blit(title_img, img_rect)

    for i, item in enumerate(menu_items):
        color = (255, 255, 0) if i == selected_index else (255, 255, 255)
        label = font.render(item, True, color)
        label_rect = label.get_rect(center=(SCREEN_SIZE // 2, 220 + i * 50))
        game.surface.blit(label, label_rect)

    pygame.display.update()


def show_credits():
    game.surface.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 28)
    lines = [
        "Snake - Sencer",
        "Apple 1 - Mehmet",
        "Apple 2 - Ebrar",
        "Toxic Apple :D - Furkan",
        "",
        "Thanks my friends, thanks my life. Enjoy :D"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_SIZE // 2, 150 + i * 40))
        game.surface.blit(text, text_rect)

    font_small = pygame.font.SysFont("arial", 20)
    hint = font_small.render("Press ENTER to return", True, (180, 180, 180))
    hint_rect = hint.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE - 60))
    game.surface.blit(hint, hint_rect)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def show_menu():
    global selected_index
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    selected = menu_items[selected_index]
                    if selected == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif selected == "Start Game":
                        return
                    elif selected == "Credits":
                        show_credits()


class Snake:
    def __init__(self, parent_screen, length=5):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/sencer.png")
        self.x = [BLOCK_WIDTH] * self.length
        self.y = [BLOCK_WIDTH] * self.length
        self.direction = "right"

    def draw(self):
        # We don't fill the screen with black here anymore
        # The Game class will handle drawing the grass background
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def increase(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        
    def decrease(self):
        if self.length > 1:  # Prevent snake from disappearing completely
            self.length -= 1
            self.x.pop()
            self.y.pop()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += BLOCK_WIDTH
        if self.direction == 'left':
            self.x[0] -= BLOCK_WIDTH
        if self.direction == 'up':
            self.y[0] -= BLOCK_WIDTH
        if self.direction == 'down':
            self.y[0] += BLOCK_WIDTH

        if self.x[0] >= SCREEN_SIZE:
            self.x[0] = 0

        if self.x[0] < 0:
            self.x[0] = SCREEN_SIZE

        if self.y[0] >= SCREEN_SIZE:
            self.y[0] = 0

        if self.y[0] < 0:
            self.y[0] = SCREEN_SIZE


class Apple:
    def __init__(self, parent_screen, image_path="resources/mehmet.png"):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load(image_path)
        self.x = BLOCK_WIDTH * 4
        self.y = BLOCK_WIDTH * 5
        self.is_toxic = False
        self.spawn_time = 0

    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))

    def move(self, snake):
        while True:  # make sure new food is not getting created over snake body
            x = random.randint(0, 19) * BLOCK_WIDTH
            y = random.randint(0, 19) * BLOCK_WIDTH
            clean = True
            for i in range(0, snake.length):
                if x == snake.x[i] and y == snake.y[i]:
                    clean = False
                    break
            if clean:
                self.x = x
                self.y = y
                self.spawn_time = time.time()  # Record when the apple was spawned
                return


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game - PyGame")
        self.SCREEN_UPDATE = pygame.USEREVENT
        self.timer = 150
        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)
        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        
        # Load grass texture
        #self.grass_texture = pygame.image.load("resources/grass_texture.png")
        
        # Create grass pattern programmatically
        self.create_grass_pattern()
        
        self.snake = Snake(self.surface, length=5)
        
        # Create all three apple types
        self.apple1 = Apple(parent_screen=self.surface, image_path="resources/mehmet.png")
        self.apple2 = Apple(parent_screen=self.surface, image_path="resources/ebrar.png")
        self.toxic_apple = Apple(parent_screen=self.surface, image_path="resources/furkan.png")
        self.toxic_apple.is_toxic = True
        
        # Set up apple sequence
        self.apple_sequence = [self.apple1, self.apple2, self.toxic_apple]
        self.apple_index = 0
        self.current_apple = self.apple_sequence[self.apple_index]
        
        self.score = 0
        self.record = 0
        self.retrieve_data()
        
    def create_grass_pattern(self):
        # Create a grass pattern surface
        pattern_size = 80
        self.grass_texture = pygame.Surface((pattern_size, pattern_size))
        
        # Base grass color
        base_color = (34, 139, 34)  # Forest green
        
        # Fill with base color
        self.grass_texture.fill(base_color)
        
        # Add some grass blade details
        for _ in range(50):
            x = random.randint(0, pattern_size - 1)
            y = random.randint(0, pattern_size - 1)
            # Vary the green shades
            shade = random.randint(-30, 30)
            grass_color = (
                max(0, min(255, base_color[0] + shade)),
                max(0, min(255, base_color[1] + shade)),
                max(0, min(255, base_color[2] + shade))
            )
            pygame.draw.circle(self.grass_texture, grass_color, (x, y), 1)
        
    def draw_grass_background(self):
        # Fill the screen with black first
        self.surface.fill((0, 0, 0))
        
        # Draw the grass texture tiled across the game area
        for y in range(0, SCREEN_SIZE, self.grass_texture.get_height()):
            for x in range(0, SCREEN_SIZE, self.grass_texture.get_width()):
                self.surface.blit(self.grass_texture, (x, y))

    def play(self):
        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)
    
        # Move the snake first
        self.snake.move()
    
        # Draw the grass background
        self.draw_grass_background()
    
        # Then draw the snake and apple on top
        self.snake.draw()
        self.current_apple.draw()
        self.display_score()

        # Check if toxic apple has been on screen for more than 3 seconds
        if self.current_apple.is_toxic and time.time() - self.current_apple.spawn_time > 3:
            # Move to next apple in sequence
            self.apple_index = (self.apple_index + 1) % len(self.apple_sequence)
            self.current_apple = self.apple_sequence[self.apple_index]
            self.current_apple.move(self.snake)

        # If snake eats the apple
        if self.snake.x[0] == self.current_apple.x and self.snake.y[0] == self.current_apple.y:
            if self.current_apple.is_toxic:
                # Toxic apple gives -1 point and decreases snake length
                self.score -= 1
                self.snake.decrease()
            else:
                # Regular apples give +1 point and increase snake length
                self.score += 1
                self.snake.increase()

            # Move to next apple in sequence
            self.apple_index = (self.apple_index + 1) % len(self.apple_sequence)
            self.current_apple = self.apple_sequence[self.apple_index]
            self.current_apple.move(self.snake)
            
            print(f"Score: {self.score}")

            if self.record < self.score:
                self.record = self.score
                self.save_data()

        

        if self.record < self.score:
            self.record = self.score
            self.save_data()

        # Check if snake collides with itself
        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                print("snake will die")
                raise Exception("Collision Occurred")

    def save_data(self):
        data_folder_path = "./resources"
        file_name = "data.json"
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        complete_path = os.path.join(data_folder_path, file_name)
        data = {'record': self.record}
        with open(complete_path, 'w') as file:
            json.dump(data, file, indent=4)

    def retrieve_data(self):
        data_folder_path = os.path.join("./resources", "data.json")
        if os.path.exists(data_folder_path):
            with open(data_folder_path, 'r') as file:
                data = json.load(file)

            if data is not None:
                self.record = data['record']

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        msg = "Score: " + str(self.score) + " Record: " + str(self.record)
        
        # Create a semi-transparent background for the score text
        text_bg = pygame.Surface((400, 40))
        text_bg.set_alpha(180)  # Semi-transparent
        text_bg.fill((0, 0, 0))
        self.surface.blit(text_bg, (350, 10))
        
        scores = font.render(f"{msg}", True, (200, 200, 200))
        self.surface.blit(scores, (350, 10))

    def show_game_over(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont('arial', 30)
        line = font.render(f"Game over! score is {self.score}", True, (255, 255, 255))
        self.surface.blit(line, (200, 300))
        line1 = font.render(f"Press Enter to Restart", True, (255, 255, 255))
        self.surface.blit(line1, (200, 400))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface)
        
        # Reset all apples
        self.apple1 = Apple(self.surface, image_path="resources/mehmet.png")
        self.apple2 = Apple(self.surface, image_path="resources/ebrar.png")
        self.toxic_apple = Apple(self.surface, image_path="resources/furkan.png")
        self.toxic_apple.is_toxic = True
        
        # Reset apple sequence
        self.apple_sequence = [self.apple1, self.apple2, self.toxic_apple]
        self.apple_index = 0
        self.current_apple = self.apple_sequence[self.apple_index]
        
        self.score = 0

    def run(self):
        running = True
        pause = False
        while running:
            # Handle Events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_1:
                        self.timer = 10
                    if event.key == K_2:
                        self.timer = 50
                    if event.key == K_3:
                        self.timer = 100
                    if event.key == K_4:
                        self.timer = 150
                    if event.key == K_5:
                        self.timer = 200

                    if event.key == K_RETURN:
                        pause = False

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.SCREEN_UPDATE:
                    try:
                        if not pause:
                            self.play()
                    except Exception as e:
                        self.show_game_over()
                        pause = True
                        self.reset()

            # update the display
            pygame.display.update()


# Make sure to import sys at the top of your file
import sys

game = Game()
show_menu()  # Show menu first
game.run()   # Then start the game
