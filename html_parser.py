from bs4 import BeautifulSoup
import requests
import pickle

#Where data comes from
goldStocks = "http://www.miningfeeds.com/gold-mining-report-all-countries"

#url must contain a table with tickers as the first table
#and tickerColumn contains the column where the tickers are indexed at 0.
def parseTickersFromHtmlTable(url, tickerColumn, stockTypes):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table")
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[tickerColumn].text
        tickers.append(ticker)

    with open(stockTypes + ".pickle", "wb") as file:
        pickle.dump(tickers, file)

    return tickers

print(parseTickersFromHtmlTable(goldStocks, 2, "gold-stocks"));
