import discord
from datetime import datetime

# Define the expected date format for the thread titles
DATE_FORMAT = '%H:%M - %d-%m'

# Replace the bot token below with your own bot token
server = 0
BOT_TOKEN = "..-"
CHANNEL_ID = 0
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_thread_create(thread):
    # print(f'Logged in as {client.user.name} ({client.user.id})')
    # Retrieve the channel object for the specified channel ID
    # channel = client.get_channel(CHANNEL_ID)
    # for thread in channel.threads:
    #     print(f'Found thread: {thread.name}, {thread.id}')
    message = await thread.fetch_message(thread.id)
    message_content = message.content
    print(message.content)
    if message_content:
        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    # thread.add_user(member.name)
                    if member.name == "soemthing":
                            message = f'New thread found: **{thread.name}**\n\n{message.content}'
                            await member.send(message)


# Run the bot using the bot token
client.run(BOT_TOKEN)
