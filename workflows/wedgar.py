from datetime import date

from prefect import flow, task, runtime
from edgar import set_identity, get_filings


@task
def hello(v):
    return 'Hi date is: {}'.format(v)


def get_edgar_ownership_on_date(date):
    set_identity("tsh tsh test@test.com")
    filings = get_filings(filing_date=date.strftime('%Y-%m-%d'), form=['3', '4', '5'])
    if filings:
        df = filings.to_pandas()
        print(set(df['cik']))
    else:
        print('No fillings today')


@flow(log_prints=True)
def hello_world(run_date: date= None):
    cur_date = run_date or runtime.flow_run.scheduled_start_time
    res = hello('world ' + str(cur_date))
    print(res)
    get_edgar_ownership_on_date(cur_date)
    return True


if __name__ == "__main__":
    # get_edgar_ownership_on_date(date(2024,12,12))
    hello_world.serve(name="my-first-deployment", cron="* * * * *",
                      parameters={'run_date': '2024-12-12'}
                      )
