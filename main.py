from models import Stock, YahooProvider
from views import GUI, TUI, Telegram
from edgar.edgar import RecentSubmissionsAtom

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



if __name__ == '__main__':
    import yfinance as yf
    res = {}
    for stock in ['BITO', 'APLD']:
        ticker = yf.Ticker(stock)
        opts = ticker.options
        last_date = opts[-1]
        chain = ticker.option_chain(last_date)
        res[stock] = [chain.calls, ticker.history()]

    for s, v in res.items():
        df = v[0]
        dff = df.loc[df['inTheMoney'] == False]
        last_history = v[1].tail(1)
        print(s, last_history.index.to_list()[0].strftime('%Y-%m-%d'),
              round(last_history.iloc[0].High, 2), round(dff.impliedVolatility.mean(), 2))

