from models import Stock, YahooProvider
from views import GUI, Telegram
from edgar.edgar import RecentSubmissionsAtom

from rich.table import Table
from rich.console import Console
from pprint import pprint


def tg():
    interests = ['tesla', 'scion']
    activities = []
    for parser in RecentSubmissionsAtom().get_data():
        for interest in interests:
            for entree in  parser.entries:
                if interest.lower() in entree['title'].lower():
                    activities.append(entree['title'])

    tg = Telegram()
    if activities:
        text = '\n'.join(activities)
    else:
        text = 'Nothing found'
    tg.send(text)

def get_data():
    import yfinance as yf
    data = {}
    for stock in ['BITO', 'APLD']:
        ticker = yf.Ticker(stock)
        opts = ticker.options
        last_date = opts[-1]
        chain = ticker.option_chain(last_date)
        data[stock] = [chain.calls, ticker.history()]

    res ={}
    for s, v in data.items():
        df = v[0]
        dff = df.loc[df['inTheMoney'] == False]
        last_history = v[1].tail(1)
        res[s]= {'date': last_history.index.to_list()[0].strftime('%Y-%m-%d'),
                 'price': round(last_history.iloc[0].High, 2),
                 'iv': round(dff.impliedVolatility.mean(), 2)}
    return res


if __name__ == '__main__':
        table = Table(show_header=True, header_style="bold ")
        table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
        table.add_column("Date", justify="right",  no_wrap=True)
        table.add_column("Price H", justify="right", no_wrap=True)
        table.add_column("IV", justify="right", no_wrap=True)

        stock_data = get_data()
        for stock, data in stock_data.items():
            table.add_row(stock, data['date'], str(data['price']), str(data['iv']))
        console = Console()
        console.print(table)

