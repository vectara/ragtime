import requests
import json
import re
from urllib.parse import quote


def extract_between_tags(text, start_tag, end_tag):
    '''
    Extracts text between two tags in a string.
    '''
    start_index = text.find(start_tag)
    end_index = text.find(end_tag, start_index)
    return text[start_index + len(start_tag):end_index - len(end_tag)]


class VectaraQuery:
    def __init__(self, api_key: str, customer_id: str, corpus_ids: list[str], prompt_name: str = None,
                 conv_id: str = None, bot_type: str = ""):
        self.customer_id = customer_id
        self.corpus_ids = corpus_ids
        self.api_key = api_key
        self.prompt_name = prompt_name if prompt_name else "vectara-summary-ext-24-05-sml"
        self.conv_id = conv_id
        self.bot_type = bot_type

    def submit_query(self, query_str: str):
        corpora_key_list = [{
            'customer_id': self.customer_id, 'corpus_id': corpus_id, 'lexical_interpolation_config': {'lambda': 0.005}
        } for corpus_id in self.corpus_ids
        ]

        endpoint = "https://api.vectara.io/v1/query"
        start_tag = "%START_SNIPPET%"
        end_tag = "%END_SNIPPET%"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "customer-id": self.customer_id,
            "x-api-key": self.api_key,
            "grpc-timeout": "60S",
            "X-Source": "ragtime"
        }
        body = {
            'query': [
                {
                    'query': query_str,
                    'start': 0,
                    'numResults': 50,
                    'corpusKey': corpora_key_list,
                    'context_config': {
                        'sentences_before': 2,
                        'sentences_after': 2,
                        'start_tag': start_tag,
                        'end_tag': end_tag,
                    },
                    'rerankingConfig':
                        {
                            'rerankerId': 272725719,  # If you are not on the scale plan, use
                            # '272725718'
                        },
                    'summary': [
                        {
                            'responseLang': 'eng',
                            'maxSummarizedResults': 7,
                            'summarizerPromptName': self.prompt_name,
                            'chat': {
                                'store': True,
                                'conversationId': self.conv_id
                            },
                        }
                    ]
                }
            ]
        }

        response = requests.post(endpoint, data=json.dumps(body), verify=True, headers=headers)
        if response.status_code != 200:
            print(f"Query failed with code {response.status_code}, reason {response.reason}, text {response.text}")
            return "Sorry, something went wrong in my brain. Please try again later."

        res = response.json()

        top_k = 10
        summary = res['responseSet'][0]['summary'][0]['text']
        conversation_id = res['responseSet'][0]['summary'][0]['chat']['conversationId']
        responses = res['responseSet'][0]['response'][:top_k]
        docs = res['responseSet'][0]['document']
        chat = res['responseSet'][0]['summary'][0]['chat']

        if chat['status'] is not None:
            st_code = chat['status']
            print(f"Chat query failed with code {st_code}")
            if st_code == 'RESOURCE_EXHAUSTED':
                self.conv_id = None
                return 'Sorry, Vectara chat turns exceeds plan limit.'
            return 'Sorry, something went wrong in my brain. Please try again later.'

        self.conv_id = res['responseSet'][0]['summary'][0]['chat']['conversationId']

        pattern = r'\[\d{1,2}\]'
        matches = [match.span() for match in re.finditer(pattern, summary)]

        # figure out unique list of references
        refs = []
        for match in matches:
            start, end = match
            response_num = int(summary[start + 1:end - 1])
            doc_num = responses[response_num - 1]['documentIndex']
            metadata = {item['name']: item['value'] for item in docs[doc_num]['metadata']}
            text = extract_between_tags(responses[response_num - 1]['text'], start_tag, end_tag)
            if 'url' in metadata.keys():
                url = f"{metadata['url']}#:~:text={quote(text)}"
                if url not in refs:
                    refs.append(url)

        # replace references with markdown links
        refs_dict = {url: (inx + 1) for inx, url in enumerate(refs)}

        for match in reversed(matches):
            start, end = match
            response_num = int(summary[start + 1:end - 1])
            doc_num = responses[response_num - 1]['documentIndex']
            metadata = {item['name']: item['value'] for item in docs[doc_num]['metadata']}
            text = extract_between_tags(responses[response_num - 1]['text'], start_tag, end_tag)
            url = f"{metadata['url']}#:~:text={quote(text)}"
            citation_inx = refs_dict[url]
            if self.bot_type == "slack":
                summary = summary[:start] + f'[<{url}|{citation_inx}>]' + summary[end:]
            else:
                summary = summary[:start] + f'[[{citation_inx}]](<{url}>)' + summary[end:]

        return conversation_id, summary
