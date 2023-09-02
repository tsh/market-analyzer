import yfinance as yf
from pandas import DataFrame
from rich.table import Table
from rich.console import Console
from rich.progress import track

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


if __name__ == '__main__':
        options_dates, stock_data = get_data()

        table = Table(show_header=True, header_style="bold ")
        table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)

        columns = sorted(options_dates)
        for d in columns:
            table.add_column(d)

        for stock, data in stock_data.items():
            row = []
            for date in columns:
                row.append(str(data.get(date, '-')))
            table.add_row(stock, *row)
        # for date in df.columns:
        #     table.add_column(str(date))
        #
        # for stock, values in zip(df.index,df.values.tolist()):
        #     table.add_row(stock, *[str(v) for v in values])
        console = Console()
        console.print(table)

