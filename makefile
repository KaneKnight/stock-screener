all: stock_screener.py
	rm -rf gold_stocks_data
	python3 stock_screener.py
clean:
	rm -rf gold_stocks_data __pycache__
