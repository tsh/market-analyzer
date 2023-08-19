import os
import requests
import datetime


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
    dt = datetime.datetime.today()
    interests = []
    filings = get_edgar(dt, interests)
    tg.send(f'As of {dt} w/ {interests}')
    tg.send(filings)
