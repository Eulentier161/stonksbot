try:
    import uvloop
    uvloop.install()
except ImportError:
    print("Couldn't install uvloop, falling back to the slower asyncio event loop")
import asyncio
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord_slash.context import SlashContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pycoingecko.api import CoinGeckoAPI
import yaml
from cogs import settings
import coin

client = Bot(command_prefix="$")
slash = SlashCommand(client, sync_commands=True)
cg = CoinGeckoAPI()
scheduler = AsyncIOScheduler()
with open('config.yaml', 'r') as f:
    token = yaml.safe_load(f)['token']

@client.event
async def on_ready():    
    print("Ready!")
    
@client.event
async def on_slash_command_error(ctx: SlashContext, ex: Exception):
    await ctx.send(f"```py\n{ex}\n```", hidden=True)

if __name__ == "__main__":    
    # load cogs
    client.add_cog(settings.SettingsCog(client))
    
    # add job
    scheduler.add_job(coin.start_schedule, 'cron', hour="*", args=[client,cg])
    scheduler.start()
    
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(client.run(token))
        loop.run_forever()
    except Exception as aya:
        print(aya)
    