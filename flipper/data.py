import pandas as pd
import requests
import sys

ITEMS = "https://api.hypixel.net/resources/skyblock/items"

def itemNames():
    response = requests.get(ITEMS)

    if response.status_code != 200:
        print("API call failed.") 
        sys.exit(1)

    items = response.json()

    results = []

    for item in items["items"]:
        id = item["id"]
        name = item["name"]
        npc_sell = item.get("npc_sell_price")

        data = {
            "id": id,
            "name": name,
            "npc_sell": npc_sell 
        }

        results.append(data)

    df = pd.DataFrame(results)

    return df
