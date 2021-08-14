nonsense project i made as a meme\
the bot will publish one of 2 emotes every hour depending on the last 2 price snapshots it gets from coingeckos api for a crypto coin.

#### if you want this bot in your server:
- [invite it](https://discord.com/api/oauth2/authorize?client_id=874400695346925630&permissions=0&scope=bot%20applications.commands)
- use its slash commands to set it up

#### if you want to selfhost this bot:
- clone this project
- create `config.yaml` with your bot token and postgresql creds like this:
```
token: <discord_bot_token>
database:
  username: <username>
  password: <password>
  name: <name>
  address: <address>
  port: <port>
```
- create a virtual environment, install requirements and run the bot:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```
