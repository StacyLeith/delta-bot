import discord
from discord.ext import commands  # IMPORTS COMMANDS MODULE
import requests
import json


# ### CLASSES ###


class Server:  # set server class
    number_of_servers = 0  # class variable
    server_list = []  # class variable

    def __init__(self, sid):  # atributes for each server when created
        self.sid = str(sid)  # give the server its id

    def pullserverinfo(self):  # pulls server info from battlemetrics api and formats into a list
        url = 'https://api.battlemetrics.com/servers/' + self.sid
        payload = "fields[server]=name%2Cip%2Cport%2Cplayers%2CmaxPlayers%2Cstatus"
        i = requests.get(url, params=payload)
        if i.status_code == requests.codes.ok:
            j = json.loads(i.text)
            return j["data"]["attributes"]
        else:
            return None


# ### COGS AND COMMANDS ###


class ServerStatus(commands.Cog, name="Server Status Plugin"):  # DEFINING THIS CLASS AND MAKING IT A COG

    server = Server(0)

    @commands.command(brief="Used to set a game server id",
                      usage="<Battlemetrics Server ID>",
                      enabled=True,
                      description="Using this command sets up the server status plugin. Once you have entered your "
                                  "server ID, you will be able to check server status, etc.",
                      hidden=False
                      )
    async def addserver(self, ctx, sid):  # DEFINES THE ADD SERVER COMMAND
        self.server = Server(sid)
        try:  # CHECKS IF THE ID IS VALID WITH THE BM API, EXCEPTS ERROR IF IT ISN'T
            name = self.server.pullserverinfo()["name"]
            serverstatus = discord.Embed(title="Success!", description="Server has been added.")
            serverstatus.add_field(name="ID", value=str(sid))
            serverstatus.add_field(name="Name", value=name)
            await ctx.channel.send(content=None, embed=serverstatus)
        except TypeError:
            await ctx.channel.send(
                    "Add server failed. Please give a valid Battlemetrics Game Server ID")
            # ERROR MESSAGE IF GIVEN AN INVALID ID

    @addserver.error
    async def addserver_error(self, ctx, error):  # ERROR HANDLER FOR ADDSERVER COMMAND MISSING ARGUEMENTS
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Add server failed. Please give a valid Battlemetrics Game Server ID")

    @commands.command(brief="",
                      enabled=True,
                      description="",
                      hidden=False
                      )
    async def status(self, ctx):  # SERVER STATUS COMMAND, PULLS FROM API AND EMBEDS INFO
        try:
            serverstatus = discord.Embed(title=self.server.pullserverinfo()["name"], value=self.server.sid)
            serverstatus.add_field(name="Server IP",
                                   value=f"{self.server.pullserverinfo()['ip']}:{self.server.pullserverinfo()['port']}")
            serverstatus.add_field(name="Status", value=self.server.pullserverinfo()['status'])
            serverstatus.add_field(name="Players",
                                   value=f"{self.server.pullserverinfo()['players']}"
                                         f"/{self.server.pullserverinfo()['maxPlayers']}")
            await ctx.channel.send(content=None, embed=serverstatus)
        except TypeError:
            await ctx.channel.send("No Valid Server ID found")


# ### SETUP AND TEARDOWN FUNCTIONS ###

def setup(bot):  # SETUP FUNCTION TO INITIALISE THE EXTENTION
    bot.add_cog(ServerStatus(bot))  # TELLS THE BOT TO ADD THE COG
    print("Server Status Plugin loaded successfully!")  # TELLS ME IT'S LOADED OK


def teardown(bot):  # TEARDOWN FUNCTION FIRES ON EXTENSION UNLOAD
    print('Server Status Plugin unloaded!')