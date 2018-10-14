class Stock:
    __allowed = ["ticker", "currentPrice", "fiftyDayMvAvg", "twoHundredDayMvAvg",
                 "marketCap", "trailingPe", "forwardPe", "peg", "priceSales", "priceBook",
                 "evSales", "evEBITDA", "debtEquity", "currentRatio", "operatingCashFlow",
                 "leveredFreeCashFlow", "forwardDividendYield", "trailingDividendYield",
                 "PayoutRatio"]
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            assert (k in self.__class__.__allowed)
            setattr(self, k, v)