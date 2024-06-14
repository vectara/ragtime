import logging
import os
import discord
from discord.ext import commands

from db import start_db_connection, get_conversation_id, insert_entry
from query_vectara import VectaraQuery

intents = discord.Intents.default()
intents.message_content = True  # Enables the bot to read message content
discord_bot = commands.Bot(command_prefix='!', intents=intents)
logging.basicConfig(level=logging.INFO)
conn = start_db_connection()

# If you are not on the scale plan, use 'vectara-summary-ext-24-05-sml'
vectara_prompt = 'vectara-summary-ext-24-05-med-omni'

def split_message(content, max_length=1950):
    """
    Discord only allows to send messages upto 2000 characters only. That's why we are splitting into multiple messages
    if the message is longer than the 2000 characters.
    setting the length of the message to 1950 characters, So that we can use the handler of the person
    who asked question
    :param content:
    :param max_length:
    :return:
    """

    # Split by space to avoid breaking words
    words = content.split(' ')
    messages = []
    current_message = ""
    for word in words:
        # Check if adding the next word would exceed the max length
        if len(current_message) + len(word) + 1 > max_length:
            messages.append(current_message.strip())
            current_message = word
        else:
            current_message += ' ' + word
    if current_message:
        messages.append(current_message.strip())
    return messages


@discord_bot.event
async def on_ready():
    logging.info(f'Logged in as {discord_bot.user} (ID: {discord_bot.user.id})')

@discord_bot.event
async def on_message(message):
    '''
    This function is triggered when the bot receives a message.
    '''
    if message.author == discord_bot.user:
        return

    is_direct_message = isinstance(message.channel, discord.DMChannel)
    if discord_bot.user.mentioned_in(message) or is_direct_message:
        message_content = message.content.replace(f'<@{discord_bot.user.id}>', '').strip()
        if message_content:
            convo_id = None
            if isinstance(message.channel, discord.Thread):
                parent_message_id = message.channel.id
                convo_id = get_conversation_id(conn, parent_message_id) if parent_message_id else None
                logging.info(f"Received conversation id from DB: {convo_id}")
            elif message.reference:
                original_message_id = str(message.reference.message_id)
                convo_id = get_conversation_id(conn, original_message_id) if original_message_id else None
                logging.info(f"Received conversation id from DB: {convo_id}")

            vectara = VectaraQuery(
                customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
                corpus_ids=os.getenv("VECTARA_CORPUS_IDS").split(','),
                api_key=os.getenv("VECTARA_API_KEY"),
                prompt_name=vectara_prompt,
                conv_id=convo_id
            )
            vectara_convo_id, response = vectara.submit_query(message_content)
            split_messages = split_message(response)
            bot_reply = None
            if len(split_messages) == 1:
                reply_message = response if is_direct_message else f'{message.author.mention} {response}'
                bot_reply = await message.channel.send(reply_message)
            else:
                for index, part in enumerate(split_messages):
                    if index == 0:
                        reply_message = response if is_direct_message else f'{message.author.mention} {response}'
                        bot_reply = await message.channel.send(reply_message)
                    else:
                        bot_reply = await message.channel.send(f'{part}')

            if bot_reply:
                reply_message_id = str(bot_reply.id)
                if not isinstance(message.channel, discord.Thread):
                    insert_entry(conn, reply_message_id, vectara_convo_id)

            await discord_bot.process_commands(message)


async def start_discord_bot():
    await discord_bot.start(os.getenv("DISCORD_BOT_TOKEN"))
