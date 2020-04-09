# ### IMPORTS ###

import discord  # IMPORTS DISCORD.PY
from discord.ext import commands  # IMPORTS COMMANDS MODULE FOR BOT
from config.botcfg import TOKEN, GAME, PREFIX  # IMPORTS VARIABLES FROM BOTCFG.PY
import json


# ### STARTUP ###


bot = commands.Bot(command_prefix=PREFIX) # ASSIGNS CLIENT AS BOT AND SETS COMMAND PREFIX
owner_id = int(108205719324483584)


# ### LOADING EXTENTIONS ###


bot.load_extension("plugins.serverstatus")
bot.load_extension("plugins.modcmds")


# ### ON READY FUNCTION ###


@bot.event
async def on_ready():  # FIRES WHEN BOT IS LOGGED IN AND READY
    print(f"NimaBot loaded with presence set as playing {GAME}, {PREFIX} as the command prefix. Ready to go!")
    # PRINTS READY
    game = discord.Game(GAME)  # SETS GAME BOT IS PLAYING FROM BOTCFG
    await bot.change_presence(status=discord.Status.online, activity=game)
    # CHANGES THE BOTS PRESENCE TO "PLAYING WHATEVER BOT CFG TELLS ME"


# ### COMMANDS ###


@commands.is_owner()
@bot.command()
async def extensions(ctx):
    statusmsg = discord.Embed(title="Bot Extension Status", description=None)
    with open('data/status.json', "r") as f:
        data = json.load(f)
        for key in data:
            statusmsg.add_field(name="Name:", value=data[key]["Name"])
            statusmsg.add_field(name="Path:", value=data[key]["Path"])
            statusmsg.add_field(name="Status:", value=data[key]["Status"])
    await ctx.send(content=None, embed=statusmsg)


# ### COGS ###


class ExtensionManager(commands.Cog, name="Extension Manager Plugin"):  # DEFINING THIS CLASS AND MAKING IT A COG

    # ### COMMANDS ###

    @commands.is_owner()
    @commands.command(hidden=True)  # HIDDEN COMMAND TO RELOAD EXTENSION, ONLY OWNER
    async def reload(self, ctx, ext):
        try:  # TRIES TO LOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
            bot.reload_extension(ext)
            await ctx.send(f"{ext} extention has been reloaded Boss")
        except discord.ext.commands.ExtensionNotLoaded:
            await ctx.send("Unable to reload extension Boss, check extension name")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, ext):
        try:  # TRIES TO UNLOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
            bot.unload_extension(ext)
            await ctx.send(f"{ext} extention has been unloaded Boss")
        except discord.ext.commands.ExtensionNotLoaded:
            await ctx.send("Unable to unload extension Boss, check extension name")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, ext):
        try:  # TRIES TO LOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
            bot.load_extension(ext)
            await ctx.send(f"{ext} extention has been loaded Boss")
        except discord.ext.commands.ExtensionNotLoaded:
            await ctx.send("Unable to load extension Boss, check extension name")

    # ### ERROR HANDLERS ###

    @load.error  # ERROR HANDLER FOR LOAD COMMAND MISSING ARGUEMENTS
    async def load_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to load Boss")

    @reload.error  # ERROR HANDLER FOR RELOAD COMMAND MISSING ARGUEMENTS
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to reload Boss")

    @unload.error  # ERROR HANDLER FOR UNLOAD COMMAND MISSING ARGUEMENTS
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to unload Boss")


# ### RUNNING THE BOT, NEEDS TO STAY AS LAST LINE OF CODE! ###


bot.add_cog(ExtensionManager(bot))
print("Extension Manager loaded successfully!")
bot.run(TOKEN)  # RUNS BOT WITH LOGIN TOKEN
