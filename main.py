import discord
import asyncio

from message_handler import MESSAGE_HANDLER_FUNCTIONS_ARGS, MESSAGE_HANDLER_FUNCTIONS_NO_ARGS, MESSAGE_HANDLER_FUNCTIONS_ALL
from private_constants import BOT_TOKEN

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('*' * 30)
    print('Logged in as: %s' % client.user.name)
    print('*' * 30)

@client.event
@asyncio.coroutine
def on_message(message):
    
    if message.content.startswith('!'):

        message_str = message.content.lower().split(' ')[0]
        if message_str not in MESSAGE_HANDLER_FUNCTIONS_ALL.keys():
            message_str = '!invalid'

        if message_str in MESSAGE_HANDLER_FUNCTIONS_ARGS:
            reply = MESSAGE_HANDLER_FUNCTIONS_ARGS[message_str](message)
        else:
            reply = MESSAGE_HANDLER_FUNCTIONS_NO_ARGS[message_str]()

        yield from client.send_message(message.channel, reply)

client.run(BOT_TOKEN)
