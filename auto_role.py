import discord
from discord.utils import *
from datetime import datetime

# Define the expected date format for the thread titles
DATE_FORMAT = '%H:%M - %d-%m'

# Replace the bot token below with your own bot token
server = 0
BOT_TOKEN = ""
CHANNEL_ID = 0
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():

    channels = client.get_guild(server)
    roles = await client.get_guild(server).fetch_roles()
    # for role in roles:
        # print(role.name, role.id)
    for channel in channels.channels:
        if isinstance(channel, discord.VoiceChannel):
            continue
        try:
            ret = client.get_channel(channel.id)
            text = f"{channel}, {channel.id} Joined succesfully"
            # print(text)
            if channel.id == 1095314360953475154:
                accepted = []
                level2 = []
                level3 = []
                messages = [message async for message in channel.history(limit=200)]
                msg = await channel.fetch_message(messages[1].id)
                for reaction in msg.reactions:
                    print(f"--------------{reaction}--------------")
                    if reaction.emoji == "✅":
                        print(msg.reactions)
                        async for user in reaction.users():
                            accepted.append(user)
                            print(f"{user}, appended {reaction}")
                    if reaction.emoji == "🧙‍♂️":
                        async for user in reaction.users():
                            level3.append(user)
                            print(f"{user}, appended {reaction}")
                    if reaction.emoji == "🧝":
                        async for user in reaction.users():
                            level2.append(user)
                            print(f"{user}, appended {reaction}")
                    print("-"*10)
                for guild in client.guilds:
                    role1 = get(guild.roles, name='Level 1')
                    role2 = get(guild.roles, name='Level 2')
                    role3 = get(guild.roles, name='Level 3')
                    for member in guild.members:
                        if not member.bot:
                            if member in accepted:
                                # member = get(guild.members, id=member.id)
                                if member is not None:
                                    if member in level3:
                                        if role3 in member.roles:
                                            try:
                                                await msg.remove_reaction("🧝", member)
                                            except:
                                                pass
                                            continue
                                        print(f"{member} added to Level 3")
                                        await member.add_roles(role1)
                                        await member.add_roles(role2)
                                        await member.add_roles(role3)
                                        continue
                                    if member in level2 and member not in level3:
                                        if role3 in member.roles:
                                            await member.remove_roles(role3)
                                        if role2 in member.roles:
                                            continue
                                        print(f"{member} added to Level 2")
                                        await member.add_roles(role1)
                                        await member.add_roles(role2)
                                        continue
                                    if member not in level2 and member not in level3:
                                        if role3 in member.roles:
                                            await member.remove_roles(role3)
                                        if role2 in member.roles:
                                            await member.remove_roles(role3)
                                        if role1 in member.roles:
                                            continue
                                        print(f"{member} added to Level 1")
                                        await member.add_roles(role1)
                                        continue
                            else:
                                if member is not None:
                                    await member.remove_roles(role1)
                                    await member.remove_roles(role2)
                                    await member.remove_roles(role3)
                                    # try:
                                    #     message = f'Dear {member.name} due to changes in policy we need you to ✅ the post under the rules ]. Once done you will receive automatically the new role.'
                                    #     ret = await member.send(message)

                                    # except Exception as e:
                                    #     print(e)

        except Exception as e:
            print(e)


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.channel_id == 1095314360953475154:
        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="✅":
            role = get(reaction.member.guild.roles, name='Level 1')
            guild = client.get_guild(server)
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await reaction.member.add_roles(role)


            channels = client.get_guild(server)
            for channel in channels.channels:
                if isinstance(channel, discord.VoiceChannel):
                    continue
                try:
                    if channel.name == "💬main":
                            # if channel.name == "bot-testing":
                        message = await channel.send(f"A new ally joined the server, but the minions of Hell grow stronger!\n Please all welcome <@{reaction.member.id}>")
                            # await message.add_reaction('🧙‍♀️✅')
                except Exception as e:
                    print(e)

        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="🧝":
            role = get(reaction.member.guild.roles, name='Level 2')
            guild = client.get_guild(server)
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await reaction.member.add_roles(role)

                channels = client.get_guild(server)
            for channel in channels.channels:
                if isinstance(channel, discord.VoiceChannel):
                    continue
                try:
                    if channel.name == "💬main":
                            # if channel.name == "bot-testing":
                        message = await channel.send(f"<@{reaction.member.id}> a mighty hero joined the ranks of level 2.")
                            # await message.add_reaction('🧙‍♀️✅')
                except Exception as e:
                    print(e)

        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="🧙‍♂️":
            role3 = get(reaction.member.guild.roles, name='Level 3')
            role2 = get(reaction.member.guild.roles, name='Level 2')
            guild = client.get_guild(server)
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await reaction.member.add_roles(role3)
                await reaction.member.add_roles(role2)


                channels = client.get_guild(server)
                for channel in channels.channels:
                    if isinstance(channel, discord.VoiceChannel):
                        continue
                    try:
                        if channel.name == "💬main":
                                # if channel.name == "bot-testing":
                            message = await channel.send(f"<@{reaction.member.id}> a mighty hero joined the ranks of level 3.")
                                # await message.add_reaction('🧙‍♀️✅')
                    except Exception as e:
                        print(e)


@client.event
async def on_raw_reaction_remove(reaction):
    if reaction.channel_id == 1095314360953475154:
        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="✅":
            print(reaction)
            guild_id = reaction.guild_id
            guild = client.get_guild(reaction.guild_id)
            role1 = get(guild.roles, name='Level 1')
            role2 = get(guild.roles, name='Level 2')
            role3 = get(guild.roles, name='Level 3')
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await member.remove_roles(role1)
                await member.remove_roles(role2)
                await member.remove_roles(role3)
        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="🧝":
            print(reaction)
            guild_id = reaction.guild_id
            guild = client.get_guild(reaction.guild_id)
            role1 = get(guild.roles, name='Level 1')
            role2 = get(guild.roles, name='Level 2')
            role3 = get(guild.roles, name='Level 3')
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await member.remove_roles(role2)
        if str(reaction.emoji).replace(' ', '').replace('\n', '') =="🧙‍♂️":
            print(reaction)
            guild_id = reaction.guild_id
            guild = client.get_guild(reaction.guild_id)
            role3 = get(guild.roles, name='Level 3')
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                await member.remove_roles(role3)


client.run(BOT_TOKEN)
