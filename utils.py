import logging
import os
import re

import requests
from vectara_agentic.agent import Agent
from redis_client import redis_client
from query_vectara import VectaraQuery

# Regular expression to find and replace Markdown-style links
pattern = r'\[(.*?)\]\((.*?)\)'


def convert_to_slack_link(match):
    """
    Function to replace each match with Slack-style hyperlink
    """
    display_text = match.group(1).strip()  # The text inside the square brackets
    url = match.group(2).strip()  # The URL inside the parentheses
    # Return the Slack hyperlink format
    return f"<{url}|{display_text}>"


# Function to convert to Discord hyperlink format
def convert_to_discord_link(match):
    display_text = match.group(1).strip()  # The text inside the square brackets
    url = match.group(2).strip()  # The URL inside the parentheses
    # Return the Discord hyperlink format
    return f'[{display_text}](<{url}>)'


def shorten_url_tinyurl(long_url):
    api_url = f'http://tinyurl.com/api-create.php?url={long_url}'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text  # This is the shortened URL
    else:
        return None  # Handle the error


def query_vectara(query, conv_id, vectara_prompt, reference_id, bot_type):
    # if os.getenv("ENABLE_AGENTIC_RAG", default=False):
    #     if reference_id:
    #         logging.info("Using the existing agent with reference_id: {}".format(reference_id))
    #         agent = redis_client.get(reference_id)
    #         agent = Agent.loads(agent)
    #         response = agent.chat(query)
    #         logging.info(response)
    #         if bot_type == "slack":
    #             response = re.sub(pattern, convert_to_slack_link, response)
    #         else:
    #             response = re.sub(pattern, convert_to_discord_link, response)
    #         return None, response, None
    #     else:
    #         agent = Agent.from_corpus(
    #             vectara_customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
    #             vectara_corpus_id=os.getenv("VECTARA_CORPUS_IDS"),
    #             vectara_api_key=os.getenv("VECTARA_API_KEY"),
    #             data_description=os.getenv("AGENTIC_RAG_DATA_DESCRIPTION"),
    #             assistant_specialty=os.getenv("AGENTIC_RAG_ASSISTANT_SPECIALTY"),
    #             tool_name=os.getenv("AGENTIC_RAG_TOOL_NAME"),
    #         )
    #
    #         response = agent.chat(query)
    #         logging.info(response)
    #         if bot_type == "slack":
    #             response = re.sub(pattern, convert_to_slack_link, response)
    #         else:
    #             response = re.sub(pattern, convert_to_discord_link, response)
    #         return None, response, agent.dumps()
    # else:
        vectara = VectaraQuery(
            customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            corpus_ids=os.getenv("VECTARA_CORPUS_IDS").split(','),
            api_key=os.getenv("VECTARA_API_KEY"),
            prompt_name=vectara_prompt,
            conv_id=conv_id,
            bot_type=bot_type
        )
        vectara_conv_id, response = vectara.submit_query(query)
        return vectara_conv_id, response, None
