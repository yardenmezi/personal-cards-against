from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types.bots_and_keyboards import callback_query

from cards import CardsPile


class Game:
    def __init__(self, chat_id):
        self.players_card = {}
        self.player_idx = []
        self.white_cards = CardsPile("text_files/white_cards.txt")
        self.black_cards = CardsPile("text_files/black_cards.txt")
        self.turn_cards = []
        self.turn = 0

    def add_player(self, player_id):
        if player_id not in self.players_card:
            self.player_idx.append(player_id)
            # self.player_idx[player_id] = len(self.players_card)
            self.players_card[player_id] = self.white_cards.draw_hand()
        print("player added", self.player_idx)

    def get_start_buttons(self):
        buttons = [
            [InlineKeyboardButton("I would like to start!", callback_data="start")]
        ]
        return buttons

    def get_card_from_picked(self, card_num):
        return self.turn_cards[card_num][0]

    def init_new_round(self):
        self.turn_cards = []

    def get_card(self, player_id, card_num):
        # cards should be taken from the turn cards
        card = self.players_card[player_id][card_num]
        self.turn_cards.append([card, player_id])
        self.players_card[player_id][card_num] = self.white_cards.draw_card()
        return card

    def did_all_players_picked(self):
        return len(self.turn_cards) == len(self.players_card) - 1

    def get_turn_id(self):
        return self.player_idx[self.turn]

    def get_black_card(self):
        return self.black_cards.draw_card()

    def get_buttons(self, player_id, callback_data=None):
        if self.player_idx[self.turn] == player_id:
            if self.did_all_players_picked():
                if len(self.player_idx) == 1:
                    buttons = [
                        [InlineKeyboardButton("you are alone here..")]
                    ]
                else:
                    buttons = [
                        [InlineKeyboardButton(card[0], "round" + ":::" + str(i))]
                        for i, card in enumerate(self.turn_cards)
                    ]
                self.turn = (self.turn + 1) % len(self.players_card)
            else:
                buttons = [[InlineKeyboardButton("WAIT.", "NOTHING")]]
        else:
            buttons = [
                [InlineKeyboardButton(card, "card" + ":::" + str(i))]
                for i, card in enumerate(self.players_card[player_id])
            ]

        return buttons
