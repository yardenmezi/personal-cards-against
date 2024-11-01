import random


class CardsPile:
    HAND_SIZE = 10

    def __init__(self, cards_file_path):
        self.cards = self.read_cards_from_file(cards_file_path)
        random.shuffle(self.cards)

    def is_pile_empty(self):
        return len(self.cards) == 0

    def read_cards_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                cards = [line.strip() for line in lines]
            return cards
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return []

    def draw_hand(self):
        partition_idx = min(CardsPile.HAND_SIZE, len(self.cards))
        hand = self.cards[:partition_idx]
        self.cards = self.cards[partition_idx:]
        return hand

    def draw_card(self):
        if not self.cards:
            return None
        txt = self.cards.pop()
        return txt
