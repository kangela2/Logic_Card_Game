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

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    def add_partner(self, player):
        self.partner = player

# Custom sort function
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
        
def draw_log(player, turn):
        log_text = log_font.render(f'Turn {turn + 1}: [{player.name}] viewed [{player.partner.name}]\'s card', True, 'black')
        screen.blit(log_text, (185, 185 + 20 * turn))


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
        log = pygame.draw.rect(screen, 'white', [175, 175, 500, 300], 0, 5)
        pygame.draw.rect(screen, 'black', [175, 175, 500, 300], 5, 5)
        
        for i in range(6):
            draw_log(player1, i)
        

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
        draw_cards(player1.hand, edge_length, WIDTH - space - card_height, False, True)
        draw_cards(player3.hand, edge_length, space, False, False)
        draw_cards(player2.hand, space, edge_length, True, True)
        draw_cards(player4.hand, WIDTH - space - card_height, edge_length, True, False)
    
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
                    player1 = Player('bottom')
                    player2 = Player('left')
                    player3 = Player('top')
                    player4 = Player('right')
                    player1.add_partner(player3)
                    player2.add_partner(player4)
                    player3.add_partner(player1)
                    player4.add_partner(player2)
                    players.append(player1)
                    players.append(player2)
                    players.append(player3)
                    players.append(player4)

    pygame.display.flip()
pygame.quit()
