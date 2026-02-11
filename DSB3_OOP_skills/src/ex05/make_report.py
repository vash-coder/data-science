import sys
from analytics import Research, Analytics
from config import (
    NUM_OF_STEPS,
    REPORT_TEMPLATE,
    REPORT_FILENAME,
    REPORT_EXTENSION
)


def main():
    if len(sys.argv) != 2:
        raise Exception("Invalid number of arguments")

    path = sys.argv[1]
    research = Research(path)
    data = research.file_reader()

    analytics = Analytics(data)
    heads, tails = analytics.counts()
    total = heads + tails

    heads_percent = round(heads / total * 100, 2)
    tails_percent = round(tails / total * 100, 2)

    forecast = analytics.predict_random(NUM_OF_STEPS)

    forecast_heads = forecast.count([1, 0])
    forecast_tails = forecast.count([0, 1])

    forecast_text = f"{forecast_tails} tail and {forecast_heads} heads"

    report = REPORT_TEMPLATE.format(
        total=total,
        tails=tails,
        heads=heads,
        tails_percent=tails_percent,
        heads_percent=heads_percent,
        steps=NUM_OF_STEPS,
        forecast=forecast_text
    )

    analytics.save_file(
        report,
        REPORT_FILENAME,
        REPORT_EXTENSION
    )


if __name__ == "__main__":
    main()