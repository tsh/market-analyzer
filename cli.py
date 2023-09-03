from typing import Iterable, Type
import yfinance as yf
from pandas import DataFrame
from rich.table import Table
from rich.console import Console
from rich.progress import track

from textual._path import CSSPathType
from textual.driver import Driver
from textual.app import App, CSSPathType, ComposeResult
from textual.widgets import DataTable

from pprint import pprint


def get_iv_atm(chain: DataFrame) -> float:
    chain['nearStrike'] = chain['inTheMoney'].shift(periods=1, fill_value=chain['inTheMoney'].head()[0]) \
                              != chain['inTheMoney']
    # TODO: calc mean with multiple options near ATM
    near_strike = chain[chain['nearStrike'] == True]
    return near_strike['impliedVolatility'].values[0]


def get_data():
    data = {}
    options_dates = set()
    for stock in track(['BITO', 'APLD'], description='getting data'):
        ticker = yf.Ticker(stock)
        opt_dates = ticker.options
        options_dates.update(opt_dates)
        date_iv = {}
        for date in opt_dates:
            chain = ticker.option_chain(date)
            iv = get_iv_atm(chain.calls)
            date_iv[date] = iv
        data[stock] = date_iv
    return options_dates, data


def make_table(options_dates: Iterable, stock_data: dict):
    """
    create array resembling table:
    Ticker  | date1 | date2
    name    |  iv1  | iv2
    """
    table = []
    columns = sorted(options_dates)
    table.append(['Ticker'] + list(columns))
    for stock_name, data in stock_data.items():
            row = []
            for date in columns:
                row.append(str(data.get(date, '-')))
            table.append([stock_name] + row)
    return table


def render_rich(data:list):
    console = Console()
    table = Table(show_header=True, header_style="bold ")
    # Header
    for i, c in enumerate(iv_table[0]):
        if i == 0:
            # Highlight instr name w/ diff color
            table.add_column(c, style='cyan')
        else:
            table.add_column(c)
    # Rows
    for row in iv_table[1:]:
        table.add_row(*row)
    console.print(table)


class TableApp(App):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.data[0])
        table.add_rows(self.data[1:])
        table.add_row('1', '2', '3')


if __name__ == '__main__':
    options_dates, stock_data = get_data()
    iv_table = make_table(options_dates, stock_data)
    print(iv_table)
    # render_rich(iv_table)
    app = TableApp(iv_table)
    app.run()

        

