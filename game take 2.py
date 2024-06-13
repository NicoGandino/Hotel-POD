import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Dive")

# Load images
background_img = pygame.image.load('background.png')
ingame_img = pygame.image.load('background_800x711.png')
character_img = pygame.image.load('diver.png')
coin_img = pygame.image.load('gold coin.png')
oxygen_img = pygame.image.load('oxygen.png')

original_widthc, original_heightc = character_img.get_size()
original_widthco, original_heightco = coin_img.get_size()
# Define the new size (e.g., half of the original size)
new_widthc = original_widthc // 2
new_heightc = original_heightc // 2
new_widthco = original_widthco // 4
new_heightco = original_heightco // 4

# Scale the image
character_img_new = pygame.transform.scale(character_img, (new_widthc, new_heightc))
coin_img_new = pygame.transform.scale(coin_img, (new_widthco, new_heightco))

# Load font
font = pygame.font.Font('Pixeltype.ttf', 50)

# Game variables
character_pos = [WIDTH // 10, HEIGHT // 10]
character_speed = [0, 0]
gravity = 0.5
coins = []
oxygen_level = 100
gold_coins_count = 0
start_time = pygame.time.get_ticks()

# Colors
WHITE = (255, 255, 255)

# Function to draw the initial start screen
def draw_start_screen():
    screen.blit(background_img, (0, 0))
    title_text = font.render("Treasure Dive", True, (255, 255,255))
    start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Function to draw the main game screen
def draw_game_screen():
    global ingame_img, character_img_new, coin_img_new, oxygen_img
    screen.blit(ingame_img, (0, 0))
    screen.blit(character_img_new, character_pos)
    for coin in coins:
        screen.blit(coin_img_new, coin)
    draw_hud()
    pygame.display.flip()

# Function to draw the HUD
def draw_hud():
    global oxygen_level, gold_coins_count, start_time
    time_elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {time_elapsed}", True, (255, 255,255))
    oxygen_text = font.render(f"Oxygen: {int(oxygen_level)}", True, (255, 255,255))
    coins_text = font.render(f"Coins: {gold_coins_count}", True, (255, 255,255))
    screen.blit(time_text, (10, 10))
    screen.blit(oxygen_text, (10, 40))
    screen.blit(coins_text, (10, 70))

# Function to update the character position and check collisions
def update_character():
    global character_pos, character_speed, oxygen_level, gold_coins_count
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_speed[0] = -5
    elif keys[pygame.K_RIGHT]:
        character_speed[0] = 5
    else:
        character_speed[0] = 0

    if keys[pygame.K_UP]:
        character_speed[1] = -5
    elif keys[pygame.K_DOWN]:
        character_speed[1] = 5
    else:
        character_speed[1] += gravity

    character_pos[0] += character_speed[0]
    character_pos[1] += character_speed[1]

    # Boundary check
    if character_pos[0] < 0:
        character_pos[0] = 0
    elif character_pos[0] > WIDTH - character_img_new.get_width():
        character_pos[0] = WIDTH - character_img_new.get_width()
    
    if character_pos[1] < 0:
        character_pos[1] = 0
    elif character_pos[1] > HEIGHT - character_img_new.get_height():
        character_pos[1] = HEIGHT - character_img_new.get_height()
    
    # Collision detection with coins
    for coin in coins[:]:
        if pygame.Rect(character_pos[0], character_pos[1], character_img_new.get_width(), character_img_new.get_height()).colliderect(
            pygame.Rect(coin[0], coin[1], coin_img_new.get_width(), coin_img_new.get_height())):
            coins.remove(coin)
            gold_coins_count += 1

    # Oxygen depletion
    oxygen_level -= 0.05
    if oxygen_level <= 0:
        game_over()

# Function to spawn coins
def spawn_coins():
    if random.randint(1, 100) > 98:
        coin_x = random.randint(0, WIDTH - coin_img_new.get_width())
        coin_y = random.randint(0, HEIGHT - coin_img_new.get_height())
        coins.append([coin_x, coin_y])

# Game over function
def game_over():
    global running
    running = False

# Main loop
running = True
in_start_screen = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if in_start_screen and event.key == pygame.K_SPACE:
                in_start_screen = False
                start_time = pygame.time.get_ticks()
    
    if in_start_screen:
        draw_start_screen()
    else:
        spawn_coins()
        update_character()
        draw_game_screen()
    
    pygame.time.delay(30)

pygame.quit()
sys.exit()