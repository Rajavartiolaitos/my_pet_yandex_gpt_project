import requests
from config import config_key


def get_answer_from_yandex_gpt(role: str, text: str):
    prompt = {
        "modelUri": config_key.catalog_identification,
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
        "Authorization": config_key.yandex_secret_key
    }
    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    result = result.split("\"result\":{\"alternatives\":"
                                "[{\"message\":{\"role\":\"assistant\",\"text\""":\"""")[1]
    result = result.split('\"},')[0]
    return result
