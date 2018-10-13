class Stock:
    def __init__(self, currentPrice, fiftyDayMvAvg, twoHundredDayMvAvg,
                 marketCap, trailingPe, forwardPe, peg, priceSales, priceBook,
                 evSales, evEBITDA, debtEquity, currentRatio, operatingCashFlow,
                 leveredFreeCashFlow, forwardDividendYield, trailingDividendYield,
                 PayoutRatio):
        self.currentPrice          = currentPrice
        self.fiftyDayMvAvg         = fiftyDayMvAvg
        self.twoHundredDayMvAvg    = twoHundredDayMvAvg
        self.marketCap             = marketCap
        self.trailingPe            = trailingPe
        self.forwardPe             = forwardPe
        self.peg                   = peg
        self.priceSales            = priceSales
        self.priceBook             = priceBook
        self.evSales               = evSales
        self.evEBITDA              = evEBITDA
        self.debtEquity            = debtEquity
        self.currentRatio          = currentRatio
        self.operatingCashFlow     = operatingCashFlow
        self.leveredFreeCashFlow   = leveredFreeCashFlow
        self.forwardDividendYield  = forwardDividendYield
        self.trailingDividendYield = trailingDividendYield
        self.PayoutRatio           = PayoutRatio