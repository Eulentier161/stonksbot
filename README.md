nonsense project i made as a meme\
the bot will publish one of 2 emotes every hour depending on the last 2 price snapshots it gets from coingeckos api for a crypto coin.

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
Never gonna give you up