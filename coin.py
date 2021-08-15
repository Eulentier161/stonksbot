import discord
from discord_slash.context import ComponentContext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from pycoingecko import CoinGeckoAPI
import db


async def publish_emote(cg: CoinGeckoAPI, channel: discord.TextChannel, crypto: str):
    chart = cg.get_coin_market_chart_by_id(crypto, "usd", 1)['prices']
    action_row = create_actionrow(
        create_button(
            style = ButtonStyle.blue,
            custom_id = "info_btn",
            label=f"{crypto}"
        )
    )
    await channel.send("\U0001f4c8" if chart[-1][1] > chart[-12][1] else "\U0001f4c9", components=[action_row])
    
async def info_callback(ctx: ComponentContext, cg: CoinGeckoAPI):
    await ctx.defer(hidden=True)

    db_guild_channel = db.get_channel(ctx.origin_message.channel.id)
    
    coin_infos = cg.get_coin_by_id(db_guild_channel['coin'])
    coin_name = coin_infos['name']
    coin_symbol = coin_infos['symbol']
    coin_rank = coin_infos['market_cap_rank']
    homepage = coin_infos['links']['homepage'][0]
    price_euro = coin_infos['market_data']['current_price']['eur']
    price_usd = coin_infos['market_data']['current_price']['usd']
    price_sats = coin_infos['market_data']['current_price']['sats']
    image = coin_infos['image']['large']
    price_change_24h = coin_infos['market_data']['price_change_24h']
    price_change_percentage_24h = coin_infos['market_data']['price_change_percentage_24h']
    market_cap_change_24h = coin_infos['market_data']['market_cap_change_24h']
    market_cap_change_percentage_24h = coin_infos['market_data']['market_cap_change_percentage_24h']
    
    embed = discord.Embed(title=coin_name, url=homepage, description=f"#{coin_rank}: {coin_symbol}")
    embed.set_thumbnail(url=image)
    embed.add_field(name="current price:", value=f"{round(price_euro, 2)}€\n${round(price_usd, 2)}\n{round(price_sats, 2)} sats", inline=False)
    embed.add_field(name="24h price change:", value=f"${round(price_change_24h, 2)} / {round(price_change_percentage_24h, 2)}%", inline=False)
    embed.add_field(name="24h market cap change:", value=f"${round(market_cap_change_24h, 2)} / {round(market_cap_change_percentage_24h, 2)}%", inline=False)
    
    await ctx.send(embed=embed, hidden=True)

async def get_targets(bot: discord.Client) -> dict:
    targets = []
    for target in db.get_all_channels():
        disc_channel = None
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
        await publish_emote(cg=cg, channel=target['channel'], crypto=target['coin'])
        
