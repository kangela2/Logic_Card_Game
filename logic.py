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
        card_width = 75
        card_height = 105
        spacing = 20

        for i, card in enumerate(self.hand):
            if card.card_type == 'horizontal':
                x = start_x + i * (card_width + spacing)
                y = start_y
            else:  # vertical
                x = start_x
                y = start_y + i * (card_height + spacing)
            
            pygame.draw.rect(screen, 'white', (x, y, card_width, card_height))
            
            # Only display the value if the card is flipped
            if card.flipped:
                value_text = str(card.value)
                if card.value == 11:
                    value_text = 'J'
                elif card.value == 12:
                    value_text = 'Q'
                elif card.value == 13:
                    value_text = 'K'
                
                value_rendered = font.render(value_text, True, 'black')
                screen.blit(value_rendered, (x + 10, y + 10))

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
                    new_card = Card(card_element, card_type='vertical' if p.name in ['Bot 1', 'Bot 2'] else 'horizontal')
                    p.hand.append(new_card)

    def start_game(self):
        return True
    
# Running PyGame
screen_width, screen_height = 750, 1050
screen = pygame.display.set_mode([screen_width, screen_height])
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
        button_width, button_height = 130, 50
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2
        pos = [button_x, button_y, button_width, button_height]
        start = pygame.draw.rect(screen, 'red', pos, 0, 5)
        pygame.draw.rect(screen, 'green', pos, 5, 5)
        start_text = font.render('START', True, 'black')
        text_rect = start_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(start_text, text_rect)

        if event.type == pygame.MOUSEBUTTONUP and start.collidepoint(event.pos):
            active = False
            dealing = True

    if dealing: # Initialize Players and Deal Cards
        New_Game = Game('New Game')
        user_player = Player('User')
        New_Game.players.append(user_player)
        New_Game.players.append(Player('Partner'))
        New_Game.players.append(Player('Bot 1'))
        New_Game.players.append(Player('Bot 2'))

        New_Game.deal_cards(cards)

        # Flip User's cards after dealing
        for card in user_player.hand:
            card.flipped = True

        for player in New_Game.players:
            player.sort_hand()  # Sort the player's hand
            player.display_hand()

        dealing = False  # Set to False to avoid redealing and printing

    if not active:
        # Draw cards for each player
        New_Game.players[0].draw_cards(screen, 100, 900)   # User
        New_Game.players[1].draw_cards(screen, 100, 25)  # Partner
        New_Game.players[2].draw_cards(screen, 25, 150)   # Bot 1
        New_Game.players[3].draw_cards(screen, 650, 150)  # Bot 2

        New_Game.start_game()

    pygame.display.flip()
pygame.quit()
