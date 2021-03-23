import pandas as pd
import random
import discord
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents().all()
client = discord.Client(intents=intents)

# shows that the bot is active
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!'):
        cmd = message.content.split()[0].replace('!', '')
        if len(message.content.split()):
            parameters = message.content.split()[1:]
    
        # SCAN command: takes in the previous 10,000 messages in the channel the command was called in
        #               and creates a data.csv file containing the content, date, and author of each message.
        if cmd == 'scan':
            data = pd.DataFrame(columns = ['content', 'date', 'author'])

            # checks to see if the message is a '!scan' command
            def is_command(msg):
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '!scan':
                    return True
                else:
                    return False
            
            async for msg in message.channel.history(limit = float('inf')):
                if not is_command(msg):
                    data = data.append({'content': msg.content,
                                        'date': msg.created_at,
                                        'author': msg.author}, ignore_index=True)
                    if len(data) == 10000:
                        break
            
            file_location = 'data.csv'
            data.to_csv(file_location)

        # INHOUSE command: checks to see which channel the user is in and assigns random teams based
        #                  on the users in the channel, tells you to use !reroll for new teams
        if cmd == 'inhouse':
            voiceChannel = message.author.voice.channel
            textChannel = message.channel
            channelMembers = voiceChannel.members
            print(channelMembers)
            random.shuffle(channelMembers)
            teamsize = len(channelMembers) // 2
            team1 = channelMembers[teamsize:]
            team2 = channelMembers[:teamsize]
            permutations = [team1]

            team1 = [member.name for member in team1]
            team2 = [member.name for member in team2]
            string = 'TEAM 1: \n'
            for member in team1:
                string += member + '\n'
            string += '\n TEAM 2: \n'
            for member in team2:
                string += member + '\n'
            
            await textChannel.send(string)
            
'''
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        general = client.get_channel(822902651048951841)
        await general.send('hello ' + member.name)
'''

client.run('token')