import discord
from discord import Embed
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = 'gw!', intents=intents)

'''
Everything is hard coded and extremely messy because I'm lazy. This is basically just Gwent Lazy Bot but reworked so I can meme with my friends lol.
View the Gwent lazy bot's repository here: https://github.com/MasterAbdoTGM50/gwent-lazy-bot
Go and play Gwent, it's a fun game!
'''

# defining our wonderful dictionary
factionColours = {
    "Neutral": 0x7f6000,
    "Monster": 0xc56c6c,
    "Nilfgaard": 0xf0d447,
    "Northern Realms": 0x48c1ff,
    "Scoia'tael": 0x2abd36,
    "Skellige": 0xad39ec,
    "Syndicate": 0xe67e22
}

class CardInfo:
    '''
    Class that holds all the card information needed to print out a Discord message.
    Includes a constructor and functions to change individual parameters of the class.
    '''
    def __init__(self, faction1, faction2, rarity, nickname, cardUrl):
        self.name = nickname                    # Card name. Also includes faction(s). Hardcoded.
        self.faction1 = faction1                # used to determine colour of the message embed that will be sent. Type: string
        self.faction2 = faction2                # only used if the card is one of those dual SY cards, by default this will be an empty string
                                                # note: SY is always the primary faction of dual cards
        self.rarity = rarity                    # common, epic, legendary, etc etc
        self.cardDesc = ''                      # initialize as blank string
        self.provPower = ''                     # initialize as blank string
        self.flavourText = ''                   # initialize as blank string
        self.cardUrl = cardUrl                  # URL on gwent.one

        # I'm not initializing cardDesc, provPower, and flavourText here otherwise there would just be too much text to copy and paste in... (note this is hardcoded)

    def changeCardDesc(self, cardDesc):         # update card description for printing
        self.cardDesc = cardDesc

    def changeProvPower(self, provPower):       # update card provision and power for printing
        self.provPower = provPower

    def changeFlavourText(self, flavourText):   # update card flavour text
        self.flavourText = flavourText


def buildCard(embed, cardInfo, cardThumbnail):
    '''
    Input args:
        cardInfo: holds a CardInfo object that contains all the card's information. To be used for printing.
        cardThumbnail: card's thumbnail, pulled from gwent.one. Hardcoded.
        
        I want to generalize this as much as possible without implementing a card search algorithm.
    Output:
        A Discord embedded message that hopefully looks like the Gwent lazy bot's embedded message.
    Usage:
        To be called whenever a user sends a message formatted like so: [carrold]
    '''
    global factionColours

    # Setting header of card
    if cardInfo.faction2 == '':     # card is one faction only
        embedAuthor = ("%s - %s Unit" %(cardInfo.faction1, cardInfo.rarity))
    else:                           # card is dual-faction
        embedAuthor = ("%s & %s - %s Unit" %(cardInfo.faction1, cardInfo.faction2, cardInfo.rarity))
    
    # Setting url of card:
    embedUrl = cardInfo.cardUrl

    # Setting embed sidebar colour
    sidebarColour = factionColours[cardInfo.faction1]

    # Setting embed thumbnail
    embedThumbnail = cardThumbnail

    # Setting card title
    embedTitle = cardInfo.name
    
    # Setting card text
    embedText = ("%s\n\n\n%s\n\n\n*%s*" %(cardInfo.cardDesc, cardInfo.provPower, cardInfo.flavourText))

    # Building the embedded message
    embed = Embed(title=embedTitle, url=embedUrl, description=embedText, color=sidebarColour)
    embed.set_author(name=embedAuthor)
    embed.set_thumbnail(url=embedThumbnail)

    return embed
   
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    startupMessage = "FOR THIS MOST BEAUTIFUL OF MAIDENS I SHALL FIGHT A HUNDRED DUELS"
    await client.change_presence(activity = discord.Streaming(name = startupMessage, url = "https://github.com/Vithraldor/"))


