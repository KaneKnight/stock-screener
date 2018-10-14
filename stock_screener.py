from bs4 import BeautifulSoup
import pickle
import html_parser as parser
import os
import pandas as pd
import requests
from stock_object import Stock
from string_number_converter import StringNumberConverter
import math

#Where tickers comes from
goldStocks = "http://www.miningfeeds.com/gold-mining-report-all-countries"

baseurl = "https://uk.finance.yahoo.com/quote/"

wantedRows = {60 : "currentPrice",
              36 : "fiftyDayMvAvg",
              37 : "twoHundredDayMvAvg",
              0  : "marketCap",
              2  : "trailingPe",
              3  : "forwardPe",
              4  : "peg",
              5  : "priceSales",
              6  : "priceBook",
              7  : "evSales",
              8  : "evEBITDA",
              26 : "debtEquity",
              27 : "currentRatio",
              29 : "operatingCashFlow",
              30 : "leveredFreeCashFlow",
              50 : "forwardDividendYield",
              52 : "trailingDividendYield",
              54 : "PayoutRatio"}

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
            if ticker in ["GLF.AX", "AZ.TO"]:
                continue
            if ticker == "RRS.L":
                ticker = "GOLD"
            dataFile = "./%s/%s.csv" % (dataDir, ticker)
            data = None
            if not os.path.exists(dataFile):
                data = self.saveDataAndReturnFrame(dataFile, ticker)
            else:
                print("Already have %s" % ticker)
                data = pd.read_csv(dataFile, index_col=0)
            self.stocks.append(self.createStock(data, ticker))
        self.calculateAveragesForSector()


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

        #Go to summary page and scrape open.
        priceData = requests.get(baseurl + "%s?p=%s" % (ticker, ticker))
        summaryFrames = pd.read_html(priceData.text)
        summaryFrame = pd.concat(summaryFrames, ignore_index=True)
        priceFrame = summaryFrame.loc[1:1]

        #Go to stats page and scrape stats.
        data = requests.get(baseurl + "%s/key-statistics?p=%s" % (ticker, ticker))
        frames = pd.read_html(data.text)
        if len(frames) < 3:
            print("No data for: %s" % ticker)
            return

        #Join stats and price
        frames.append(priceFrame)
        frame = pd.concat(frames, ignore_index=True)

        #Save data
        frame.to_csv(dataFile)
        return frame

    def createStock(self, stockDataFrame, ticker):
        dict = {}
        for index in wantedRows:
            series = stockDataFrame.loc[index]
            key = wantedRows[index]
            value = series.get(1)
            dict[key] = value
            dict["ticker"] = ticker
        marketCapString = dict["marketCap"]
        if not isinstance(marketCapString, str):
            return None
        converter = StringNumberConverter(marketCapString)
        marketCap = converter.convert()
        print(marketCap)
        print(marketCap < 500)
        if marketCap < 500:
            return None
        dict["marketCap"] = marketCap
        return Stock(**dict)

    def calculateAveragesForSector(self):
        seriesList = []
        tickers = []
        print(self.stocks)
        for stock in self.stocks:
            if stock == None:
                continue
            dict = stock.__dict__
            series = pd.Series(dict)
            series = series.drop(labels=["ticker"])
            tickers.append(stock.ticker)
            seriesList.append(series)
        frame = pd.concat(seriesList, axis=1, keys=tickers)
        frame = frame.convert_objects(convert_numeric=True)
        frame = frame.sort_values(by="debtEquity", axis=1, ascending=True)
        print(frame)
        average = frame.mean(axis=1, skipna=True)
        print(average)
        frame.to_csv("output.csv")


def main():
    stockScreener = StockScreener("gold_stocks", reloadTickers = False)
    stockScreener.getDataFromYahoo()

if __name__ == "__main__":
    main()
