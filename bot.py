import discord


from send_message import MessageListener
from settings import DISCORD_TOKEN

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(client.guilds)


@client.event
async def on_message(message):
    # To check if the message is sent by discord Bot or another user.
    if message.author == client.user:
        return

    message_listner = MessageListener(message.author)
    reply_message = message_listner.send_message(message.content)
    await message.channel.send(reply_message)


client.run(DISCORD_TOKEN)