# Commands
@client.command()
async def info(ctx):
    embed = Embed(title="Gwont Super Lazy Bot", description="Developed by Ashley/Vith! To request a new feature just DM them :)", color=0x042069)
    embed.add_field(name="GitHub Link", value="https://github.com/Vithraldor/Gwont-Super-Lazy-Bot", inline=False)
    embed.add_field(name="Gwent Lazy Bot", value="Based off of the Gwent Lazy Bot: https://github.com/MasterAbdoTGM50/gwent-lazy-bot", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ronvid(ctx):
    random.seed()
    probabilityValue = int(random.random() * 100)
        
    if probabilityValue <= 33:
        await ctx.send('FOR THIS MOST BEAUTIFUL OF MAIDENS I SHALL FIGHT A HUNDRED DUELS!')

    elif probabilityValue > 33 and probabilityValue <= 66:
        await ctx.send("FOR MAID BILBERRY'S HONOUR!")

    else:
        await ctx.send("BLOOD ALONE CAN MY MAID'S HONOUR UNBESMIRCH!")

@client.command()
async def master(ctx):
    await ctx.send("Take a look at this link to see all of our resources: https://docs.google.com/spreadsheets/d/1sHyniAWVV0gAi39Wzckwl-axwMRlvKq-HnTGuHgkB90/edit?usp=sharing (currently only has tournament decks and Ashley's homebrews, we'll update it when we're not lazy!)")

@client.command()
async def roadmap(ctx):
    await ctx.send("https://static.cdprojektred.com/cms.cdprojektred.com/crystal-news/8cccb8946f2e69bb8a929c58dbd971091ca7115d.jpg")

# Automatic interactions done by the bot:
@client.event
async def on_message(message):
    # Allows the bot to both process commands and actively read input.
    await client.process_commands(message)

    # Create dummy embed variable, used with the buildCard function
    embed = Embed(title='fgsd', description='fsgd', color=discord.Color.blue())

    # Checks if the message was sent by an actual user so the bot won't respond to itself
    if message.author == client.user:
        return

    if str.lower(message.content) == "[broken elf]": 
        # This activates Gezras' description
        gezrasCard = CardInfo("Scoia'tael", '', 'Legendary', 'Gezras of Leyda - Witcher', 'https://gwent.one/en/card/202801')
        
        cardDesc = "Melee: At the end of your turn, move self to the Ranged row and boost a random allied unit on this row by 1.\nRanged: At the end of your turn, move self to the Melee row and damage a random enemy unit on the opposite row by 1.\nAdrenaline 3: Instead of a random unit, affect all other units in a row."
        gezrasCard.changeCardDesc(cardDesc)

        provPower = "Provision: 12\nPower: 5"
        gezrasCard.changeProvPower(provPower)

        flavourText = "“Take a contract from Aen Seidhe over a dh'oine any day, as you’re far less likely to receive a knife between the ribs in place of coin.” ⁠— Gezras"
        gezrasCard.changeFlavourText(flavourText)

        await message.channel.send(embed=buildCard(embed, gezrasCard, "https://gwent.one/img/assets/medium/art/2335.jpg"))

    elif str.lower(message.content) == "[carold]" or str.lower(message.content) == "[carrold]":
        # This activates Harald Gord's description
        haraldCard = CardInfo("Syndicate", "Scoia'tael", 'Epic', 'Harald Gord - Dwarf, Crownsplitters', 'https://gwent.one/en/card/202383')

        cardDesc = "Deploy: Boost self by 0.\nIncrease the boost by 1 for every special card you played this game.\nBoost cannot exceed 12."
        haraldCard.changeCardDesc(cardDesc)

        provPower = "Provision: 7\nPower: 3"
        haraldCard.changeProvPower(provPower)

        flavourText = "The last occasion Harald's grim countenance betrayed a smile was in 1211 when Brouver Hoog drunkenly ate five bowls of goat and cabbage stew then promptly shat his trousers."
        haraldCard.changeFlavourText(flavourText)

        await message.channel.send(embed=buildCard(embed, haraldCard, "https://gwent.one/img/assets/medium/art/1873.jpg"))

    elif str.lower(message.content) == "[best]":
        # This activates Knickers' description
        knickersCard = CardInfo("Neutral", '', 'Legendary', 'Knickers - Beast, Bandit', 'https://gwent.one/en/card/202397')

        cardDesc = "This unit may raid the battlefield to aid you in battle."
        knickersCard.changeCardDesc(cardDesc)

        provPower = "Provision: 7\nPower: 3\nArmor: 1"
        knickersCard.changeProvPower(provPower)

        flavourText = "Leave it alone, Knickers! Damn it, leave it alone!"
        knickersCard.changeFlavourText(flavourText)

        await message.channel.send(embed=buildCard(embed, knickersCard, "https://gwent.one/img/assets/medium/art/1684.jpg"))


client.run('')
