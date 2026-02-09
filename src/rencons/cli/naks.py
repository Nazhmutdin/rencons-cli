import json
from asyncio import get_event_loop
from pathlib import Path
from typing import Annotated

from rich import print as rich_print
from rich.prompt import Prompt
from typer import Option, Typer

from rencons.core.interactors.naks_bot import ParseCertsByKleymoInteractor
from rencons.utils.progress import get_progress

naks_group = Typer(no_args_is_help=True)


overwrite_output_file_prompt = """
[yellow]Output file already exists. Would you like to [bold yellow]overwrite[/] it?
"""


@naks_group.command("parse-kleymos", no_args_is_help=True)
def parse_kleymos(
    input_path: Annotated[Path, Option(help="path to json file with kleymos")],
    output_path: Annotated[Path, Option()],
):
    if not input_path.exists():
        rich_print(f"[red]Kleymos list file path doesn't exists ({input_path})")
        return

    if not input_path.is_file():
        rich_print(f"[red]Input path must be path to file ({input_path})")
        return

    if output_path.exists():
        answer = Prompt.ask(
            overwrite_output_file_prompt.strip(),
            choices=["Yes", "No"],
            default="Yes",
            case_sensitive=False,
        )

        if answer == "No":
            return

    loop = get_event_loop()

    parse = ParseCertsByKleymoInteractor()

    result = []

    kleymos = json.load(open(input_path, "r", encoding="utf-8"))

    if not isinstance(kleymos, list):
        rich_print("[red]Input file should be list of strings")

    with get_progress() as progress:
        task = progress.add_task("parse naks bot...", total=len(kleymos))

        for kleymo in kleymos:
            result += loop.run_until_complete(parse(kleymo))

            progress.advance(task, 1)

    rich_print("[green]Done")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump([el.__dict__ for el in result], file, indent=4, ensure_ascii=False)
