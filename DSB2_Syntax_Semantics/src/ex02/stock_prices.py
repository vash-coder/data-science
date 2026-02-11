import sys


def get_stock(company: str):
    stock = company.capitalize()
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

    if stock in COMPANIES:
        return STOCKS[COMPANIES[stock]]
    else:
        return 'Unknown company'


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    print(get_stock(sys.argv[1]))

    
if __name__ == "__main__":
    main()
