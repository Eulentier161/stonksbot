import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext
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
            text = ""
            for coin in self.coins_list:
                text += f"id: {coin['id']}, name: {coin['name']}, symbol: {coin['symbol']}\n"
            with open("ids.txt", "a") as f:
                f.write(text)
            with open("ids.txt", "rb") as f:
                await ctx.reply(f"`{target_coin}` is not a valid id. here is a textfile with all available coins and their corresponding ids.", file=discord.File(f, "ids.txt"))
            os.remove("ids.txt")
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
        