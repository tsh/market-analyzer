import json
import os
import requests
import datetime as dt

from portfolio import Portfolio
from api import SeekingAlpha
import config


class Telegram:
    def __init__(self):
        self.chat_id_prev = 595574277
        self.token = config.TG_TOKEN
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

    def send_photo(self, obj):
        import telepot
        bot = telepot.Bot(self.token)
        bot.sendPhoto(self.chat_id, obj)


def get_edgar(date, interests) -> str:
    from edgar import set_identity, get_filings
    set_identity("tsh tsh test@test.com")

    filings = get_filings().filter(filing_date=date.strftime('%Y-%m-%d'))
    # filings = get_filings().filter(filing_date=date.strftime('2023-08-17'))
    df = filings.to_pandas()
    df = df[df['cik'].isin(interests)]
    return str(df)


if __name__ == '__main__':
    tg = Telegram()
    today = dt.datetime.today()
    interests = Portfolio.notification_interests()
    filings = get_edgar(today, interests)
    tg.send(f'As of {today} w/ {interests}')
    tg.send(filings)
    # tg.send_photo(open('Figure_1.png', 'rb'))

    past_day = today - dt.timedelta(days=1)
    unix_past_day = past_day.timestamp()
    sa = SeekingAlpha()
    articles = sa.get_articles(unix_past_day)
    with open(os.path.join(config.DATA_DIR, f'{past_day:%Y_%m_%d}.json'), 'w') as f:
        f.write(json.dumps(articles))
