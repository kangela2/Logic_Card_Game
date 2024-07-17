import copy
import random
import pygame

pygame.init()

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
one_deck = 2 * cards
WIDTH = 850
HEIGHT = 850
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Logic')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)
title_font = pygame.font.Font('freesansbold.ttf', 80)
active = False
initial_deal = False
game_deck = one_deck
player_hand = []
teammate_hand = []
left_oppenent_hand = []
right_opponent_hand = []

# Define the size of each rectangle
rect_width = 75
rect_height = 105

# Define the space between rectangles
space = 20

# Define the colors
colors = ['blue', 'red', 'green', 'pink', 'yellow', 'cyan', 'magenta']

# Save the colors for each rectangle at the start
num_cards = 24
rect_colors = [random.choice(colors) for _ in range(num_cards)]

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    
    print(current_hand, current_deck)
    
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, teammate, left, right):
    for i in range(len(player)):
        
        # Positions for bottom row - player's hand
        bottom_row_y = 850 - rect_height - 20
        
        x = 150 + (rect_width + space) * i
        
        pygame.draw.rect(screen, 'red', [x, bottom_row_y, rect_width, rect_height])
        screen.blit(font.render(player[i], True, 'black'), (x + 10, bottom_row_y - 20))


def draw_game(act):
    button_list = []
    # initially on startup (not active) only option is to start game
    if not active:
        start = pygame.draw.rect(screen, 'red', [360, 400, 130, 50], 0, 5)
        pygame.draw.rect(screen, 'green', [360, 400, 130, 50], 3, 5)
        start_text = font.render('START', True, 'black')
        screen.blit(start_text, (376, 414))
        button_list.append(start)
        
#        title = pygame.draw.rect(screen, 'red', [360, 400, 130, 50], 0, 5)
#        pygame.draw.rect(screen, 'green', [360, 400, 130, 50], 3, 5)
        title_text = title_font.render('LOGIC', True, 'black')
        screen.blit(title_text, (300, 100))

        
    # once game started, show game board and user action options
    else:
        # Positions for top row - teammate's hand
        top_row_y = 20
        for i in range(6):
            x = 150 + (rect_width + space) * i
            pygame.draw.rect(screen, rect_colors[i], [x, top_row_y, rect_width, rect_height])
        
        # Positions for bottom row - player's hand
        bottom_row_y = 850 - rect_height - 20
        for i in range(6, 12):
            x = 150 + (rect_width + space) * (i - 6)
            pygame.draw.rect(screen, rect_colors[i], [x, bottom_row_y, rect_width, rect_height])
        
        # Positions for left column (flipped dimensions) - left opponent's hand
        left_col_x = 20
        for i in range(12, 18):
            y = 25 + rect_height + space + (rect_width + space) * (i - 12)
            pygame.draw.rect(screen, rect_colors[i], [left_col_x, y, rect_height, rect_width])
        
        # Positions for right column (flipped dimensions) - right opponent's hand
        right_col_x = 850 - rect_height - 20
        for i in range(18, 24):
            y = 25 + rect_height + space + (rect_width + space) * (i - 18)
            pygame.draw.rect(screen, rect_colors[i], [right_col_x, y, rect_height, rect_width])
    return button_list


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('white')
    
    # deal cards to players
    if initial_deal:
        for i in range(6):
            player_hand, game_deck = deal_cards(player_hand, game_deck)
            left_oppenent_hand, game_deck = deal_cards(left_oppenent_hand, game_deck)
            teammate_hand, game_deck = deal_cards(teammate_hand, game_deck)
            right_opponent_hand, game_deck = deal_cards(right_opponent_hand, game_deck)
            
        print(player_hand, teammate_hand, left_oppenent_hand, right_opponent_hand)
        
        initial_deal = False
    
    # once game is started, and cards are dealt, display board
    if active:
        draw_cards(player_hand, teammate_hand, left_oppenent_hand, right_opponent_hand)
    
    buttons = draw_game(active)
    
    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(one_deck)
                    player_hand = []
                    teammate_hand = []
                    left_oppenent_hand = []
                    right_opponent_hand = []
                    
        
    pygame.display.flip()
pygame.quit()
