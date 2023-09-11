import sys
import pandas as pd

import requests

BAZAAR="https://api.hypixel.net/skyblock/bazaar"

def callapi():
    response = requests.get(BAZAAR)

    if response.status_code != 200:
        print("API call failed")
        sys.exit(1)

    r_json = response.json()
    products = r_json["products"]
    results = []

    for i in products:
        id = products[i]["quick_status"]["productId"]
        sell_price = products[i]["quick_status"]["sellPrice"]
        buy_price = products[i]["quick_status"]["buyPrice"]
        buy_week = products[i]["quick_status"]["buyMovingWeek"]

        data = {
            "id": id,
            "sell_price": sell_price,
            "buy_price": buy_price,
            "buy_week": buy_week
        }

        results.append(data)

    df = pd.DataFrame(results)
