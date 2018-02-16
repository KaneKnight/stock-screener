from bs4 import BeautifulSoup
import requests

#Where data comes from
goldStocks = "http://www.miningfeeds.com/gold-mining-report-all-countries"

#url must contain a table with tickers as the first table
#and tickerColumn contains the column where the tickers are indexed at 0.
def parseTickersFromHtmlTable(url, tickerColumn):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table")
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[tickerColumn].text
        tickers.append(ticker)
    return tickers

print(parseTickersFromHtmlTable(goldStocks, 2));
