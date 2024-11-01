import json
from pyrogram.types import InlineKeyboardMarkup
from game_runner import GamesRunner
from pyrogram import Client, filters


def read_config(file_path):
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
        return config
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


@app.on_callback_query()
def button_click(client, callback_query):
    chat_id = callback_query.message.chat.id
    game = games_runner.get_game(callback_query.message.chat.id)
    splited = callback_query.data.split(":::")

    if len(splited) > 1 and splited[0] == "card":
        card_txt = game.get_card(chat_id, int(splited[1]))
        client.send_message(
            games_runner.get_chat_id(chat_id), "Someone chose card:" + card_txt
        )
        print(game.did_all_players_picked())
        if game.did_all_players_picked():
            picker_id = game.get_turn_id()
            bottons = game.get_bottons(picker_id)
            client.send_message(
                picker_id,
                "Time to choose a winner!:",
                reply_markup=InlineKeyboardMarkup(bottons),
            )

    # client.send_message(games_runner.get_chat_id(chat_id), "Someone chose card:" + card_txt)
    # client.send_message(chat_id, callback_query)
    if len(splited) > 1 and splited[0] == "round":
        client.send_message(
            games_runner.get_chat_id(chat_id), "We have a winner card!:"
        )
        client.send_message(
            games_runner.get_chat_id(chat_id),
            {game.get_card_from_picked(int(splited[1]))},
        )
        game_round(client, callback_query.message, game)
        # client.send_message(f"chosen card was ")
        # game_round(game, callback_query.message, client)


@app.on_message(filters.command("join"))
def start_command(client, message):

    game = games_runner.get_game(message.chat.id)
    user_id = message.from_user.id

    games_runner.add_player(message.chat.id, message.from_user.id)

    client.send_message(
        message.chat.id,
        f"{message.from_user.first_name} joined the game. /start when all players are joined",
    )
    # keyboard = InlineKeyboardMarkup(game.get_start_buttons())
    # client.send_message(message.from_user.id, "Start!", reply_markup=keyboard)
    # Send message with the inline keyboard


def game_round(client, message, game):
    game.init_new_round()
    chat_id = (
        message.chat.id
        if message.chat.id < 0
        else games_runner.get_chat_id(message.chat.id)
    )
    client.send_message(chat_id, f"You have a new black card. X choose")
    client.send_message(chat_id, f"***{game.get_black_card()}***")
    # TODO: should be chat specific!!! only players in this game. (chat_id).
    #  maybe player_to_chat is not required?
    print(games_runner.player_to_chat.keys())
    for user in games_runner.player_to_chat.keys():
        bottons = game.get_bottons(user)
        keyboard = InlineKeyboardMarkup(bottons)
        print(keyboard)
        client.send_message(user, "Time to choose.", reply_markup=keyboard)


@app.on_message(filters.command("start"))
def start_command(client, message):
    games_runner.add_player(message.chat.id, message.from_user.id)
    client.send_message(
        message.chat.id, f"{message.from_user.first_name} joined the game."
    )
    client.send_message(message.chat.id, f"Lets play the game!")
    game = games_runner.get_game(message.chat.id)
    user_id = message.from_user.id
    game_round(client, message, game)


@app.on_message(filters.command("hi"))
def say_hi(client, message):
    user_id = message.from_user.id
    client.send_message(user_id, "hi.")


app.run()
