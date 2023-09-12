import sys
import pandas as pd
from typing import Optional

from rich.table import Table

import requests

BAZAAR="https://api.hypixel.net/skyblock/bazaar"
ITEMS = "https://api.hypixel.net/resources/skyblock/items"

def getBazaar() -> pd.DataFrame:
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

        if sell_price == 0 or buy_price == 0:
            continue

        margin = buy_price/sell_price

        if margin < 50:
            continue

        data = {
            "ID": id,
            "Sell Price": "${:,.2f}".format(sell_price),
            "Buy Price": "${:,.2f}".format(buy_price),
            "Instabuys last 7 days": buy_week,
            "Profit Margin": "{:,.1f}%".format(margin)
        }

        results.append(data)

    df = pd.DataFrame(results)

    return df


def itemNames() -> pd.DataFrame:
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

        if npc_sell == None:
            continue

        data = {
            "ID": id,
            "Name": name,
            "NPC Sell Price": "${:,.2f}".format(npc_sell) 
        }

        results.append(data)

    df = pd.DataFrame(results)

    return df

def finalDf() -> pd.DataFrame:
    bazaarDf = getBazaar()
    namesDf = itemNames()

    merged = pd.merge(bazaarDf, namesDf)
    merged.pop("ID")
    names = merged.pop("Name")
    merged.insert(0, "Name", names)

    return merged.sort_values(by=["Profit Margin"])

def printOut(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
    ) -> Table:

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table
