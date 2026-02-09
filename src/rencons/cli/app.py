from rich import print as rich_print
from typer import Typer

app_group = Typer(no_args_is_help=True)


@app_group.command("status")
def status():
    rich_print("[green]Ok")
