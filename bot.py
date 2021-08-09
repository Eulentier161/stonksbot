import discord
from pycoingecko import CoinGeckoAPI
import asyncio
import yaml

client = discord.Client()
cg = CoinGeckoAPI()
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

@client.event
async def on_ready():
    print("Ready!")
    while True:
        await publish_emote()
        await asyncio.sleep(3600)

async def get_channels() -> list:
    channels = []
    for channel_id in config['channels']:
        channel = None
        try:
            channel = await client.fetch_channel(channel_id)
        except:
            continue
        finally:
            if channel:
                channels.append(channel)     
    return channels
        
async def publish_emote():
    chart = cg.get_coin_market_chart_by_id(config['crypto'], "usd", 1)['prices']
    channels = await get_channels()
    for channel in channels:
        if chart[-1][1] > chart[-2][1]:
            await channel.send("📈")
        else:
            await channel.send("📉")

if __name__ == "__main__":
    client.run(config['token'])
    