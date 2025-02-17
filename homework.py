import os
import requests
import time

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()


def get_status(user_id):
    TOKEN = os.getenv('VK_TOKEN')
    params = {
        "user_ids": user_id,
        "v": "5.92",
        "fields": "online",
        "access_token": TOKEN,
    }
    user_status = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
    )
    return user_status.json()['response'][0]['online']


def sms_sender(sms_text):
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    NUMBER_FROM = os.getenv('NUMBER_FROM')
    NUMBER_TO = os.getenv('NUMBER_TO')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите ID ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
