import requests
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
def get_answer_from_yandex_gpt(role: str, text: str):
    prompt = {
        "modelUri": os.getenv('catalog_identification'),
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": role
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv('yandex_secret_key')
    }
    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    result = result.split("\"result\":{\"alternatives\":"
                                "[{\"message\":{\"role\":\"assistant\",\"text\""":\"""")[1]
    result = result.split('\"},')[0]
    return result
