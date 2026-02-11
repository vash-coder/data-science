import sys


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


def all_stocks(items):
    for item in items:
        ticker = item.upper()

        if ticker in STOCKS:
            company = next(
                c for c, t in COMPANIES.items()
                if t == ticker
            )
            print(f"{ticker} is a ticker symbol for {company}")

        else:
            company = next(
                (c for c in COMPANIES if c.lower() == item.lower()),
                None
            )

            if company:
                ticker = COMPANIES[company]
                price = STOCKS[ticker]
                print(f"{company} stock price is {price}")

            else:
                print(f"{item} is an unknown company or an unknown ticker symbol")


def parse_argv(argv):
    if len(argv) < 2:
        sys.exit(1)

    if len(argv) == 2:
        raw_items = argv[1].split(',')
    else:
        raw_items = argv[1:]

    return [item.strip() for item in raw_items if item.strip()]


def main():
    items = parse_argv(sys.argv)
    all_stocks(items)


if __name__ == "__main__":
    main()
