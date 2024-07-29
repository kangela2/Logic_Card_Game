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
    def __init__(self, value):
        self.value = value
        self.flipped = False
  
class Player:
    def __init__(self, name, type):
        self.name = name
        self.hand = []
        self.type = type

    def display_hand(self):
        print(self.name)
        for x in self.hand:
            print(x.value)

    def draw_cards(self, position):

        if self.type == 'user':
            pygame.draw.rect(screen, 'white', [150 + 75, 75, 100, 75], 0, 5)

        return True

class Game:
    def __init__(self, name):
        self.name = name
        self.players = []

    def simulate_game(self):
        return True
    
    def deal_cards(self, card_list: list[int]):
        deck = copy.deepcopy(card_list)
        num_players = len(self.players)

        for i in range(6):
            for p in self.players:
                if len(deck) > 0:
                    card_index = random.randint(0, len(deck) - 1)
                    card_element = deck.pop(card_index)
                    p.hand.append(Card(card_element))
        
        for p in self.players:
            p.hand.sort(key=lambda card: card.value)

    def start_game(self):
        for p in self.players:
            p.draw_cards(100)
    
# Running PyGame
screen = pygame.display.set_mode([850, 850])
font = pygame.font.Font('freesansbold.ttf', 30)

active = True
dealing = False  # Flag to indicate if the game has started
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
            dealing = True
            
    New_Game = Game('New Game')
    if dealing: # Initialize Players and Deal Cards
        New_Game.players.append(Player('User', 'user'))
        New_Game.players.append(Player('Partner', 'partner'))
        New_Game.players.append(Player('Bot 1', 'bot'))
        New_Game.players.append(Player('Bot 2', 'bot'))

        New_Game.deal_cards(cards)

        for player in New_Game.players:
            player.display_hand()

        dealing = False  # Set to False to avoid redealing and printing

    pygame.display.flip()
pygame.quit()
