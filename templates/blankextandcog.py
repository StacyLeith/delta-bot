from discord.ext import commands  # IMPORTS COMMANDS MODULE


class COGNAME(commands.Cog):  # DEFINING THIS CLASS AND MAKING IT A COG

    @commands.Cog.listener()  # A LISTENER WITHIN THE COG
    async def on_message(self, ctx):  # FIRES WHENEVER A MESSAGE IS SENT, AND PASSES IN CONTEXT
        pass

    @commands.command()  # A COMMAND IN A COG
    async def test(self, ctx):  # DEFINES THE COMMAND
        pass


# ### ONLY USE THESE IF EXTENSION ###


def setup(bot):  # SETUP FUNCTION TO INITIALISE THE EXTENTION
    bot.add_cog(COGNAME(bot))  # TELLS THE BOT TO ADD THE COG
    print("extension loaded")  # TELLS ME IT'S LOADED OK


def teardown(bot):  # TEARDOWN FUNCTION FIRES ON EXTENSION UNLOAD
    print('extension unloaded!')
