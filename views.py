import os

import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num
from rich.console import Console
from rich.table import Table


class GUI():
    def display(self, stock):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(stock.history()['Date'], stock.history()['Close'])
        plt.show()


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




