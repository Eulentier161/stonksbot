try:
    import uvloop
    uvloop.install()
except ImportError:
    print("Couldn't install uvloop, falling back to the slower asyncio event loop")
import asyncio
import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord_slash.context import ComponentContext, SlashContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pycoingecko.api import CoinGeckoAPI
import yaml
from cogs import settings
import coin

client = Bot(command_prefix="$", help_command=None)
slash = SlashCommand(client, sync_commands=True)
cg = CoinGeckoAPI()
scheduler = AsyncIOScheduler()
with open('config.yaml', 'r') as f:
    token = yaml.safe_load(f)['token']

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the stonks market"))
    print("Ready!")
    
@client.event
async def on_slash_command_error(ctx: SlashContext, ex: Exception):
    await ctx.send(f"```py\n{ex}\n```", hidden=True)

@slash.component_callback()
async def info_btn(ctx: ComponentContext):
    await coin.info_callback(ctx, cg)


if __name__ == "__main__":    
    # load cogs
    client.add_cog(settings.SettingsCog(client))
    
    # add job
    scheduler.add_job(coin.start_schedule, 'cron', minute="*", args=[client,cg])
    scheduler.start()
    
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(client.run(token))
        loop.run_forever()
    except Exception as e:
        print(e)
    