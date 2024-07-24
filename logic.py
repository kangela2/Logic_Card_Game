import copy
import random
import pygame

pygame.init()

# game variables
cards = [
    '2', '3', '4',
    '5', '6', '7',
    '8', '9', '10',
    'J', 'Q', 'K'
    ]
rank_order = {
    '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13
    }
deck = 2 * cards
WIDTH = 850
HEIGHT = 850
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Logic')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)
title_font = pygame.font.Font('freesansbold.ttf', 80)
log_font = pygame.font.Font('freesansbold.ttf', 18)
button_font = pygame.font.Font('freesansbold.ttf', 24)
active = False
initial_deal = False
win = False
players = []
teams = []
win_results = []

# Define colors
BLACK = 'black'
WHITE = 'white'
BACKGROUND = 'limegreen'

# Define the size of each card
card_width = 75
card_height = 105

# Define the space between card
space = 20
corner_length = 150

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
        self.idx = [0, 1, 2, 3, 4, 5]
        self.flipped = [False, False, False, False, False, False]
        
def simulate_loop():
    i = 0
    w = False
    
    while not w:
        i += 1
        w, winner, loser = simulate_game(i)
        
    return w, winner, loser
        
def simulate_game(turn):
    end = False
    player = players[turn%4 - 1]
    
    # player guesses cards of the opponent to their left
    opponent = players[turn%4]
    
    # chance that the player will guess the cards of opponent to their right
    if random.getrandbits(1):
        opponent = players[turn%4 - 2]

    x = random.randint(0, len(opponent.idx) - 1)
    
    index = opponent.idx[x]
    guess = random.randint(0, len(cards) - 1)
    
    text = [
        f"Turn {turn}:",
        f"[{player.name}] guessed [{opponent.name}]'s",
        f"{index+1} card as a {cards[guess]}",
        f"{guess_card(opponent, index, cards[guess])}"
        ]
    
    string = " ".join(text)
    
    add_turn(log, string, visible_log, turn)
    
    if opponent.flipped[index]:
        opponent.idx.remove(index)
        end = check_endgame(player, opponent, turn)
#        print(string)
    
    return end, player, opponent
        
def check_endgame(player, opponent, turn):
    if len(opponent.idx) == 0:
        return True
    return False
        
def guess_card(player, index, guess):
    if player.hand[index] == guess:
        player.flipped[index] = True
        return "correctly"
        
    return "incorrectly"

def initialize_players():
    # clear previous players if any
    if len(players) > 0:
        players.clear()
        
    # adds player 1 // user // bottom hand to list of players
    players.append(Player("A"))
    
    # adds player 2 // opponent // left hand to list of players
    players.append(Player("B"))
    
    # adds player 3 // user's partner // top hand to list of players
    players.append(Player("C"))
    
    # adds player 4 // opponent's partner // right hand to list of players
    players.append(Player("D"))
    
    
    # creates the first team with players 1 & 3
    teams.append((players[0], players[2], "Player Team"))
    
    # creates the second team with players 2 & 4
    teams.append((players[1], players[3], "Opposing Team"))
    
# get key of card based on rank
def card_key(card):
    return rank_order[card]

def clear_logs():
    log.clear()
    visible_log.clear()

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
            
    return current_hand, current_deck

# draw cards visually onto screen depending on hand, x and y starting positions, whether or not they're displayed vertically, and what order the ranks should be displayed
def draw_cards(player, x, y, vertical, order):
    for i in range(len(player.hand)):
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
        
        pos = [x + 10, y + 10]
        
        # display rank on cards only if card is flipped
        if order and player.flipped[i]:
            rank = font.render(player.hand[i], True, BLACK)
            screen.blit(rank, pos)
            
        elif not order and player.flipped[5 - i]:
            rank = font.render(player.hand[5 - i], True, BLACK)
            screen.blit(rank, pos)
            
        pos[1] -= 30
        
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
        text = log_font.render(turn, True, BLACK)
        screen.blit(text, (log_pos + 10, y))
        y -= 20
        
