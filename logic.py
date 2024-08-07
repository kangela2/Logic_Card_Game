# Summer Capstone 2024
import copy
import random
import pygame
import time

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
    def __init__(self, value, card_type='horizontal', position = []):
        self.value = value
        self.flipped = False
        self.card_type = card_type
        self.position = position

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def display_hand(self):
        print(self.name)
        for x in self.hand:
            print(x.value)

    def rename(self):
        name_input = input(f'Name player {self.name}: ')
        self.name = name_input

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.value)
        for h in self.hand:
            if h.value == 11:
                h.value = 'J'
            elif h.value == 12:
                h.value = 'Q'
            elif h.value == 13:
                h.value = 'K'
            else:
                h.value = str(h.value)

    def draw_cards(self, screen, start_x, start_y):
        card_width = 75
        card_height = 105
        spacing = 20

        for i, card in enumerate(self.hand):
            display_name = font.render(self.name, True, 'purple')
            if card.card_type == 'horizontal':
                x = start_x + i * (card_width + spacing)
                y = start_y
                screen.blit(display_name, (25, y))
            else:  # vertical
                x = start_x
                y = start_y + i * card_height
                screen.blit(display_name, (x, 100))
            
            card.position = pygame.draw.rect(screen, 'white', (x, y, card_width, card_height)) if card.card_type == 'horizontal' else pygame.draw.rect(screen, 'white', (x, y, card_height, card_width))
        
            # Only display the value if User, Flipped or Partner
            if self.name == 'User':
                value_text = str(card.value)
                value_rendered = font.render(value_text, True, 'red' if card.flipped else 'black')
                screen.blit(value_rendered, (x + 10, y + 10))
            elif card.flipped == 'User View':
                value_text = str(card.value)
                value_rendered = font.render(value_text, True, 'blue')
                screen.blit(value_rendered, (x + 10, y + 10))
            elif card.flipped:
                value_text = str(card.value)
                value_rendered = font.render(value_text, True, 'red')
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

    def enable_game_log(self):
        pygame.draw.rect(screen, 'green', (150, 200, 450, 600)) # x, y

        return True

    def start_game(self):        

        # self.enable_game_log()

        for i, card in enumerate(self.players[1].hand): # Opponent Card Flipped Onclick
            if event.type == pygame.MOUSEBUTTONUP and card.position.collidepoint(event.pos):
                if not card.flipped:
                    card.flipped = 'User View'
        for card in [self.players[2].hand + self.players[3].hand]:
            for c in card:
                if event.type == pygame.MOUSEBUTTONUP and c.position.collidepoint(event.pos) and not c.flipped:
                    user_guess = input('Guess: ')
                    if user_guess == str(c.value):
                        print('Correct!')
                        c.flipped = True
                    else:
                        random_player = self.players[random.randint(0, 1)]
                        random_idx = random.randint(0, len(random_player.hand) - 1)
                        random_card = random_player.hand[random_idx]

                        if not all(u.flipped for u in self.players[0].hand + self.players[1].hand):
                            while random_card.flipped:
                                random_player = self.players[random.randint(0, 1)]
                                random_idx = random.randint(0, len(random_player.hand) - 1)
                                random_card = random_player.hand[random_idx]

                        random_card.flipped = True
                        print("Wrong",  random_player.name, "'s card", random_card.value, "is now visible!")

                #         if all(u.flipped for u in self.players[0].hand) or all(u.flipped for u in self.players[1].hand):
                #             print('You lost!')
                # if all(a.flipped for a in self.players[2].hand) or all(b.flipped for b in self.players[3].hand):
                #     print('You won!') # Guess all cards for either bot

    
# Running PyGame
screen_width, screen_height = 900, 900
screen = pygame.display.set_mode([screen_width, screen_height], pygame.RESIZABLE)
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
        start_text = font.render('Make sure Terminal is in view, then click this button', True, 'black')
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

        for player in New_Game.players:
            player.sort_hand() # Sort the player's hand
            player.rename()
        for player in New_Game.players:
            player.display_hand()

        dealing = False  # Set to False to avoid redealing and printing

    if not active:
        # Draw cards for each player
        New_Game.players[0].draw_cards(screen, 160, 750)   # User
        New_Game.players[1].draw_cards(screen, 160, 25)  # Partner
        New_Game.players[2].draw_cards(screen, 25, 125)   # Bot 1
        New_Game.players[3].draw_cards(screen, 750, 125)  # Bot 2

        New_Game.start_game()

    pygame.display.flip()
pygame.quit()
