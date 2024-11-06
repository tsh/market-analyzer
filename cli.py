from typing import Iterable, Type
import logging 

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


class Errors:
    NO_ATM = 'No ATM'  # Some options available, but no ATM
    EMPTY_CHAIN = 'Empty chain'
    NO_OPTIONS_FOR_DATE = 'no4d'


def get_iv_atm(chain: DataFrame) -> float:
    if chain.empty:
        logging.warning('Empty chain for:\n %s', chain)
        return Errors.EMPTY_CHAIN
    chain['nearStrike'] = chain['inTheMoney'].shift(periods=1, fill_value=chain['inTheMoney'].head()[0]) \
                            != chain['inTheMoney']
    # TODO: calc mean with multiple options near ATM
    near_strike = chain[chain['nearStrike'] == True]
    if near_strike.empty:
        logging.warning('No atm for:\n %s', chain)
        return Errors.NO_ATM
    return near_strike['impliedVolatility'].values[0]


def get_data():
    data = {}
    options_dates = set()
    for stock in [ 
                'APLD', 'MARA', 'COIN', 'ANY', 'ARBK', 'BTBT', 'BTDR', 'BITF', 'CIFR',
                'CLSK', 'CORZ', 'DGHI', 'DMG', 'GREE', 'HIVE', 'HUT', 'IREN', 'GLXY.TO', 'MIGI',
                'IBIT', 'ETHA', 'BITO'
                ]:
        logging.info('Fetching: %s', stock)
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
                row.append(str(data.get(date, Errors.NO_OPTIONS_FOR_DATE)))
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
    CSS_PATH = 'textual.tcss'

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def compose(self) -> ComposeResult:
        yield DataTable(id='iv-table')

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.data[0])
        table.add_rows(self.data[1:])
        table.fixed_columns = 1
        table.cursor_type='row'


if __name__ == '__main__':
    options_dates, stock_data = get_data()
    iv_table = make_table(options_dates, stock_data)

    # render_rich(iv_table)
    app = TableApp(iv_table)
    app.run()

        

