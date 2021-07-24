import discord
from SecretStorage import *
from WEN_SLP import *
from datetime import datetime

now = datetime.now()
client = discord.Client()

@client.event
async def on_ready():
    print('\nWe are logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "$wen":
        current_time = now.strftime("%H:%M:%S")
        print('\n')
        if str(message.author.id) in ScholarsDict:
            # Log actions
            print("Get SLP amount for : " + message.author.name)
            print("Discord ID : " + str(message.author.id))
            print("Current time : ", current_time)

            # Get scholars informations
            botPlaceHolders = ScholarsDict[str(message.author.id)]
            accountPrivateKey = botPlaceHolders[2]
            accountAddress = botPlaceHolders[1]

            # Send the message
            await message.channel.send(
                "------------------------------------------------\n\n" + \
                claim_slp(accountAddress, get_access_token(accountAddress, accountPrivateKey)) + \
                "\n\nhave a good day " + message.author.name + "."
                "\n\n------------------------------------------------\n\n")
            return
        else:
            print("Couldn't claim SLP for : " + message.author.name)
            print("Discord ID : " + str(message.author.id))
            print("Current time : ", current_time)
            return

# Run the client (This runs first)
client.run(DiscordBotToken)