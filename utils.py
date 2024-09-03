import os

from vectara_agentic.agent import Agent

from query_vectara import VectaraQuery


def query_vectara(query, conv_id, vectara_prompt, bot_type):
    if os.getenv("ENABLE_AGENTIC_RAG", default=False):
        agent = Agent.from_corpus(
            vectara_customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            vectara_corpus_id=os.getenv("VECTARA_CORPUS_IDS"),
            vectara_api_key=os.getenv("VECTARA_API_KEY"),
            data_description="Vectara website, docs and forum data ",
            assistant_specialty="Vectara ",
            tool_name="ask_vectara",
        )
        response = agent.chat(query)
        return None, response
    else:
        vectara = VectaraQuery(
            customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
            corpus_ids=os.getenv("VECTARA_CORPUS_IDS").split(','),
            api_key=os.getenv("VECTARA_API_KEY"),
            prompt_name=vectara_prompt,
            conv_id=conv_id,
            bot_type=bot_type
        )
        vectara_convo_id, response = vectara.submit_query(query)
        return vectara_convo_id, response