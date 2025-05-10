import csv
import time

import gspread

MONTH = 'april'
SUBSCRIPTIONS = {"iliad", "valletta", "goldbet", "klarna", "scalapay"}
FOOD = {"bar", "pasticceria", "conad", "supermercato", "bontà", "cremeria"}
EARNINGS = {"emolumenti", "bonifico in entrata"}
CATEGORIES = [SUBSCRIPTIONS, FOOD, EARNINGS]
file = f"mediolanum_{MONTH}.csv"

transactions = []


def safe_float(value):
    value = value.replace('€', '').replace('â‚¬', '').replace(',', '.').strip()
    return float(value) if value else 0.0


def get_category(text):
    text = text.lower()
    if any(word in text for word in SUBSCRIPTIONS):
        return "Subscription"
    elif any(word in text for word in FOOD):
        return "Food"
    elif any(word in text for word in EARNINGS):
        return "Entry"
    else:
        return "Others"


def get_transaction(file):
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for _ in range(6):
            next(csv_reader)
        for row in csv_reader:
            date = row[0]
            name = row[3]
            print(name)
            category = get_category(name)
            out = safe_float(row[4].replace('€', ''))
            earned = safe_float(row[5].replace('€', ''))
            amount = out if out < 0 else earned
            transaction = (date, name, category, amount)
            transactions.append(transaction)
        return transactions


sa = gspread.service_account(filename='.venv/Lib/site-packages/gspread/service_account.json')
sh = sa.open("Personal Finances")

wks = sh.worksheet(f"{MONTH}")

rows = get_transaction(file)

for row in rows:
    wks.insert_row([row[0], row[1], row[2], row[3]], 7)
    time.sleep(2)


wks.insert_row([1, 2, 3], 100)

