import os
import requests


class Telegram:
    def __init__(self):
        self.chat_id_prev = 595574277
        self.token = os.environ['TG_TOKEN']
        rsp = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        rsp.raise_for_status()
        chat_id = None
        for result in rsp.json()['result']:
            chat_id = result['message']['chat']['id']
            break
        self.chat_id = chat_id or self.chat_id_prev

    def send(self, msg: str):
        rsp = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage', json={'chat_id': self.chat_id,
                                                                                          'text': msg})
        rsp.raise_for_status()


if __name__ == '__main__':
    tg = Telegram()
    tg.send('test')
