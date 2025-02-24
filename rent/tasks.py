from celery import shared_task
import requests

TELEGRAM_BOT_TOKEN = "7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A"
TELEGRAM_CHAT_ID = "777759367"


@shared_task
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    requests.post(url, data=payload)


@shared_task
def send_telegram_feedback(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    requests.post(url, data=payload)