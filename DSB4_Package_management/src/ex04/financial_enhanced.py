import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import gzip
import io
import pstats
import cProfile

def find(content, title):
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
    request = Request(url, headers=headers)

    try:
        with urlopen(request) as response:
            raw_data = response.read()
            if response.headers.get('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                    content = gz.read().decode("utf-8")
            return content
    except HTTPError as e:
        raise Exception(f"HTTP error: {e.code} — {e.reason}")
    except URLError as e:
        raise Exception(f"URL error: {e.reason}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    if len(sys.argv) != 3:
        raise Exception("Incorrect number of arguments")
    ticker = sys.argv[1]
    title = sys.argv[2]
    content = request_url(ticker)
    result = find(content, title)
    print(result)

    stream = io.StringIO()
    ps = pstats.Stats(profiler, stream=stream).sort_stats('cumtime')
    ps.print_stats(5)
    print(stream.getvalue())
    profiler.disable()

if __name__ == '__main__':
    main()