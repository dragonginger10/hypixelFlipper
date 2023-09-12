from typing import Optional, Annotated

import typer
from rich.console import Console
from rich.table import Table

from flipper import __version__
from flipper.getData import finalDf, printOut

console = Console()

def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()

def main(
    version: Annotated[
        Optional[bool], 
        typer.Option(None, "--version", callback=version_callback, is_eager=True)
    ] = None
):
    df = finalDf()

    table = Table("Bazaar Flips", show_header=True, header_style="bold cyan")

    table = printOut(df, table, False)
    console.print(table)

if __name__ == "__main__":
    typer.run(main)
