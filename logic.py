import copy
import random
import pygame

pygame.init()

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
one_deck = 2 * cards
WIDTH = 850
HEIGHT = 850
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Logic')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)
title_font = pygame.font.Font('freesansbold.ttf', 80)
log_font = pygame.font.Font('freesansbold.ttf', 18)
active = False
initial_deal = False
game_deck = one_deck
players = []

# Define the size of each card
card_width = 75
card_height = 105

# Define the space between card
space = 20
edge_length = 150

# Define game log variables
log_pos = 175
log_width = 500
log_height = 320
log = []
visible_log = []

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    def set_partner(self, player):
        self.partner = player
        
def initialize_players():
    # adds player 1 // user // bottom hand to list of players
    players.append(Player("A"))
    
    # adds player 2 // opponent // left hand to list of players
    players.append(Player("B"))
    
    # adds player 3 // user's partner // top hand to list of players
    players.append(Player("C"))
    
    # adds player 4 // opponent's partner // right hand to list of players
    players.append(Player("D"))
    
    
    # set user's partner as player 3
    players[0].set_partner(players[2])
    
    # set opponent's partner as player 4
    players[2].set_partner(players[0])
    
    # set player 2's partner as user
    players[1].set_partner(players[3])
    
    # set player 4's partner as opponent
    players[3].set_partner(players[1])

# get key of card based on rank
def card_key(card):
    return rank_order[card]

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
        
#    print(current_hand, current_deck)
    
    return current_hand, current_deck

# draw cards visually onto screen depending on hand, x and y starting positions, whether or not they're displayed vertically, and what order the ranks should be displayed
def draw_cards(hand, x, y, vertical, order):

    for i in range(len(hand)):
        if not vertical:
            x = 150 + (card_width + space) * i
            w = card_width
            h = card_height
        else:
            y = 150 + (card_width + space) * i
            w = card_height
            h = card_width
        
        # white card
        pygame.draw.rect(screen, 'white', [x, y, w, h], 0, 5)
        
        # rank
        if order:
            screen.blit(font.render(hand[i], True, 'black'), (x + 10, y + 10))
        else:
            screen.blit(font.render(hand[5 - i], True, 'black'), (x + 10, y + 10))
        
        # black border
        pygame.draw.rect(screen, 'black', [x, y, w, h], 5, 5)
        
        
# appends turns to the logs
def add_turn(log, turn, v_log, max):
    log.append(turn)
    v_log.append(turn)
    
    # makes the 15 most recent turns visible in the log
    if max > 15:
        v_log.pop(0)
        
    return log, v_log

# draws turns stored in log
def draw_log(log):
    
    # sets y position for turns to be displayed
    y = log_pos + log_height - 30
    
    for turn in reversed(log):
        text = log_font.render(turn, True, 'black')
        screen.blit(text, (log_pos + 10, y))
        y -= 20

# draws game elements depending on scene
def draw_game(act):
    button_list = []
    
    # initially on startup (not active) only option is to start game
    if not active:
        title_text = title_font.render('LOGIC', True, 'black')
        screen.blit(title_text, (300, 100))
        
        start = pygame.draw.rect(screen, 'red', [360, 400, 130, 50], 0, 5)
        pygame.draw.rect(screen, 'green', [360, 400, 130, 50], 5, 5)
        start_text = font.render('START', True, 'black')
        screen.blit(start_text, (376, 414))
        button_list.append(start)
        
    # once game started, show game board and user action options
    else:
        # displays log window
        pygame.draw.rect(screen, 'white', [log_pos, log_pos, log_width, log_height], 0, 5)
        pygame.draw.rect(screen, 'black', [log_pos, log_pos, log_width, log_height], 5, 5)

    return button_list


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('limegreen')
    
    # deal cards to players
    if initial_deal:
        for i in range(6):
            for x in players:
                x.hand, game_deck = deal_cards(x.hand, game_deck)
        
        initial_deal = False
        
        # sort hands after they're all dealt
        for x in players:
            x.hand = sorted(x.hand, key = card_key)
        
        # prints every player's hand
#        for i in players:
#            print(f"{i.hand} : {i.name}")
    
    # once game is started, and cards are dealt, display board
    if active:
        # draws user's hand at the bottom of the board
        draw_cards(players[0].hand, edge_length, WIDTH - space - card_height, False, True)
        
        # draws opponent's hand on the left side of the board
        draw_cards(players[2].hand, edge_length, space, False, False)
        
        # draws user's partner's hand at the top of the board
        draw_cards(players[1].hand, space, edge_length, True, True)
        
        # draws opponent's partner's hand on the right side of the board
        draw_cards(players[3].hand, WIDTH - space - card_height, edge_length, True, False)
    
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
                    initialize_players()
                
        # placeholder functionality to test log
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                turn_number = len(log) + 1
                
                add_turn(log, f"Turn {turn_number}: [{players[0].name}] viewed [{players[0].partner.name}]'s card and guessed [{players[1].name}]'s card.", visible_log, turn_number)


    draw_log(visible_log)

    pygame.display.flip()
pygame.quit()
