# Personalized Cards Against Humanity Bot

This bot allows you to play a personalized version of Cards Against Humanity.

## Requirements

1. **Install Python**: Make sure you have Python installed on your machine.
2. **Install Dependencies**: Run the following command to install the required packages from the `requirements.txt` file:
3. **Create Your Bot**: You need to create your bot using Telegram BotFather.

   ```bash
   pip install -r requirements.txt
4. Create and Configure config.json: You need to create a config.json file in the root directory of the project and fill in the following values:
```json
{
  "api_id": "<your_api_id>",
  "api_hash": "<your_api_hash>",
  "bot_token": "<your_bot_token>"
}
```

4. Prepare Text Files: Create a folder named text_files and include the following files:
* white_cards.txt
* black_cards.txt
Each file should contain all the cards you want to have in the game.

## Bot Setup

To get the bot up and running:
1. **Run Bot**: Make sure your program is running (deployed or locally).
2. **Players Requirement**: At least 2 players are needed to start the game. Have each player send a message saying "hi" to the bot to establish communication.
3. **Group Setup**: The bot must be added to a group chat where the game will take place. Once in the group, someone can start the game by pressing `/start`.

## Enjoy the Game!

Have fun playing!

