import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from configurations import wantedRows, letterNumbers, percentageNumbers, dates
from converter import Converter
import pymongo
from config import password
from tickers import gold, spy
import logging
import datetime

class Miner:

    def __init__(self, baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString):
        self.baseurl = baseurl
        self.wantedRows = wantedRows
        self.letterNumbers = letterNumbers
        self.percentageNumbers = percentageNumbers
        self.dates = dates
        self.connection = pymongo.MongoClient(connString)

    def reformatData(self, data):
        """Reformat data with better names and remove redundancies"""
        dataDict = {}
        for index in self.wantedRows:
            series = data.loc[index]
            key = self.wantedRows[index]
            value = series.get(1)
            dataDict[key] = value
        return pd.Series(dataDict)

    def getCurrency(self, html):
        """Gets the string of the currency stock is priced in."""
        soup = bs(html, "lxml")
        results = soup.findAll("span", {"data-reactid" : "9"})
        i = 0
        line = None
        for result in results:
            if i == 1:
                line = result.text
            i += 1
        if line == None:
            return False, None
        return True, line[-3:] 
            
    def returnSeries(self, ticker):
        """Gets data from yahoo and dumps in csv file before 
        returning data as pandas series. Returns true, series if
        there is data, false, none if not."""

        #Go to summary page and scrape open.
        priceData = requests.get(baseurl + "%s?p=%s" % (ticker, ticker))       
        summaryFrames = pd.read_html(priceData.text)
        summaryFrame = pd.concat(summaryFrames, ignore_index=True)
        priceFrame = summaryFrame.loc[1:1]
        
        #Scrape currency from summary page.
        exists, currency = self.getCurrency(priceData.text)
        if not exists:
            return False, None
        
        #Go to stats page and scrape stats.
        data = requests.get(baseurl + "%s/key-statistics?p=%s" % (ticker, ticker))
        frames = pd.read_html(data.text)
        if len(frames) < 3:
            return False , None

        #Join stats and price
        frames.append(priceFrame)
        frame = pd.concat(frames, ignore_index=True)

        #Reformat
        try:
            reformattedSeries = self.reformatData(frame)
        except Exception:
            return False, None
        reformattedSeries["currency"] = currency.upper()

        # Convert letters to numbers
        letterMask = reformattedSeries.index.isin(self.letterNumbers)
        reformattedSeries[letterMask]= reformattedSeries[letterMask].apply(Converter.convertLetter)
        
        # Convert percentage to numbers
        percentMask = reformattedSeries.index.isin(self.percentageNumbers)
        reformattedSeries[percentMask] = reformattedSeries[percentMask].apply(Converter.convertPercent)

        # Try convert to float
        reformattedSeries = reformattedSeries.apply(Converter.tryConvertToFloat)

        # Add the name.
        reformattedSeries["ticker"] = ticker

        reformattedSeries["collected"] = datetime.date.today().isoformat() 

        return True, reformattedSeries

    def collectAndStore(self):
        for ticker in self.tickers:
            logging.info("Requesting:{}".format(ticker))
            exists, data = self.returnSeries(ticker)
            if exists:
                self.insertData(data)
            else:
                logging.warn("Ticker does not exist: {}".format(ticker))    




class GoldMiner(Miner):
    def __init__(self, baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString, tickers):
        super().__init__(baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString)
        self.tickers = tickers

    def insertData(self, data):
        d = data.to_dict()
        col = self.connection["stocks"]["gold"]
        col.insert_one(d)

class SpyMiner(Miner):
    
    def __init__(self, baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString, tickers):
        super().__init__(baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString)
        self.tickers = tickers

    def insertData(self, data):
        d = data.to_dict()
        col = self.connection["stocks"]["spy"]
        col.insert_one(d)        



if __name__ == "__main__":
    logging.basicConfig(filename="miner.log", filemode='a', level=logging.INFO)
    baseurl = "https://uk.finance.yahoo.com/quote/"
    connString = "mongodb+srv://improve:%s@improveatinvesting-s3ghn.mongodb.net/test?retryWrites=true&w=majority" % password
    miner = SpyMiner(baseurl, wantedRows, letterNumbers, percentageNumbers, dates, connString, spy)
    miner.collectAndStore()
    miner.connection.close()
