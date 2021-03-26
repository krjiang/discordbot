# utils file

import discord

# returns last used command
def is_command(commands, cmd):
    if cmd in commands:
        return True
    else: return False