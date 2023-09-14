import matplotlib.pyplot as plt
import yfinance as yf


def display(standardize=True):
    start, end = '2020-01-01', '2023-09-01'
    fig, ax = plt.subplots(figsize=(10, 10))

    for stock_name in ['COIN', 'BITO', 'MSTR', 'MSFT']:
        stock_data = yf.download(stock_name, start=start, end=end)
        stock_data.reset_index(inplace=True)

        if standardize:
            std = stock_data.std()
            mean = stock_data.mean()
            data = (stock_data['Close'] - mean['Close'])/ std['Close']
        else:
            data = stock_data['Close']

        ax.plot(stock_data['Date'], data, label=stock_name)
    plt.legend()
    plt.show()

display(False)