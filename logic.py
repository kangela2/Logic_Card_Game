import copy
import random
import pygame

pygame.init()

# Logic Variables
cards = [2, 2,
         3, 3, 
         4, 4, 
         5, 5,
         6, 6, 
         7, 7, 
         8, 8,
         9, 9,
         10, 10,
         11, 11,
         12, 12,
         13, 13]

# Logic Classes
class Card:
    def __init__(self, value, card_type='horizontal'):
        self.value = value
        self.flipped = False
        self.card_type = card_type

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def display_hand(self):
        print(self.name)
        for x in self.hand:
            print(x.value)

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.value)

    def draw_cards(self, screen, start_x, start_y):
        card_width = 50
        card_height = 70
        spacing = 10

        for i, card in enumerate(self.hand):
            if card.card_type == 'horizontal':
                x = start_x + i * (card_width + spacing)
                y = start_y
            else:  # vertical
                x = start_x
                y = start_y + i * (card_height + spacing)
            
            pygame.draw.rect(screen, 'white', (x, y, card_width, card_height))
            value_text = font.render(str(card.value), True, 'black')
            screen.blit(value_text, (x + 10, y + 10))

class Game:
    def __init__(self, name):
        self.name = name
        self.players = []

    def simulate_game(self):
        return True
    
    def deal_cards(self, card_list: list[int]):
        deck = copy.deepcopy(card_list)
        num_players = len(self.players)
        cards_per_player = 6

        for _ in range(cards_per_player):
            for p in self.players:
                if len(deck) > 0:
                    card_index = random.randint(0, len(deck) - 1)
                    card_element = deck.pop(card_index)
                    if p.name in ['Bot 1', 'Bot 2']:
                        p.hand.append(Card(card_element, card_type='vertical'))
                    else:
                        p.hand.append(Card(card_element))

    def start_game(self):
        return True
    
# Running PyGame
screen = pygame.display.set_mode([850, 850])
font = pygame.font.Font('freesansbold.ttf', 30)

active = True
game_started = False  # Flag to indicate if the game has started
run = True
while run:
    # PyGame Display Settings
    pygame.time.Clock().tick(60)
    pygame.display.set_caption('Logic')
    screen.fill('limegreen')

    # If Quit pressed, Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if active:
        # Start Button
        pos = [360, 400, 130, 50]
        start = pygame.draw.rect(screen, 'red', pos, 0, 5)
        pygame.draw.rect(screen, 'green', pos, 5, 5)
        start_text = font.render('START', True, 'black')
        screen.blit(start_text, (pos[0] + 16, pos[1] + 14))

        if event.type == pygame.MOUSEBUTTONUP and start.collidepoint(event.pos):
            active = False
            game_started = True

    if game_started: # Initialize Players and Deal Cards
        New_Game = Game('New Game')
        New_Game.players.append(Player('User'))
        New_Game.players.append(Player('Partner'))
        New_Game.players.append(Player('Bot 1'))
        New_Game.players.append(Player('Bot 2'))

        New_Game.deal_cards(cards)

        for player in New_Game.players:
            player.sort_hand()  # Sort the player's hand
            player.display_hand()

        game_started = False  # Set to False to avoid redealing and printing

    if not active:
        # Draw cards for each player
        New_Game.players[0].draw_cards(screen, 100, 700)   # User
        New_Game.players[1].draw_cards(screen, 100, 100)  # Partner
        New_Game.players[2].draw_cards(screen, 50, 200)  # Bot 1
        New_Game.players[3].draw_cards(screen, 500, 200) # Bot 2

    pygame.display.flip()
pygame.quit()
