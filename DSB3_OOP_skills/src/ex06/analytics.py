from random import randint
import logging
import urllib.request
import json
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class Research:
    def __init__(self, path):
        logging.debug(f"Initializing Research with path: {path}")
        self.path = path

    def file_reader(self, has_header=True):
        logging.debug(f"Starting file reading: {self.path}")
        try:
            with open(self.path, "r") as file:
                logging.debug("File opened successfully")
                lines = file.read().strip().split("\n")
                logging.debug(f"Read {len(lines)} lines")
        except Exception as e:
            logging.debug(f"Error opening/reading file: {e}")
            raise Exception(f"Cannot read file: {e}")

        logging.debug("Checking file structure")
        if not self.check_structure(lines):
            logging.debug("File structure validation failed")
            raise Exception("Invalid file structure")

        if has_header:
            logging.debug("Skipping header line")
            lines = lines[1:]

        data = []
        for line in lines:
            data.append([int(x) for x in line.split(",")])

        logging.debug(f"Successfully parsed {len(data)} observations")
        return data

    def check_structure(self, lines):
        logging.debug("Starting structure validation")
        if len(lines) < 2:
            logging.debug("Too few lines in file")
            return False

        if lines[0] != "head,tail":
            logging.debug(f"Invalid header: {lines[0]}")
            return False

        for line in lines[1:]:
            if line not in ["0,1", "1,0"]:
                logging.debug(f"Invalid data line: {line}")
                return False

        logging.debug("File structure is valid")
        return True

    def send_telegram(self, success: bool):
        logging.debug("Preparing Telegram notification")
        message = (
            "The report has been successfully created"
            if success
            else "The report hasn't been created due to an error."
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method="POST"
        )
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    logging.debug("Telegram notification sent successfully")
                else:
                    resp_body = response.read().decode()
                    logging.debug(f"Telegram error {response.status}: {resp_body}")
        except Exception as e:
            logging.debug(f"Exception during Telegram send: {e}")


class Calculations:
    def __init__(self, data):
        logging.debug(f"Initializing Calculations with {len(data)} observations")
        self.data = data

    def counts(self):
        logging.debug("Calculating counts of heads and tails")
        heads = 0
        tails = 0
        for item in self.data:
            if item == [1, 0]:
                heads += 1
            elif item == [0, 1]:
                tails += 1
        logging.debug(f"Counts calculated: heads={heads}, tails={tails}")
        return heads, tails

    def fractions(self):
        logging.debug("Calculating fractions")
        heads, tails = self.counts()
        total = heads + tails
        heads_frac = round(heads / total, 4) if total else 0
        tails_frac = round(tails / total, 4) if total else 0
        logging.debug(f"Fractions: heads={heads_frac}, tails={tails_frac}")
        return heads_frac, tails_frac


class Analytics(Calculations):
    def predict_random(self, n):
        logging.debug(f"Generating {n} random predictions")
        result = []
        for _ in range(n):
            r = randint(0, 1)
            if r == 1:
                result.append([1, 0])
            else:
                result.append([0, 1])
        heads_pred = result.count([1, 0])
        tails_pred = result.count([0, 1])
        logging.debug(f"Random prediction result: {heads_pred} heads, {tails_pred} tails")
        return result

    def predict_last(self):
        logging.debug("Predicting next observation as the last one")
        last = self.data[-1]
        logging.debug(f"Last observation: {last}")
        return last

    def save_file(self, data, filename, extension):
        full_name = f"{filename}.{extension}"
        logging.debug(f"Saving report to {full_name}")
        with open(full_name, "w") as file:
            file.write(data)
        logging.debug("Report saved successfully")