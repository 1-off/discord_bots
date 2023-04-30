import discord
import logging
from fuzzywuzzy import fuzz, process
import re
import requests
import json

# Configure the "bot" logger
bot_logger = logging.getLogger('bot')
bot_logger.setLevel(logging.ERROR)
bot_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
bot_handler = logging.FileHandler('bot.log')
bot_handler.setFormatter(bot_formatter)
bot_logger.addHandler(bot_handler)

# Configure the "blocked" logger
blocked_logger = logging.getLogger('blocked')
blocked_logger.setLevel(logging.INFO)
blocked_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
blocked_handler = logging.FileHandler('blocked.log')
blocked_handler.setFormatter(blocked_formatter)
blocked_logger.addHandler(blocked_handler)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

webhook_url = ""
server = 0
token = "."


banned_words = []
functional_words = []
allowed_words = []

with open('profanity1.txt', 'r') as file:
    lines = map(str.strip, file.readlines())
    banned_words = list(lines)

with open('functional_words.txt', 'r') as file:
    lines = map(str.strip, file.readlines())
    functional_words = list(lines)

with open('allowed_words.txt', 'r') as file:
    lines = map(str.strip, file.readlines())
    allowed_words = list(lines)

# banned_words = list(filter(lambda x: x.strip(), banned_words))

@client.event
async def on_ready():

    channels = client.get_guild(server)

    for channel in channels.channels:
        

        if isinstance(channel, discord.VoiceChannel):
            continue
        try:
            # await channel.send(f'{client.user} joined the room.')
            ret = client.get_channel(channel.id)
            print(f"{channel}, {channel.id} Joined succesfully")
        except Exception as e:
            print(f"{channel}, {channel.id} not Joined succesfully")
            bot_logger.error(f'Failed to join channel: {channel.name}: {e}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # enable tenor if only gif or remove it to mod all messages
    # if "tenor" in str(message.content).lower():

    for word in str(message.content).lower().split(" "):
        print(word)
        if word in functional_words or word in allowed_words:
            print("allowed")
            continue
        if word in banned_words:
            print("it is a banned word")
            warning_message = ''
            if "tenor" in str(message.content).lower():
                    await message.delete()
                    warning_message = f"The gif has been flagged not appropriate for this server. Therefore, Your message has been reported and the message deleted from {message.channel.name} due to violation of the rules."
            else:
                    warning_message = f"The word [{word}] is a not safe word, and it was found in the sentence: [{message.content}]. Therefore, Your message in the channel {message.channel.name} has been flagged and reported due to violation of the rules."

            await message.author.send(warning_message)

            blocked_logger.info(
                    f"{message.author} used the word {word} in the sentence: [{str(message.content).lower()}] Full text: https://discord.com/channels/{server}/{message.channel.id}/{message.id} in channel {message.channel}")

            payload = {
                    "content": f"{message.author} used the word {word} in the sentence: [{str(message.content).lower()}] Full text:  https://discord.com/channels/{server}/{message.channel.id}/{message.id}"
                }

                # Make the POST request to the webhook URL
            response = requests.post(webhook_url, json=payload)

            return

    similarity_score = 0
    for bad_word in banned_words:
        for token in str(message.content).lower().split(" "):
            if token in allowed_words or token in functional_words:
                continue
            similarity_score = fuzz.token_set_ratio(bad_word, token)
            similarity_score2 = fuzz.ratio(bad_word, token)
                # keep this line for debugging:
                # print(similarity_score,similarity_score2, token,bad_word)

            if similarity_score > 80:
                warning_message = ''
                if "tenor" in str(message.content).lower():
                    warning_message = f"The gif [{bad_word}] has been flagged not appropriate for this server. Therefore, Your message has been reported and the message deleted from {message.channel.name} due to violation of the rules.If this was an error please PM the admin."
                    await message.delete()
                else:
                    warning_message = f"The word [{token}] is a not safe word, and it was found in the sentence: [{message.content}]. Therefore, Your message in the channel {message.channel.name} has been flagged and reported due to violation of the rules. If this was an error please PM the admin."

                    # better to limit this to logging due to the high chance of errors. 
                # await message.author.send(warning_message)

                blocked_logger.info(
                        f"{message.author} used the word {token} in the sentence [{str(message.content).lower()}] which has a with a Similarity score of {similarity_score} to {bad_word}. Full text: https://discord.com/channels/{server}/{message.channel.id}/{message.id}")

                payload = {
                        "content":  f"{message.author} used the word {token} in the sentence [{str(message.content).lower()}] which has a with a Similarity score of {similarity_score} to {bad_word}. Full text: https://discord.com/channels/{server}/{message.channel.id}/{message.id}"
                    }

                response = requests.post(webhook_url, json=payload, headers={
                        "Content-Type": "application/json"})

                return

client.run(token)
