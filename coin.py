import discord
from pycoingecko import CoinGeckoAPI
import db


async def publish_emote(cg: CoinGeckoAPI, bot: discord.Client, channel: discord.TextChannel, crypto: str):
    chart = cg.get_coin_market_chart_by_id(crypto, "usd", 1)['prices']
    await channel.send("\U0001f4c8" if chart[-1][1] > chart[-12][1] else "\U0001f4c9")

async def get_targets(bot: discord.Client) -> dict:
    targets = []
    disc_channel = None
    for target in db.get_all_channels():
        try:
            disc_channel: discord.TextChannel = await bot.fetch_channel(target['channel_id'])
        except:
            continue
        finally:
            if disc_channel:
                targets.append({"channel": disc_channel, "coin": target['coin']})
    return targets

async def start_schedule(bot: discord.Client, cg: CoinGeckoAPI):
    targets = await get_targets(bot)
    for target in targets:
        await publish_emote(cg=cg, bot=bot, channel=target['channel'], crypto=target['coin'])
        
