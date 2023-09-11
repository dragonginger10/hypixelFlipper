

    table = Table(title="Bazaar Flips")

    table.add_column("Product", justify="center", style="cyan")
    table.add_column("Sell price", justify="center", style="green")
    table.add_column("Buy Price", justify="center", style="red")
    table.add_column("Instant Buys", justify="center", style="cyan")
    table.add_column("Profit Margin", justify="center", style="green")

    product_list = []

    for i in products:
        id = products[i]["quick_status"]["productId"]
        sell_price = products[i]["quick_status"]["sellPrice"]
        buy_price = products[i]["quick_status"]["buyPrice"]
        buy_week = products[i]["quick_status"]["buyMovingWeek"]

        if sell_price == 0.0 or buy_price == 0.0:
            continue

        margin = (buy_price/sell_price)

        if margin > 100 and buy_week > 1000:
            product_list.append((id, sell_price, buy_price, margin, buy_week))


    for id, sell_price, buy_price, margin, buy_week in sorted(product_list, key=lambda item: item[3], reverse=True):
        table.add_row(id, '${:,.2f}'.format(sell_price), '${:,.2f}'.format(buy_price), '{:,}'.format(buy_week),'{:,.1f}%'.format(margin))

    console = Console()
    console.print(table)
