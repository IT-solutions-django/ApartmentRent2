import requests


def send_telegram_message(text):
    token = "7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A"
    chat_id = "661612764"
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)
    return response.json()
