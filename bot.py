import discord


from send_message import MessageListener
from settings import DISCORD_TOKEN

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(client.guilds)
    print(client.guilds[0].members)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_listner = MessageListener(message.author)
    reply_message = message_listner.send_message(message.content)
    await message.channel.send(reply_message)


client.run(DISCORD_TOKEN)
