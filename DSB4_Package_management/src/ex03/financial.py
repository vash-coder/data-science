import sys
import time
from bs4 import BeautifulSoup
import requests


def find(content, title):
    time.sleep(5)
    soup = BeautifulSoup(content, "lxml")
    error = soup.find("div", class_="noData")
    if error is not None:
        raise Exception("Ticker not found")
    try:
        tag = tuple(soup.find(title=f"{title}").find_parent("div").find_parent("div").stripped_strings)
    except AttributeError:
        raise Exception("Field of the table as arguments not found")
    return tag


def request_url(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36 Edge/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    content = requests.get(url, headers=headers)
    return content.text


def main():
    if len(sys.argv) != 3:
        raise Exception("Incorrect number of arguments")
    ticker = sys.argv[1]
    title = sys.argv[2]
    content = request_url(ticker)
    result = find(content, title)
    print(result)


if __name__ == '__main__':
    main()