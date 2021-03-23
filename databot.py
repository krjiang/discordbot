import pandas as pd
import discord
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

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

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        general = client.get_channel(822902651048951841)
        await general.send('hello ' + member.name)

client.run('token')