import logging

NUM_OF_STEPS = 3
REPORT_FILENAME = "report"
REPORT_EXTENSION = "txt"
REPORT_TEMPLATE = """We made {total} observations by tossing a coin: {tails} were tails and {heads} were heads. The probabilities are {tails_percent}% and {heads_percent}%, respectively. Our forecast is that the next {steps} observations will be: {forecast}."""

TELEGRAM_TOKEN = "8551695984:AAGjfBGuvwD0kq2D3LjdyC2QuxlbaRCXCHI"
TELEGRAM_CHAT_ID = "-5038932852"

class AnalyticsFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        s = (f"{ct.tm_year:04d}-{ct.tm_mon:02d}-{ct.tm_mday:02d} "
             f"{ct.tm_hour:02d}:{ct.tm_min:02d}:{ct.tm_sec:02d}")
        millis = int(record.msecs)
        return f"{s},{millis:03d}"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers.clear()
handler = logging.FileHandler("analytics.log", encoding="utf-8")
formatter = AnalyticsFormatter(fmt="%(asctime)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)