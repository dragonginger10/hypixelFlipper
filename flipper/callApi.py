import requests
from rich import print

BAZAAR="https://api.hypixel.net/skyblock/bazaar"

def callapi():
    response = requests.get(BAZAAR)

    if response.status_code != 200:
        print("API call failed")
    else:
        print("API call success")

    r_json = response.json()

    for product in r_json["products"]:
        print(product["quick_status"])