def draw_win():
    winning_team = ""
    
    winner = win_results[0]
    loser = win_results[1]
    turn = win_results[2]
    
    for i in range(len(teams)):
        if teams[i].count(winner) > 0:
            winning_team = teams[i][2]
    
    text = [
        f"[{winner.name}] guessed [{loser.name}]'s",
        f"final card correctly on Turn {turn}",
        f"{winning_team} Wins!"
    ]
    
    pos = [
        log_pos,
        log_pos + log_height + space,
        log_width,
        120
        ]
    
    pygame.draw.rect(screen, WHITE, pos, 0, 5)
    pygame.draw.rect(screen, BLACK, pos, 5, 5)
    
    pos[0] += 75
    pos[1] += 65
    pos[2] = 150
    pos[3] = 42
    
    exit = pygame.draw.rect(screen, 'red', pos, 0, 5)
    pygame.draw.rect(screen, BLACK, pos, 5, 5)
    
    exit_text = button_font.render('Exit Game', True, BLACK)
    screen.blit(exit_text, (pos[0] + 10, pos[1] + 10))
    
    pos[0] += pos[2] + 50
    
    play = pygame.draw.rect(screen, 'green', pos, 0, 5)
    pygame.draw.rect(screen, BLACK, pos, 5, 5)
    
    play_text = button_font.render('Play Again', True, BLACK)
    screen.blit(play_text, (pos[0] + 10, pos[1] + 10))
    
    pos = [
        log_pos + 10,
        log_pos + log_height + space + 10,
        ]
    
    win_text = button_font.render(text[2], True, BLACK)
    screen.blit(win_text, pos)
    
    text.pop()
    
    pos[1] += 30
    
    string = " ".join(text)

    win_text = log_font.render(string, True, BLACK)
    screen.blit(win_text, pos)
    
    return exit, play

# draws game elements depending on scene
def draw_game(act):
    button_list = []
    
    # initially on startup (not active) only option is to start game
    if not active:
        title_text = title_font.render('LOGIC', True, BLACK)
        screen.blit(title_text, (300, 100))
        
        pos = [
            360,    # x
            400,    # y
            130,    # width
            50      # height
            ]
        
        # display start game button
        start = pygame.draw.rect(screen, 'red', pos, 0, 5)
        pygame.draw.rect(screen, 'green', pos, 5, 5)
        
        start_text = font.render('START', True, BLACK)
        screen.blit(start_text, (pos[0] + 16, pos[1] + 14))
        
        button_list.append(start)
        
    # once game started, show game board and user action options
    else:
        # displays log window
        pos = [log_pos, log_pos]
        dimensions = [log_width, log_height]
        
        pygame.draw.rect(screen, WHITE, [pos, dimensions], 0, 5)
        pygame.draw.rect(screen, BLACK, [pos, dimensions], 5, 5)
        
        if win:
            exit, play = draw_win()
            button_list.append(exit)
            button_list.append(play)

    return button_list

# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill(BACKGROUND)
    
    # deal cards to players
    if initial_deal:
        for i in range(6):
            for x in players:
                x.hand, game_deck = deal_cards(x.hand, game_deck)
        
        initial_deal = False
        
        # sort hands after they're all dealt
        for x in players:
            x.hand = sorted(x.hand, key = card_key)
    
    # once game is started, and cards are dealt, display board
    if active:
        pos = [
            corner_length,                  # offset window corner
            WIDTH - space - card_height,    # offset card length
            space                           # offset window edge
            ]
        
        # draws user's hand at the bottom of the board
        draw_cards(players[0], pos[0], pos[1], False, True)
        
        # draws opponent's hand on the left side of the board
        draw_cards(players[2], pos[0], pos[2], False, False)
        
        # draws user's partner's hand at the top of the board
        draw_cards(players[1], pos[2], pos[0], True, True)
        
        # draws opponent's partner's hand on the right side of the board
        draw_cards(players[3], pos[1], pos[0], True, False)
    
    buttons = draw_game(active)
    
    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    win = False
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(deck)
                    initialize_players()
                    
            if win:
                if buttons[0].collidepoint(event.pos):
                    active = False
                    clear_logs()
                    
                elif buttons[1].collidepoint(event.pos):
                    win = False
                    initial_deal = True
                    game_deck = copy.deepcopy(deck)
                    initialize_players()
                    clear_logs()
                
        # placeholder functionality to test log
        if active and not win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    turn_number = len(log) + 1
                    
                    win, winner, loser = simulate_loop()
                    
#                    win, winner, loser = simulate_game(turn_number)

                    if win:
                        win_results = [
                            winner,
                            loser,
                            len(log)
#                            turn_number
                            ]
                        
    draw_log(visible_log)

    pygame.display.flip()
pygame.quit()
