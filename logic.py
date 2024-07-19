import copy
import random
import pygame

pygame.init()

#class to draw make guess button and face value options for the guess 
class GameButtons:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 17)
        self.make_guess_button = pygame.Rect(360, 650, 130, 50)
        self.face_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.face_value_buttons = []
        self.show_face_values = False
        self.selected_card = None
        self.selected_card_index = None
        self.guessed_value = None

    #button display
    def draw_make_guess(self):
        pygame.draw.rect(self.screen, 'gray', self.make_guess_button, 0, 5)
        pygame.draw.rect(self.screen, 'black', self.make_guess_button, 3, 5)
        text = self.font.render('MAKE GUESS', True, 'black')
        text_rect = text.get_rect(center=self.make_guess_button.center)
        self.screen.blit(text, (365, 666))

    #guess display
    def draw_face_values(self):
        self.face_value_buttons = []
        if self.show_face_values:
            for i, value in enumerate(self.face_values):
                button = pygame.Rect(50 + i*60, 600, 40, 40)
                pygame.draw.rect(self.screen, 'white', button, 0, 5)
                #highlights guessed card with pink border, normal cards have black border
                #need to modify later so it's for all clicked cards for any button action
                outline_color = 'pink' if value == self.guessed_value else 'black'
                pygame.draw.rect(self.screen, outline_color, button, 2, 5)
                text = self.font.render(value, True, 'black')
                self.screen.blit(text, (60 + i*60, 615))
                self.face_value_buttons.append(button)

    #new thing???
    def draw_player_cards(self, player_hand):
        for i, card in enumerate(player_hand):
            x = 150 + (75 + 20) * i
            y = 725
            pygame.draw.rect(self.screen, 'white', [x, y, 75, 105], 0, 5)
            outline_color = 'pink' if i == self.selected_card_index else 'black'
            pygame.draw.rect(self.screen, outline_color, [x, y, 75, 105], 5, 5)
            self.screen.blit(self.font.render(card, True, 'black'), (x + 10, y + 10))

    #compares selected card w player's guess
    def handle_click(self, pos, player_hand):
        if self.make_guess_button.collidepoint(pos):
            self.show_face_values = True
            return "make_guess"
        
        if self.show_face_values:
            for i, button in enumerate(self.face_value_buttons):
                if button.collidepoint(pos):
                    self.show_face_values = False
                    guess = self.face_values[i]
                    return self.check_guess(guess)
        
        # Check if a card was clicked
        for i, card in enumerate(player_hand):
            card_rect = pygame.Rect(150 + (75 + 20) * i, 725, 75, 105)
            if card_rect.collidepoint(pos):
                self.selected_card = card
                return "card_selected"

        return None

    def check_guess(self, guess):
        if self.selected_card == guess:
            return True
        else: 
            result = False
        self.selected_card = None
        self.selected_card_index = None
        self.guessed_value = None
        return result


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
active = False
initial_deal = False
game_deck = one_deck
player_hand = []
teammate_hand = []
left_oppenent_hand = []
right_opponent_hand = []
#add game buttons
game_buttons = GameButtons(screen)


# Define the size of each card
card_width = 75
card_height = 105

# Define the space between card
space = 20
edge_length = 150

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
    
    hand = sorted(hand, key = card_key)

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


def draw_game(act, game_buttons):
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
    else:
        game_buttons.draw_make_guess()
        game_buttons.draw_face_values()

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
            player_hand, game_deck = deal_cards(player_hand, game_deck)
            left_oppenent_hand, game_deck = deal_cards(left_oppenent_hand, game_deck)
            teammate_hand, game_deck = deal_cards(teammate_hand, game_deck)
            right_opponent_hand, game_deck = deal_cards(right_opponent_hand, game_deck)
            
        # prints every player's hand
#        print(player_hand, teammate_hand, left_oppenent_hand, right_opponent_hand)
        
        initial_deal = False
    
    # once game is started, and cards are dealt, display board
    if active:
        draw_cards(player_hand, edge_length, WIDTH - space - card_height, False, True)
        draw_cards(teammate_hand, edge_length, space, False, False)
        draw_cards(left_oppenent_hand, space, edge_length, True, True)
        draw_cards(right_opponent_hand, WIDTH - space - card_height, edge_length, True, False)

    #pass game buttons here
    buttons = draw_game(active, game_buttons)  
    
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
            else:
                result = game_buttons.handle_click(event.pos, player_hand)
                if result == "make_guess":
                    print("Make a guess by clicking a card and then selecting a face value.")
                elif result == "card_selected":
                    print("Card selected. Now choose a face value to guess.")
                elif result is not None:
                    print(f"Your guess was {'correct' if result else 'incorrect'}!")
                            
    pygame.display.flip()
pygame.quit()
