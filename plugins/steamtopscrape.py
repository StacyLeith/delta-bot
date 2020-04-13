from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# vars ready to call
topgames = {}
amount = 20  # arguement for amount of results to return
game_count = 0

# url to open
url = "https://store.steampowered.com/search/?filter=topsellers&os=win"

# open page and grabe raw html with urlopen
uClient = uReq(url)
raw_html = uClient.read()
uClient.close()

# parsing html
pagesoup = soup(raw_html, "html.parser")

# finding the main div class data is in
i = pagesoup.find("div", {"id": "search_resultsRows"})

# finding all the a tags and putting them in a list
containers = i.findAll("a")

# start looping though the a tags
for container in containers:
    if game_count < amount:
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
            elif i.find("£") != -1:
                price = i.strip()  # sets price if it finds £ in the value
            elif i != "":
                release = i  # sets whatever is left thats a valid string to release
            else:
                pass  # ignores all the other stuff
        count = 0  # count var for finding how many £ are in price
        for x in price:
            if x == "£":  # counts the amount of £ in price
                count += 1
        if count == 1:  # sets the normal price if only 1 £
            cprice = price
            sprice = ""
        else:  # splits the price into a list at the £, and assisgns current and sale price
            price_list = price.split("£")
            cprice = price_list[1]
            sprice = price_list[2]
        # sets a dictionary with the games info
        gameinfo = {name: {"releasedate": release, "sale": reduction, "price": cprice, "saleprice": sprice,
                           "link": link}}
        topgames.update(gameinfo)  # updates the main dictionary with the values for the game
        game_count += 1  # adds 1 to game count to control results with an arguement


for x in topgames:  # cycles through the names of the games in the dict
    if topgames[x]["sale"] == "":  # formates if it is not on sale
        print(f"{x}, {topgames[x]['releasedate']}, {topgames[x]['price']}, {topgames[x]['link']}")
    else:  # formats it if it is on sale
        print(f"{x}, {topgames[x]['releasedate']}, {topgames[x]['price']}, {topgames[x]['sale']}, {topgames[x]['saleprice']}, {topgames[x]['link']}")
