from typing import Optional

import pandas as pd
import requests
import typer
from rich.table import Table

BAZAAR = "https://api.hypixel.net/skyblock/bazaar"
ITEMS = "https://api.hypixel.net/resources/skyblock/items"


def getBazaar(
    instabuys: int,
    profit: float,
    ) -> pd.DataFrame:
    response = requests.get(BAZAAR)

    if response.status_code != 200:
        print("API call failed")
        raise typer.Exit(code=1)

    r_json = response.json()
    products = r_json["products"]
    results = []

    for i in products:
        id = products[i]["quick_status"]["productId"]
        sell_price = products[i]["quick_status"]["sellPrice"]
        buy_price = products[i]["quick_status"]["buyPrice"]
        buy_week = products[i]["quick_status"]["buyMovingWeek"]

        if buy_week < instabuys:
            continue

        if sell_price == 0 or buy_price == 0:
            continue

        margin = buy_price / sell_price

        if margin < profit:
            continue

        data = {
            "ID": id,
            "Sell Price": "${:,.2f}".format(sell_price),
            "Buy Price": "${:,.2f}".format(buy_price),
            "Instabuys last 7 days": buy_week,
            "Profit Margin": margin,
        }

        results.append(data)

    df = pd.DataFrame(results)

    return df


def itemNames() -> pd.DataFrame:
    response = requests.get(ITEMS)

    if response.status_code != 200:
        print("API call failed.")
        raise typer.Exit(code=1)

    items = response.json()

    results = []

    for item in items["items"]:
        id = item["id"]
        name = item["name"]
        npc_sell = item.get("npc_sell_price")

        if npc_sell is None:
            continue

        data = {"ID": id, "Name": name, "NPC Sell Price": npc_sell}


        results.append(data)

    df = pd.DataFrame(results)

    return df


def finalDf(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    ) -> pd.DataFrame:
    merged = pd.merge(df1, df2)
    merged.pop("ID")
    names = merged.pop("Name")
    merged.insert(0, "Name", names)

    return merged.sort_values(by=["Profit Margin"], ascending=False)


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

    for index, value_list in enumerate(pandas_dataframe.to_numpy()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        name, sellPrice, buyPrice, instaBuys, margin, npcPrice = row
        rich_table.add_row(name, sellPrice, buyPrice, instaBuys, "{:,.1f}%".format(float(margin)), "${:,.2f}".format(float(npcPrice)))

    return rich_table
