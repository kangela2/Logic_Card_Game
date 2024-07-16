import copy
import random
import pygame

# game variables
WIDTH = 1200
HEIGHT = 1200
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Logic')
fps = 60
timer = pygame.time.Clock()

# Define the size of each rectangle
rect_width = 100
rect_height = 150

# Define the space between rectangles
space = 20

# Define the colors
colors = ['blue', 'red', 'green', 'pink', 'yellow', 'cyan', 'magenta']

# Save the colors for each rectangle at the start
num_cards = 24
rect_colors = [random.choice(colors) for _ in range(num_cards)]

def draw_game():
    # Positions for top row
    top_row_y = 20
    for i in range(6):
        x = 200 + (rect_width + space) * i
        pygame.draw.rect(screen, rect_colors[i], [x, top_row_y, rect_width, rect_height])
    
    # Positions for bottom row
    bottom_row_y = 1100 - rect_height - 20
    for i in range(6, 12):
        x = 200 + (rect_width + space) * (i - 6)
        pygame.draw.rect(screen, rect_colors[i], [x, bottom_row_y, rect_width, rect_height])
    
    # Positions for left column (flipped dimensions)
    left_col_x = 50
    for i in range(12, 18):
        y = top_row_y + rect_height + space + (rect_width + space) * (i - 12)
        pygame.draw.rect(screen, rect_colors[i], [left_col_x, y, rect_height, rect_width])
    
    # Positions for right column (flipped dimensions)
    right_col_x = 1100 - rect_height - 50
    for i in range(18, 24):
        y = top_row_y + rect_height + space + (rect_width + space) * (i - 18)
        pygame.draw.rect(screen, rect_colors[i], [right_col_x, y, rect_height, rect_width])



# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('white')
    draw_game()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
