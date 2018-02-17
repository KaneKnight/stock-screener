from bs4 import BeautifulSoup
import pickle
import html_parser as parser
import os
import pandas as pd
import requests

#Where tickers comes from
goldStocks = "http://www.miningfeeds.com/gold-mining-report-all-countries"

baseurl = "https://uk.finance.yahoo.com/quote/"
def getDataFromYahoo(url, tickerColumn, stockTypes, reloadTickers=False):
    if reloadTickers:
        tickers = parser.parseTickersFromHtmlTable(url, tickerColumn, stockTypes)
    else:
        with open(stockTypes + ".pickle", "rb") as file:
            tickers = pickle.load(file)

    dataDir = "./%s_data" % stockTypes
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    for ticker in tickers:
        dataFile = "./%s/%s.csv" % (dataDir, ticker)
        if not os.path.exists(dataFile):
            print("Requesting: %s" % ticker)
            data = requests.get(baseurl + "%s/key-statistics?p=%s" % (ticker, ticker))
            soup = BeautifulSoup(data.text, "lxml")
            frames = pd.read_html(data.text)
            if len(frames) < 3:
                print("No data for: %s" % ticker)
            frame = pd.concat(frames)
            frame.to_csv(dataFile)
        else:
            print("Already have %s" % ticker)



getDataFromYahoo(goldStocks, 2, "gold_stocks", reloadTickers=True)
