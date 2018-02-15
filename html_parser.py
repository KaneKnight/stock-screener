from bs4 import BeautifulSoup

#Where data comes from
#url = "http://www.miningfeeds.com/gold-mining-report-all-countries"

def parseGoldStocks():
    fp = open("gold_stocks.txt", "r")
    htmlString = fp.read()
    fp.close()
    stockSoup = BeautifulSoup(htmlString, 'html.parser')
    table = stockSoup.find("table")
    rows = table.findAll("tr")[1::]
    data = [[]]
    for row in rows:
        col = row.findAll("td")[2]
        ticker = str(col)
        ticker = ticker.split("<td>")
        ticker = ticker[1].split("</td>")
        data.append(ticker[0])
    return data[1::]

print(parseGoldStocks())
