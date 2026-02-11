import sys


def get_name_stock(ticker: str):
    ticker = ticker.upper()
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }

    REV_COMPANIES = {value: key for key, value in COMPANIES.items()}
    if ticker in STOCKS:
        return f'{REV_COMPANIES[ticker]} {STOCKS[ticker]}'
    else:
        return 'Unknown ticker'


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    print(get_name_stock(sys.argv[1]))


if __name__ == "__main__":
    main()
