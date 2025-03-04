import requests


def send_telegram_message(text):
    token = "7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A"
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    chat_ids = ["661612764", "777759367", "882495943"]

    responses = []
    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload)
        responses.append(response.json())

    return responses
