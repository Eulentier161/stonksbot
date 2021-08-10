nonsense project i made as a meme\
the bot will publish one of 2 emotes every hour in all channels inside its `config.yaml` depending on the last 2 price snapshots it gets from coingeckos api for a crypto coin.

if you want to selfhost this bot:
- clone this project
- create `config.yaml` like this:
```
token: <discord_bot_token>
crypto: <coingecko_crypto_id>
channels:
  - <discord.TextChannel.id>
  - <discord.TextChannel.id>
  - [...]
```
- create a virtual environment, install requirements and run the bot:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```
