import logging
import os

from vectara_agentic.agent import Agent

from query_vectara import VectaraQuery


def query_vectara(query, convo_id, vectara_prompt, bot_type):
    if query.startswith('!agentic'):
        agent = Agent.from_corpus(
            vectara_customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            vectara_corpus_id=os.getenv("VECTARA_CORPUS_IDS"),
            vectara_api_key=os.getenv("VECTARA_API_KEY"),
            data_description="Vectara website, docs and forum data ",
            assistant_specialty="Vectara ",
            tool_name="ask_vectara",
        )
        response = agent.chat(query.replace("!agentic", ""))
        return None, response
    else:
        vectara = VectaraQuery(
            customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            corpus_ids=os.getenv("VECTARA_CORPUS_IDS").split(','),
            api_key=os.getenv("VECTARA_API_KEY"),
            prompt_name=vectara_prompt,
            conv_id=convo_id,
            bot_type=bot_type
        )
        vectara_convo_id, response = vectara.submit_query(query)
        return vectara_convo_id, response
