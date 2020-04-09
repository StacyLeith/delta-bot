# ### IMPORTS ###

import discord  # IMPORTS DISCORD.PY
from discord.ext import commands  # IMPORTS COMMANDS MODULE FOR BOT
from config.botcfg import TOKEN, GAME, PREFIX, ADMINS  # IMPORTS VARIABLES FROM BOTCFG.PY


# ### STARTUP ###


bot = commands.Bot(command_prefix=PREFIX) # ASSIGNS CLIENT AS BOT AND SETS COMMAND PREFIX


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


# ### COGS & COMMANDS ###

class ExtensionManager(commands.Cog):  # DEFINING THIS CLASS AND MAKING IT A COG

    @commands.command(hidden=True)  # HIDDEN COMMAND TO RELOAD EXTENSION, ONLY OWNER
    async def reload(self, ctx, ext):
        if str(ctx.author) in ADMINS:  # CHECKS IF AUTHOR IS BOT OWNER
            try:  # TRIES TO LOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
                bot.reload_extension(ext)
                await ctx.send(f"{ext} extention has been reloaded Boss")
            except discord.ext.commands.ExtensionNotLoaded:
                await ctx.send("Unable to reload extension Boss, check extension name")
        else:
            await ctx.send(f"{ctx.author.mention} you do not have permission to perform this action")

    @reload.error  # ERROR HANDLER FOR RELOAD COMMAND MISSING ARGUEMENTS
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to reload Boss")

    @commands.command(hidden=True)
    async def unload(self, ctx, ext):
        if str(ctx.author) in ADMINS:  # CHECKS IF AUTHOR IS BOT OWNER
            try:  # TRIES TO UNLOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
                bot.unload_extension(ext)
                await ctx.send(f"{ext} extention has been unloaded Boss")
            except discord.ext.commands.ExtensionNotLoaded:
                await ctx.send("Unable to unload extension Boss, check extension name")
        else:
            await ctx.send(f"{ctx.author.mention} you do not have permission to perform this action")

    @unload.error  # ERROR HANDLER FOR UNLOAD COMMAND MISSING ARGUEMENTS
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to unload Boss")

    @commands.command(hidden=True)
    async def load(self, ctx, ext):
        if str(ctx.author) in ADMINS:  # CHECKS IF AUTHOR IS BOT OWNER
            try:  # TRIES TO LOAD GIVEN EXTENSION, HANDLES ERROR IS NOT FOUND
                bot.load_extension(ext)
                await ctx.send(f"{ext} extention has been loaded Boss")
            except discord.ext.commands.ExtensionNotLoaded:
                await ctx.send("Unable to load extension Boss, check extension name")
        else:
            await ctx.send(f"{ctx.author.mention} you do not have permission to perform this action")

    @load.error  # ERROR HANDLER FOR LOAD COMMAND MISSING ARGUEMENTS
    async def load_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide extension name to load Boss")



# ### RUNNING THE BOT, NEEDS TO STAY AS LAST LINE OF CODE! ###

bot.add_cog(ExtensionManager(bot))
print("Extension Manager loaded successfully!")
bot.run(TOKEN)  # RUNS BOT WITH LOGIN TOKEN


# ### LEGACY HELP CODE ###

# @client.event
# async def on_message(message): # FIRES WHEN A MESSAGE IS RECIEVED
#     if message.content == "!help": # LOOKS TO SEE IF THE MESSAGE IS !HELP
#         help_msg = get_help() # CALLS GET_HELP FUNCTION TO GENERATE A HELP FILE
#         await message.channel.send(content=None, embed=help_msg) # SENDS THE HELP FILE TO THE CHANNEL AS AN EMBED
#
# def get_help():
#     help_dict = { # DICTIONARY CONTAINING ALL THE COMMANDS AND THEIR HELP TEXT
#         '!help': 'This is the help command you just used, dumbass',
#         '!status': 'Brings up server status for the currently assigned game server',
#         '!serverid [id]': 'Sets the currently assigned game server with the servers Battlemetrics ID'
#     }
#     help_msg = discord.Embed(title="NimaBot", description="Currently in developement by Stacy Leith")
#     for key in help_dict: # CYCLES THROUGH EACH KEY IN THE DICTIONARY
#         help_msg.add_field(name=key, value=help_dict[key]) # ADDS EACH KEYS NAME AND DESCRIPTION TO THE HELP EMBED
#     return help_msg # RETURNS THE COMPLETED HELP FILE EMBED TO WHEREVER CALLED THE FUNCTION

# ### MY EXAMPLE COMMANDS ###

# @bot.command(name="test",
#              help="long help text goes here man",
#              brief="short help text",
#              usage="arguments for usage here",
#              aliases=["other", "names"],
#              enabled=True,
#              description="description when command is searched in help",
#              hidden=False
#              )
# async def test(ctx):
#     await ctx.send("yo yo")
#
# @bot.command()
# async def largs(ctx, *args):
#     await ctx.send(f"{len(args)} Arguments given: {', '.join(args)}")
#
# @bot.command()
# async def args(ctx, *, args):
#     await ctx.send(args)
#
# @bot.command()
# async def margs(ctx, arg1, arg2, arg3):
#     await ctx.send(f"{arg3} {arg2} {arg1}")
