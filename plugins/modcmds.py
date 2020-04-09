import discord
from discord.ext import commands
import typing


# ### COGS AND COMMANDS ###


class ModCommands(commands.Cog):  # MOD COMMANDS COG

    # ### COMMANDS ###

    @commands.command(help="long help text goes here man",
                      brief="short help text",
                      usage="arguments for usage here",
                      description="description when command is searched in help",
                      )
    @commands.has_permissions(kick_members=True)  # CHECKS IF USER HAS PERMISSIONS
    async def kick(self, ctx):
        try:
            victim = ctx.message.mentions[0]  # SETS VICTIM TO MENTIONED USERS ID
            try:
                await discord.Member.kick(victim, reason=None)  # KICKS USER ID IN VICTIM
            except discord.Forbidden:  # EXCEPTS ERROR WHEN BOT CAN'T KICK USER DUE TO PERMS
                await ctx.send(f"{ctx.author.mention} I do not have permissions to kick {victim.mention}")
        except IndexError:  # EXCEPTS ERROR WHEN USER NOT FOUND
            await ctx.send(f"{ctx.author.mention} No member given or member not found")

    @commands.command(help="long help text goes here man",
                      brief="short help text",
                      usage="arguments for usage here",
                      description="description when command is searched in help",
                      )
    @commands.has_permissions(manage_messages=True)  # CHECKS IF USER HAS PERMISSIONS
    async def clear(self, ctx, arg: typing.Optional[int] = 10):
        # LOOKS FOR INTEGAR ARGUEMENT, DEAULTS TO 10 IF NOT FOUND
        limit = int(arg) + 1  # ADDS 1 TO ACCOUNT FOR CLEAR MSG
        chan = ctx.message.channel  # CALLS CHANNEL ID
        delete = await discord.TextChannel.purge(chan, limit=limit, bulk=True)
        # DELETES MESSAGES AND RETURNS NUMBER DELETED
        await ctx.send(f"{len(delete) - 1} messages delete by {ctx.author.mention}")

    @commands.command(help="long help text goes here man",
                      brief="short help text",
                      usage="arguments for usage here",
                      description="description when command is searched in help",
                      )
    @commands.has_permissions(ban_members=True)  # CHECKS IF USERS HAS PERMISSIONS
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                  delete_days: typing.Optional[int] = 0, *,
                  reason: str):
        # APPENDS ALL MENTIONS INTO MEMBERS LIST, AND DEFAULTS 0 IN NO LENGTH GIVEN
        if len(members) != 0:  # IF NO LENGTH GIVEN, BANS AND LISTS RIGHT NAME
            for member in members:
                await member.ban(delete_message_days=delete_days, reason=reason)
        else:
            if delete_days == 0:
                await ctx.send(f"Ban failed, could not find member {ctx.message.content.split()[1]}")
            else:
                # IF LENGTH IS GIVEN, LISTS CORRECT NAME
                await ctx.send(f"Ban failed, could not find member {ctx.message.content.split()[2]}")

    @commands.command(help="long help text goes here man",
                      brief="short help text",
                      usage="arguments for usage here",
                      description="description when command is searched in help",
                      )
    async def purge(self, ctx, victim: discord.Member, amount: typing.Optional[int] = 10):
        # TAKES VICTIM NAME AND AMOUNT OF MSGS, DEFAULTS TO 10
        msglist = []  # INITIATES A MESSAGE LIST
        messages = await ctx.channel.history(limit=None).flatten()  # GETS CHANNELS MESSAGE HISTORY
        for message in messages:  # ITERATES THROUGH HISTORY SET AMOUNT OF TIMES AND APPENDS MSG ID IF USER MATCHES
            if message.author == victim and amount != 0:
                msglist.append(message)
                amount -= 1
            else:
                pass
        chan = ctx.message.channel  # CALLS CHANNEL ID
        await discord.TextChannel.delete_messages(chan, messages=msglist)  # DELETES ALL MESSAGES FOUND
        await ctx.send(f"{ctx.author.mention} deleted the last {len(msglist)} messages by {victim.mention}")


# ### ERROR HANDLERS ###

    @purge.error
    async def purge_error(self, ctx, error):  # ERROR HANDLER FOR CLEAR NO PERMISSIONS
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.channel.send(f"{ctx.author.mention} please specify a valid Discord User")

    @ban.error
    async def ban_error(self, ctx, error):  # ERROR HANDLER FOR CLEAR NO PERMISSIONS
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f"{ctx.author.mention} please specify a valid Discord User")
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} you do not have permission to use this command")

    @clear.error
    async def clear_error(self, ctx, error):  # ERROR HANDLER FOR CLEAR NO PERMISSIONS
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} you do not have permission to use this command")

    @kick.error
    async def kick_error(self, ctx, error):  # ERROR HANDLER FOR KICK NO PERMISSIONS
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} you do not have permission to use this command")


# ### SETUP AND TEARDOWN ###


def setup(bot):
    bot.add_cog(ModCommands(bot))
    print("Mod Commands Plugin extension loaded")


def teardown(bot):
    print('Mod Commands Plugin extension unloaded!')