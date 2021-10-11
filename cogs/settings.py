import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button
from pycoingecko import CoinGeckoAPI
import db
import os


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.cg = CoinGeckoAPI()
        self.coins_list = self.cg.get_coins_list()
        
    @cog_ext.cog_slash(name="addit", description="add or edit a channel to post crypto updates")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def addit_cmd(self, ctx: SlashContext, channel: discord.TextChannel, target_coin: str):
        if target_coin not in [coin['id'] for coin in self.coins_list]:
            await ctx.reply(f"`{target_coin}` is not a valid id. https://api.coingecko.com/api/v3/coins/list", hidden=True)
            return
        db.create_or_update_channel(ctx.guild.id, channel.id, target_coin)
        await ctx.reply(f"ill post {target_coin} infos in {channel.mention} from now on. remove this rule with `/remove <channel>`")
        
    @cog_ext.cog_slash(name="remove", description="remove a channel from crypto updates")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def settings_cmd(self, ctx: SlashContext, channel: discord.TextChannel):
        db.delete_channel(channel.id)
        await ctx.reply(f"im not going to post updates to {channel.mention} anymore")
        
    @cog_ext.cog_slash(name="list", description="list all crypto-rules for your guild")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def list_cmd(self, ctx: SlashContext):
        channels = db.get_all_guild_channels(ctx.guild.id)
        response = ""
        for channel in channels:
            disc_channel: discord.TextChannel = self.bot.get_channel(channel['channel_id'])
            response += f"{disc_channel.mention}: {channel['coin']}\n"
        await ctx.send(response) if response else await ctx.send("None")

    @cog_ext.cog_slash(name="price", description="get infos about a coin")
    async def price_cmd(self, ctx: SlashContext, coin: str):
        coin_list = self.cg.get_coins_list()
        found = False
        for entry in coin_list:
            if entry["name"].lower() == coin or entry["symbol"].lower() == coin:
                coin = {
                    "id": entry["id"], 
                    "name": entry["name"], 
                    "symbol": entry["symbol"]
                }
                found = True
                break
        if not found:
            ctx.send(f"i cant find {coin}", hidden=True)
            return
        coin_infos = self.cg.get_coin_by_id(coin["id"])
        description=f"""[{coin['symbol']} Blockchain]({coin_infos['links']['blockchain_site'][0]})

**Current Price:** ```
{round(coin_infos['market_data']['current_price']['eur'], 2)}€
${round(coin_infos['market_data']['current_price']['usd'], 2)}
{round(coin_infos['market_data']['current_price']['sats'], 2)} satoshi
```
**Price Changes:** ```
24h:  {round(coin_infos['market_data']['price_change_percentage_24h'], 2)}%
7d:   {round(coin_infos['market_data']['price_change_percentage_7d'], 2)}%
14d:  {round(coin_infos['market_data']['price_change_percentage_14d'], 2)}%
30d:  {round(coin_infos['market_data']['price_change_percentage_30d'], 2)}%
60d:  {round(coin_infos['market_data']['price_change_percentage_60d'], 2)}%
200d: {round(coin_infos['market_data']['price_change_percentage_200d'], 2)}%
1y:   {round(coin_infos['market_data']['price_change_percentage_1y'], 2)}%
```"""
        embed = discord.Embed(title=coin["name"], url=coin_infos['links']['homepage'][0], description=description)
        embed.set_thumbnail(url=coin_infos['image']['large'])
        await ctx.send(embed=embed)
        
    @commands.command("list_all", hidden=True)
    @commands.is_owner()
    async def list_all_cmd(self, ctx):
        channels = db.get_all_channels()
        response = ""
        for channel in channels:
            try:
                guild: discord.Guild = self.bot.get_guild(channel['guild_id'])
                disc_channel: discord.TextChannel = self.bot.get_channel(channel['channel_id'])
                target_coin = channel['coin']
                response += f"{guild.name}, #{disc_channel.name}: {target_coin}\n"
            except:
                continue
        await ctx.send(response) if response else await ctx.send("None")
        