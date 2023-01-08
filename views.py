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

class TUI():
    def __init__(self):
        self.table = Table(show_header=True, header_style="bold magenta")
        # self.table.add_column("Date", style="dim", width=12)
        # self.table.add_column("Title")
        # self.table.add_column("Production Budget", justify="right")
        # self.table.add_column("Box Office", justify="right")
        # self.table.add_row(
        #     "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
        # )
        # self.table.add_row(
        #     "May 25, 2018",
        #     "[red]Solo[/red]: A Star Wars Story",
        #     "$275,000,000",
        #     "$393,151,347",
        # )
        # self.table.add_row(
        #     "Dec 15, 2017",
        #     "Star Wars Ep. VIII: The Last Jedi",
        #     "$262,000,000",
        #     "[bold]$1,332,539,889[/bold]",
        # )

    def display_table(self, data):
        console = Console()
        self.table.add_column('Ticker', style='dim', width=12)
        self.table.add_column('Current Price')
        self.table.add_column('My guess price')
        self.table.add_column('Analyst price')
        self.table.add_column('Analyst Percent')
        self.table.add_column('Buy/Outperform/Hold/Underperform/Sell')
        self.table.add_column('Current Analyst Resolution')  #e.g. buy/hold/sell?
        self.table.add_column('Analyst Resolution 6m')
        self.table.add_column('Analyst Resolution 1y')
        sdata = list(map(str, data))
        self.table.add_row(sdata[0], sdata[1])
        console.print(self.table)

    def display_graph(self, data):
        pass


class Telegram:
    def __init__(self):
        # self.chat = 595574277
        self.token = os.environ['TG_TOKEN']
        rsp = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        rsp.raise_for_status()
        for result in rsp.json()['result']:
            chat_id = result['message']['chat']['id']
            break

        rsp = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage', json={'chat_id': '@fnmngr_bottsh',
                                                                                          'text': 'test2'})
        rsp.raise_for_status()




