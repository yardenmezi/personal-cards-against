import json
from pyrogram.types import InlineKeyboardMarkup
from game_runner import GamesRunner
from pyrogram import Client, filters
from game import SPLIT_SIGN
import game_messages as msgs


def read_config(file_path):
    try:
        with open(file_path, "r") as file:
            bot_config = json.load(file)
        return bot_config
    except FileNotFoundError:
        print(f"Config file '{file_path}' not found.")
        return {}


config_file_path = "config.json"
config = read_config(config_file_path)
app = Client(
    "my_bot",
    api_hash=config.get("api_hash"),
    api_id=config.get("api_id"),
    bot_token=config.get("bot_token"),
)
games_runner = GamesRunner()


def _handle_card_picking(content, game, chat_id, client):
    card_txt = game.get_card(chat_id, int(content))
    client.send_message(
        games_runner.get_chat_id(chat_id), "Someone picked card:" + card_txt
    )
    if game.did_all_players_picked():
        picker_id = game.get_turn_id()
        buttons = game.get_buttons(picker_id)
        client.send_message(
            picker_id,
            msgs.PICK_WINNER,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def _handle_round_end(content, game, chat_id, client, msg):
    client.send_message(games_runner.get_chat_id(chat_id), msgs.ROUND_WINNER)
    client.send_message(
        games_runner.get_chat_id(chat_id),
        {game.get_card_from_picked(int(content))},
    )
    game_round(client, msg, game)


@app.on_callback_query()
def button_click(client, callback_query):
    chat_id = callback_query.message.chat.id
    game = games_runner.get_game(callback_query.message.chat.id)
    data_lst = callback_query.data.split(SPLIT_SIGN)

    if len(data_lst) > 1:
        data_type = data_lst[0]
        content = data_lst[1]
        if data_type == "card":
            _handle_card_picking(content, game, chat_id, client)
        elif data_type == "round":
            _handle_round_end(content, game, chat_id, callback_query.message)


@app.on_message(filters.command("join"))
def start_command(client, message):
    games_runner.add_player(message.chat.id, message.from_user.id)

    client.send_message(
        message.chat.id,
        message.from_user.first_name + msgs.JOINED_GAME,
    )


def game_round(client, message, game):
    game.init_new_round()
    chat_id = (
        message.chat.id
        if message.chat.id < 0
        else games_runner.get_chat_id(message.chat.id)
    )
    client.send_message(chat_id, msgs.PICK_BLACK)
    client.send_message(chat_id, f"***{game.get_black_card()}***")
    for user in games_runner.player_to_chat.keys():
        buttons = game.get_buttons(user)
        keyboard = InlineKeyboardMarkup(buttons)
        client.send_message(user, msgs.PICK_WHITE, reply_markup=keyboard)


@app.on_message(filters.command(msgs.START_GAME_KEYWORD))
def start_command(client, message):
    games_runner.add_player(message.chat.id, message.from_user.id)
    client.send_message(
        message.chat.id, message.from_user.first_name + msgs.JOINED_GAME
    )
    client.send_message(message.chat.id, msgs.START_GAME)
    game = games_runner.get_game(message.chat.id)
    user_id = message.from_user.id
    game_round(client, message, game)


@app.on_message(filters.command(msgs.INTRODUCE_KEYWORD))
def say_hi(client, message):
    user_id = message.from_user.id
    client.send_message(user_id, msgs.REPLY_INTRODUCE)


app.run()
