import logging
import os
import traceback

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk import WebClient
from slack_bolt.async_app import AsyncApp

from db import get_conversation_id, insert_entry, start_db_connection
from query_vectara import VectaraQuery
from dotenv import load_dotenv

load_dotenv()

# Event API & Web API
slack_app = AsyncApp(token=os.getenv("SLACK_BOT_TOKEN"))
client = WebClient(os.getenv("SLACK_BOT_TOKEN"))
logging.basicConfig(level=logging.INFO)

conn = start_db_connection()

# If you are not on the scale plan, use 'vectara-summary-ext-24-05-sml'
vectara_prompt = 'vectara-summary-ext-24-05-med-omni'


@slack_app.event("app_mention")
async def handle_mention(body, say):
    '''
    This function is triggered when the bot is mentioned in a channel.
    '''
    event = body["event"]
    await reply_to_message(event, say)


@slack_app.event("message")
async def handle_direct_message(body, say):
    '''
    This function is triggered when the bot receives a direct message.
    '''
    event = body["event"]
    if event.get("channel_type") == "im":
        await reply_to_message(event, say)


async def reply_to_message(event, say):
    '''
    This function replies to the message received by the bot.
    The response is based on a Vectara Query that uses the message as a prompt.
    '''
    convo_id = None
    try:
        try:
            prompt = event["text"].split(">")[1]
        except IndexError:
            prompt = event["text"]
        thread_ts = event.get("thread_ts", None)
        if thread_ts:
            res = client.conversations_replies(channel=event["channel"], ts=thread_ts)
            parent_message_ts = res["messages"][0]["ts"]
            convo_id = get_conversation_id(conn, parent_message_ts)
            logging.info(f"Received conversation id from DB: {convo_id}")

        vectara = VectaraQuery(
            customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            corpus_ids=os.getenv("VECTARA_CORPUS_IDS").split(','),
            api_key=os.getenv("VECTARA_API_KEY"),
            prompt_name=vectara_prompt,
            conv_id=convo_id,
            bot_type="slack"
        )
        vectara_convo_id, response = vectara.submit_query(prompt)
        user = event["user"]
        reply_content = f"<@{user}> {response}" if event.get("channel_type") != "im" else response

        response = await say(reply_content, thread_ts=thread_ts, unfurl_links=False, unfurl_media=False)
        ts = response["ts"]
        if thread_ts is None:
            insert_entry(conn, ts, vectara_convo_id)

    except Exception as e:
        logging.error(
            f"Error  {e}, traceback={traceback.format_exc()}"
        )
        reply_content = "Something went wrong. Please, try again."
        say(reply_content)


async def start_slack_bot():
    handler = AsyncSocketModeHandler(slack_app, os.getenv("SLACK_APP_TOKEN"))
    await handler.start_async()
