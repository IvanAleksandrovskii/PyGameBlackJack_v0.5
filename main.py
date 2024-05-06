import random
from dataclasses import dataclass
import pygame

pygame.init()


@dataclass
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        # string, just for a case
        self.rank = str(self.rank)
        self.suit = str(self.suit)
        self.image_name = f'{self.rank}_of_{self.suit}.png'

    def get_score(self) -> int:
        rank = self.rank
        if rank.isdigit():
            return int(rank)
        elif rank in ('jack', 'queen', 'king'):
            return 10
        elif rank == 'ace':
            return 11


def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    suits = ['hearts', 'spades', 'clubs', 'diamonds']
    return [Card(rank, suit) for suit in suits for rank in ranks]


@dataclass
class Deck:
    cards: list = None

    def __post_init__(self):
        self.cards = self.cards if self.cards is not None else create_deck()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            self.cards = create_deck()
            self.shuffle()
        return self.cards.pop(0)


@dataclass
class Hand:
    cards: list = None

    def __post_init__(self):
        self.cards = [] if self.cards is None else self.cards

    def hand_score(self) -> int:
        scores = 0
        aces = 0
        for card in self.cards:
            card_score = card.get_score()
            if card.rank == 'ace':
                aces += 1
            scores += card_score

        while scores > 21 and aces:
            scores -= 10
            aces -= 1
        return scores


def load_image(path, scale=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {str(e)}")
        return None  # Optionally return a placeholder image or halt the game


class CardVisuals:
    def __init__(self, screen):
        self.screen = screen

    def visual_player_hand(self, hand, start_x=150, start_y=500):
        x_position = start_x
        for card in hand.cards:
            image_path = f"images/cards/{card.image_name}"
            card_image = load_image(image_path, scale=(120, 150))
            if card_image:
                self.screen.blit(card_image, (x_position, start_y))
            x_position += 25

    def visual_dealer_hand(self, hand, start_x=300, start_y=300):
        x_position = start_x
        for card in hand.cards:
            image_path = f"images/cards/{card.image_name}"
            card_image = load_image(image_path, scale=(120, 150))
            if card_image:
                self.screen.blit(card_image, (x_position, start_y))
            x_position -= 25

    def visual_dealer_hand_hidden(self, hand, start_x=300, start_y=300):
        x_position = start_x
        card_back_path = "images/cards/card_back.png"
        card_back = pygame.image.load(card_back_path).convert_alpha()
        card_back = pygame.transform.scale(card_back, (120, 150))
        self.screen.blit(card_back, (x_position, start_y))  # Draw the card back image for the first card

        for card in hand.cards[1:]:
            image_path = f"images/cards/{card.image_name}"
            card_image = load_image(image_path, scale=(120, 150))
            if card_image:
                self.screen.blit(card_image, (x_position - 25, start_y))
            x_position -= 25


class Button:
    def __init__(self, screen, x, y, width, height, text, text_color, button_color, hover_color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)  # Here specify the font
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, mouse):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.button_color, button_rect)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, self.hover_color, button_rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def is_hovered(self, mouse):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return button_rect.collidepoint(mouse)


record = [0, 0, 0]  # Wins, Losses, Draws


def get_result(player_hand, dealer_hand, record):
    player_score = player_hand.hand_score()
    dealer_score = dealer_hand.hand_score()

    if player_score > 21:
        record[1] += 1
        return 0, record  # Player busts
    elif player_score == 21 and dealer_score != 21:
        record[0] += 1
        return 1, record  # Player has Blackjack
    elif dealer_score > 21:
        record[0] += 1
        return 2, record  # Dealer busts
    elif player_score > dealer_score:
        record[0] += 1
        return 3, record  # Player wins
    elif player_score < dealer_score:
        record[1] += 1
        return 4, record  # Dealer wins
    else:
        record[2] += 1
        return 5, record  # Tie


def draw_result_text(screen, get_result):
    end_game_font = pygame.font.Font('fonts/Jersey.ttf', 50)

    if get_result[0] == 0:
        text = 'You\'r BUSTED'
        result_text = end_game_font.render(text, True, (230, 41, 3))
        screen.blit(result_text, (180, 450))
    elif get_result[0] == 1:
        text = 'BlackJack!!!'
        result_text = end_game_font.render(text, True, (22, 235, 22))
        screen.blit(result_text, (180, 450))
    elif get_result[0] == 2:
        text = 'You WON!!!'
        result_text = end_game_font.render(text, True, (22, 235, 22))
        screen.blit(result_text, (180, 450))
    elif get_result[0] == 3:
        text = 'You WON!!!'
        result_text = end_game_font.render(text, True, (22, 235, 22))
        screen.blit(result_text, (180, 450))
    elif get_result[0] == 4:
        text = 'You LOSE :('
        result_text = end_game_font.render(text, True, (230, 41, 3))
        screen.blit(result_text, (180, 450))
    elif get_result[0] == 5:
        text = 'It\'s a DRAW'
        result_text = end_game_font.render(text, True, (255, 218, 16))
        screen.blit(result_text, (180, 450))


