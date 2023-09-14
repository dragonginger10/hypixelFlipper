from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from flipper import __version__
from flipper.getData import finalDf, printOut, getBazaar, itemNames

console = Console()
app = typer.Typer()


def _version_callback(value: bool = False):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=_version_callback, is_eager=True
    ),
    instabuys: Optional[int] = typer.Option(
        10000, 
        "--instabuys",
        "-i",
        help="Number of instabuys in last seven days",
    ),
    profit: Optional[float] = typer.Option(
        5.0,
        "--profit",
        "-p",
        help="minimum Profit margin to show"
    )
    
):
    df = finalDf(getBazaar(instabuys, profit), itemNames())

    table = Table(title="Bazaar Flips", show_header=True, header_style="bold cyan")

    table = printOut(df, table, False)
    console.print(table)
