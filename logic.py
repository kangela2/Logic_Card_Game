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

# Define the size of each card
card_width = 75
card_height = 105

# Define the space between card
space = 20

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    
#    print(current_hand, current_deck)
    
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, x, y, vertical):
    for i in range(len(player)):
        if not vertical:
            x = 150 + (card_width + space) * i
            w = card_width
            h = card_height
        else:
            y = 150 + (card_width + space) * i
            w = card_height
            h = card_width
        
        pygame.draw.rect(screen, 'red', [x, y, w, h])
        screen.blit(font.render(player[i], True, 'black'), (x + 10, y + 10))


def draw_game(act):
    button_list = []
    # initially on startup (not active) only option is to start game
    if not active:
        title_text = title_font.render('LOGIC', True, 'black')
        screen.blit(title_text, (300, 100))
        
        start = pygame.draw.rect(screen, 'red', [360, 400, 130, 50], 0, 5)
        pygame.draw.rect(screen, 'green', [360, 400, 130, 50], 3, 5)
        start_text = font.render('START', True, 'black')
        screen.blit(start_text, (376, 414))
        button_list.append(start)
        
    # once game started, show game board and user action options
#    else:

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
            
        # prints every player's hand
#        print(player_hand, teammate_hand, left_oppenent_hand, right_opponent_hand)
        
        initial_deal = False
    
    # once game is started, and cards are dealt, display board
    if active:
        draw_cards(player_hand, 150, WIDTH - space - card_height, False)
        draw_cards(teammate_hand, 150, 20, False)
        draw_cards(left_oppenent_hand, 20, 150, True)
        draw_cards(right_opponent_hand, WIDTH - space - card_height, 150, True)

    
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
