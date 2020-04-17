from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from discord.ext import commands  # IMPORTS COMMANDS MODULE
import json
import typing
import discord


def change_status(newstat):
    with open('data/status.json', "r") as f:
        data = json.load(f)
    data["ext3"]["Status"] = newstat
    with open('data/status.json', "w") as f:
        json.dump(data, f)


def scrapesteam():  # function to scrape steams top sellers by amount given
    # url to open
    url = "https://store.steampowered.com/search/?filter=topsellers&os=win"
    # open page and grabe raw html with urlopen
    uclient = uReq(url)
    raw_html = uclient.read()
    uclient.close()
    # parsing html
    pagesoup = soup(raw_html, "html.parser")
    # finding the main div class data is in
    i = pagesoup.find("div", {"id": "search_resultsRows"})
    # finding all the a tags and putting them in a list
    containers = i.findAll("a")
    # vars ready to call
    topgames = {}
    game_count = 0
    # start looping though the a tags
    for container in containers:
        name = ""  # variables set to call
        price = ""
        release = ""
        reduction = ""
        link = container['href']  # find the game page link
        info = container.text.split("\n")  # takes containers text and splits into list
        info[:] = [x for x in info if x]  # removes empty values from the list
        for c, i in enumerate(info):  # counts through each list item
            i = i.rstrip()
            if c == 0:
                name = i  # assigns first value as the game name
            elif i == " ":
                info.remove(i)  # removes values with just white space
            elif i.find("%") != -1:
                reduction = i  # sets reduction if it finds % in the value
            elif i.find("€") != -1:
                price = i.strip()  # sets price if it finds £ in the value
            elif i != "":
                release = i  # sets whatever is left thats a valid string to release
            else:
                pass  # ignores all the other stuff
        count = 0  # count var for finding how many £ are in price
        for x in price:
            if x == "€":  # counts the amount of £ in price
                count += 1
        if count == 1:  # sets the normal price if only 1 £
            cprice = price
            sprice = ""
        elif count == 0:
            cprice = ""
            sprice = ""
        else:  # splits the price into a list at the £, and assisgns current and sale price
            price_list = price.split("€")
            cprice = price_list[1]
            sprice = price_list[2]
        # sets a dictionary with the games info
        gameinfo = {name: {"releasedate": release, "sale": reduction, "price": cprice, "saleprice": sprice,
                           "link": link}}
        topgames.update(gameinfo)  # updates the main dictionary with the values for the game
        game_count += 1  # adds 1 to game count to control results with an arguement
    return topgames


class SteamScrape(commands.Cog):  # DEFINING THIS CLASS AND MAKING IT A COG
    @commands.command()
    async def steamtop(self, ctx, arg: typing.Optional[int]):
        topgames = scrapesteam()
        steamscrape = discord.Embed(title="Top 10 Games on Steam", value="Use !steamtop <number> for details & link")
        if arg == int:
            pass
        else:
            for c, x in enumerate(topgames, 1):  # cycles through the names of the games in the dict
                if topgames[x]["sale"] == "":  # formates if it is not on sale
                    steamscrape.add_field(name=f"#{c}", value=f"{x}: {topgames[x]['price']}")
                    c += 1
                    if c == 11:
                        break
                else:  # formats it if it is on sale
                    steamscrape.add_field(name=f"#{c}", value=f"{x}:{topgames[x]['sale']} = €{topgames[x]['saleprice']}")
                    c += 1
                    if c == 11:
                        break
            await ctx.channel.send(content=None, embed=steamscrape)


def setup(bot):  # SETUP FUNCTION TO INITIALISE THE EXTENTION
    bot.add_cog(SteamScrape(bot))  # TELLS THE BOT TO ADD THE COG
    change_status("loaded")
    print("Steam Scrape Plugin loaded")  # TELLS ME IT'S LOADED OK


def teardown(bot):  # TEARDOWN FUNCTION FIRES ON EXTENSION UNLOAD
    change_status("unloaded")
    print('Steam Scrape Plugin extension unloaded!')