def main():
    # Setup screen and game title
    screen = pygame.display.set_mode((600, 900))
    pygame.display.set_caption('Black Jack 0.5')
    pygame.display.set_icon(pygame.image.load('images/icon_black_jack.png'))

    # Dealer icon
    dealer_icon = pygame.image.load('images/dealer_icon.png').convert_alpha()
    dealer_icon_layer = pygame.image.load('images/dealer_icon.png').convert_alpha()
    dealer_icon = pygame.transform.scale(dealer_icon, (100, 100)).convert_alpha()

    # Mr Bean
    Mr_Bean = pygame.image.load('images/Mr_Bean.png').convert_alpha()
    Mr_Bean = pygame.transform.scale(Mr_Bean, (100, 332))

    # Initialize fonts
    font = pygame.font.Font('fonts/Montserrat.ttf', 43)
    smaller_font = pygame.font.Font('fonts/Montserrat.ttf', 36)

    # Card back
    card_back_path = f"images/cards/card_back.png"
    card_back = pygame.image.load(card_back_path).convert_alpha()
    card_back = pygame.transform.scale(card_back, (60, 75)).convert_alpha()

    # Set frames per second
    card_vis = CardVisuals(screen)
    fps = 60
    timer = pygame.time.Clock()

    # Create an Instance-Deck and get the cards
    deck_instance = Deck()
    deck_instance.shuffle()
    deck = deck_instance
    player_hand = Hand()
    dealer_hand = Hand()

    running = True
    active = False
    first_deal = True
    first_check = True
    second_check = True
    the_end = False
    dealer_reveal = False
    dealer_reveal2 = False
    third_check = True
    a = None

    # Value to rendering a decorative deck
    number_of_cards = 40

    # Create button instances
    deal_button = Button(screen, 150, 700, 290, 100, 'DEAL HAND', (0, 0, 0),
                         (0, 167, 144), (0, 75, 66))
    hit_button = Button(screen, 10, 700, 290, 100, 'HIT ME', (0, 0, 0),
                        (0, 167, 144), (0, 75, 66))
    stand_button = Button(screen, 300, 700, 290, 100, 'STAND', (0, 0, 0),
                          (0, 167, 144), (0, 75, 66))

    score_text = smaller_font.render(f'Wins: {record[0]} Lose: {record[1]} Draw: {record[2]}', True,
                                     (255, 255, 255))
    screen.blit(score_text, (90, 830))

    while running:
        timer.tick(fps)
        screen.fill((62, 149, 199))
        screen.blit(dealer_icon, (240, 50))
        screen.blit(Mr_Bean, (40, 500))

        score_text = smaller_font.render(f'Wins: {record[0]} Lose: {record[1]} Draw: {record[2]}', True,
                                         (255, 255, 255))
        screen.blit(score_text, (90, 830))

        hand_score_font = pygame.font.Font('fonts/Gothic.ttf', 36)
        hand_score_text = hand_score_font.render(f'Score: {player_hand.hand_score()}', True,
                                                 (0, 0, 0))
        if the_end:
            screen.blit(hand_score_text, (250, 660))

        mouse_pos = pygame.mouse.get_pos()

        # Decorative deck
        for b in range(number_of_cards):
            offset = b * 0.15  # Each card is offset by 2 pixels
            screen.blit(card_back, (350 + offset, 100 + offset))

        if not active:
            deal_button.draw(mouse_pos)

        if active:

            # Dealer takes cards
            if dealer_reveal:
                while 21 > player_hand.hand_score() > dealer_hand.hand_score() and dealer_hand.hand_score() < 17:
                    dealer_hand.cards.append(deck.deal_card())
                dealer_reveal = False
                the_end = True
                active = False

            if first_deal:
                dealer_hand.cards.append(deck.deal_card())
                dealer_hand.cards.append(deck.deal_card())
                player_hand.cards.append(deck.deal_card())
                player_hand.cards.append(deck.deal_card())
                first_deal = False
                if player_hand.hand_score() == 21 and first_check:
                    the_end = True
                    active = False
                first_check = False

            hit_button.draw(mouse_pos)
            stand_button.draw(mouse_pos)

            # Visual hands
            card_vis.visual_player_hand(player_hand)
            if dealer_reveal2:
                card_vis.visual_dealer_hand(dealer_hand)
            else:
                card_vis.visual_dealer_hand_hidden(dealer_hand)

            # Player allowed to hint
            if player_hand.hand_score() > 21:
                dealer_reveal = True
                dealer_reveal2 = True

            elif second_check:
                the_end = True
                second_check = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP and active:
                mouse_x, mouse_y = event.pos  # Get the position of the mouse when the button is released

                if hit_button.rect.collidepoint(mouse_x, mouse_y):  # Check if the hit button was clicked
                    player_hand.cards.append(deck.deal_card())

                elif stand_button.rect.collidepoint(mouse_x, mouse_y):  # Check if the stand button was clicked
                    dealer_reveal = True
                    dealer_reveal2 = True

            elif event.type == pygame.MOUSEBUTTONUP and not active:
                mouse_x, mouse_y = event.pos

                if deal_button.rect.collidepoint(mouse_x, mouse_y):
                    player_hand = Hand()
                    dealer_hand = Hand()

                    active = True
                    first_deal = True
                    first_check = True
                    second_check = True
                    third_check = True
                    the_end = False
                    dealer_reveal = False
                    dealer_reveal2 = False
                    a = None
                else:
                    pass

        if the_end and not active:

            # Visual hands
            card_vis.visual_player_hand(player_hand)
            card_vis.visual_dealer_hand(dealer_hand)
            screen.blit(score_text, (90, 830))
            hand_score_text = hand_score_font.render(f'Dealer\'s score: {dealer_hand.hand_score()}',
                                                     True, (0, 0, 0))
            screen.blit(hand_score_text, (200, 240))

            if third_check:
                a = get_result(player_hand, dealer_hand, record)
                third_check = False

            draw_result_text(screen, get_result=a)

            deal_button.draw(mouse_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
