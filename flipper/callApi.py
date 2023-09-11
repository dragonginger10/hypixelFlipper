import requests

BAZAAR="https://api.hypixel.net/skyblock/bazaar"

response = requests.get(BAZAAR)

if response.status_code != "200":
    print("API call failed")
else:
    print("API call success")
