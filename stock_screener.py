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
        tickers = parseTickersFromHtmlTable(url, tickerColumn, stockTypes)
    else:
        with open(stockTypes + ".pickle", "rb") as file:
            tickers = pickle.load(file)

    for ticker in tickers[:1]:
        data = requests.get(baseurl + "%s/key-statistics?p=%s" % (ticker, ticker))
        soup = BeautifulSoup(data.text, "lxml")
        frame = pd.read_html(data.text)
        


getDataFromYahoo(goldStocks, 2, "gold_stocks")
