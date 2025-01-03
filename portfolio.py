from sec_cik_mapper import StockMapper, MutualFundMapper

class Portfolio:
    def __init__(self):
        self.mapper = StockMapper()  # todo: cache locally with weekly refresh
        # ticker: cik
        self.interests = {
            'GLXY': '1859392',
            'COIN': '1679788',
            'BITO': '0001174610'
        }

    def interest_tickers(self):
        return list(self.interests.keys())

    def interest_cik(self):
        return list(self.interests.values())
