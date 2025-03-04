from celery import shared_task
import requests

TELEGRAM_BOT_TOKEN = "7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A"
TELEGRAM_CHAT_ID = "661612764"


@shared_task
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    chat_ids = ["661612764", "777759367", "882495943"]

    responses = []
    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        responses.append(response.json())

    return responses


@shared_task
def send_telegram_feedback(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    chat_ids = ["661612764", "777759367", "882495943"]

    responses = []
    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        responses.append(response.json())

    return responses


@shared_task
def send_email_booking(recipient, subject, content, ip):
    url = "https://sendemail.space/send-email/"
    data_q = {
        "recipient": recipient,
        "subject": subject,
        "content": content,
        "ip": ip
    }

    try:
        response = requests.post(url, data=data_q, timeout=10)
        response_data = response.json()
        return response_data
    except requests.RequestException as e:
        return {"status": "failed", "errors": str(e)}
