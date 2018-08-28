from bs4 import BeautifulSoup
import pickle
import html_parser as parser
import os
import pandas as pd
import requests

#Where tickers comes from
goldStocks = "http://www.miningfeeds.com/gold-mining-report-all-countries"

baseurl = "https://uk.finance.yahoo.com/quote/"


class StockScreener:
    def __init__(self, stockTypes, baseurl = baseurl, goldStocks = goldStocks, reloadTickers = True):
        self.baseurl = baseurl
        self.goldStocks = goldStocks
        self.stockTypes = stockTypes
        self.reloadTickers = reloadTickers
        self.tickers = self.loadGoldTickers()
        self.stocks = []

    def getDataFromYahoo(self):

        dataDir = "./%s_data" % self.stockTypes
        self.createDirIfItDoesntExist(dataDir)

        for ticker in self.tickers:
            dataFile = "./%s/%s.csv" % (dataDir, ticker)
            data = None
            if not os.path.exists(dataFile):
                data = self.saveData(dataFile, ticker)
            else:
                print("Already have %s" % ticker)
                data = pd.read_csv(dataFile)
            self.createStock(data)


    def loadGoldTickers(self, stockTypes = "gold_stocks"):
        if self.reloadTickers:
            return parser.parseTickersFromHtmlTable(self.goldStocks, 2, stockTypes)
        else:
            with open(stockTypes + ".pickle", "rb") as file:
                return pickle.load(file)

    def createDirIfItDoesntExist(self, dataDir):
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)

    def saveDataAndReturnFrame(self, dataFile, ticker):
        print("Requesting: %s" % ticker)
        data = requests.get(baseurl + "%s/key-statistics?p=%s" % (ticker, ticker))
        soup = BeautifulSoup(data.text, "lxml")
        frames = pd.read_html(data.text)
        if len(frames) < 3:
            print("No data for: %s" % ticker)
        frame = pd.concat(frames)
        frame.to_csv(dataFile)
        return frame

    def createStock(self, stockDataFrame):
        print(stockDataFrame)

def main():
    stockScreener = StockScreener("gold_stocks", reloadTickers = False)
    stockScreener.getDataFromYahoo()

if __name__ == "__main__":
    main()
