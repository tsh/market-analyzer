from datetime import date
import sys
from pathlib import Path

from prefect import flow, task, runtime
from prefect.logging import get_run_logger

from edgar import set_identity, get_filings

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from tg import Telegram
from portfolio import Portfolio


logger = get_run_logger()


@task
def get_edgar_ownership_on_date(date) -> set:
    logger.info('+++ GETTING EDGAR')

    set_identity("tsh tsh test@test.com")
    filings = get_filings(filing_date=date.strftime('%Y-%m-%d'), form=['3', '4', '5'])
    if filings:
        df = filings.to_pandas()
        cik = set(df['cik'])
        print(cik)
        return cik
    else:
        print('No fillings today')
        return set()


@task
def notify(cik: set):
    # if not cik:
    #     return None
    logger.info('STARTING TG process')
    tg = Telegram()
    portfolio = Portfolio()
    interests = portfolio.interest_cik()
    to_notify = cik.intersection(interests)
    logger.info('TG SENDING')
    if to_notify:
        tg.send(str(to_notify))
    else:
        tg.send('Nothing of interests today')


@flow(log_prints=True)
def edgar_ownership(run_date: date= None):
    cur_date = run_date or runtime.flow_run.scheduled_start_time
    logger.info('+++ Running for ' + str(run_date))
    cik = get_edgar_ownership_on_date(cur_date)
    notify(cik)
    return True


if __name__ == "__main__":
    edgar_ownership.from_source(
        source='https://github.com/tsh/market-analyzer.git',
        entrypoint='workflows/wedgar.py:edgar_ownership'  # TODO: dynamic path
    ).deploy(
        name="edgar-ownership-deploy",
        work_pool_name="laptop-local",  # TODO: link w/ ansible
        cron="*/2 * * * *"
    )
    # edgar_ownership(date(2024,12,12))

