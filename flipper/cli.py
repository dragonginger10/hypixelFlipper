from flipper.getData import printOut, finalDf
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    df = finalDf()

    table = Table(show_header=True, header_style="bold cyan")

    table = printOut(df, table)
    console.print(table)
