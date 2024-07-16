import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
width, height = 800, 600
frame_margin = 50
frame_width = width - 2 * frame_margin
frame_height = height - 2 * frame_margin
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
background_color = (173, 204, 96) # Retro Green
snake_color = (34, 139, 34)
rat_color = (128, 128, 128)  # Grey
frame_color = (0, 0, 0)
text_color = (255, 255, 255)

# Load sounds
eat_sound = pygame.mixer.Sound(r" ") #copy the path of eat sound
out_of_bound_sound = pygame.mixer.Sound(r" ") # copy the path of the sound file when snake goes out of frame

# Game variables
block_size = 20
initial_speed = 15
speed_increment = 1
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 35)

# High score handling
def get_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def set_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = get_high_score()

# Placeholder for snake head as a pentagon
def draw_snake_head(head_pos):
    pygame.draw.polygon(win, snake_color, [
        (head_pos[0] + block_size // 2, head_pos[1]),  # Top point
        (head_pos[0], head_pos[1] + block_size // 3),  # Bottom-left
        (head_pos[0] + block_size // 4, head_pos[1] + block_size),  # Bottom-middle-left
        (head_pos[0] + 3 * block_size // 4, head_pos[1] + block_size),  # Bottom-middle-right
        (head_pos[0] + block_size, head_pos[1] + block_size // 3)  # Bottom-right
    ])

# Draw the background as green
def draw_background():
    win.fill(background_color)

# Draw the snake with rounded corners for body segments
def draw_snake(snake_list):
    for segment in snake_list[:-1]:
        pygame.draw.rect(win, snake_color, [segment[0], segment[1], block_size, block_size], border_radius=5)
    draw_snake_head(snake_list[-1])

# Draw the rat as a circle
def draw_rat(rat_pos):
    pygame.draw.circle(win, rat_color, rat_pos, block_size // 2)

# Draw the game frame
def draw_frame():
    pygame.draw.rect(win, frame_color, [frame_margin, frame_margin, frame_width, frame_height], 3)

# Display a message on the screen
def display_message(msg, color, position):
    message = font.render(msg, True, color)
    win.blit(message, position)

def game_loop():
    global high_score
    
    game_over = False
    game_close = False

    x, y = width // 2, height // 2
    x_change, y_change = 0, 0
    snake_list = []
    length_of_snake = 1

    rat_x = round(random.randrange(frame_margin, frame_margin + frame_width - block_size) / block_size) * block_size
    rat_y = round(random.randrange(frame_margin, frame_margin + frame_height - block_size) / block_size) * block_size

    current_score = 0
    speed = initial_speed

    while not game_over:

        while game_close:
            draw_background()
            draw_frame()
            display_message("You Lost! Press Shift to Restart or Q to Quit", text_color, [width // 6, height // 3])
            display_message(f"Score: {current_score}", text_color, [width // 2.5, height // 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block_size
                    x_change = 0
                elif event.key == pygame.K_SPACE and x_change == 0 and y_change == 0:
                    x_change = block_size
                    y_change = 0

        if x >= frame_margin + frame_width or x < frame_margin or y >= frame_margin + frame_height or y < frame_margin:
            out_of_bound_sound.play()
            game_close = True

        x += x_change
        y += y_change

        draw_background()
        draw_frame()
        draw_rat([rat_x + block_size // 2, rat_y + block_size // 2])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_message("Snake Game", text_color, [width // 2.5, 10])
        display_message(f"Score: {current_score}", text_color, [10, height - 40])
        display_message(f"High Score: {high_score}", text_color, [width - 200, height - 40])

        pygame.display.update()

        if x == rat_x and y == rat_y:
            eat_sound.play()
            rat_x = round(random.randrange(frame_margin, frame_margin + frame_width - block_size) / block_size) * block_size
            rat_y = round(random.randrange(frame_margin, frame_margin + frame_height - block_size) / block_size) * block_size
            length_of_snake += 1
            current_score += 1
            speed += speed_increment
            if current_score > high_score:
                high_score = current_score
                set_high_score(high_score)

        clock.tick(speed)

    pygame.quit()
    sys.exit()

try:
    game_loop()
except Exception as e:
    print(f"An error occurred: {e}")
    pygame.quit()
    sys.exit()
