import json
from pathlib import Path
from typing import Annotated

from rich import print as rich_print
from typer import Option, Typer

from rencons.core.dto import CertDataDTO
from rencons.core.interactors.wedler_registry import AddDataToWelderRegistryInteractor

welder_registry_group = Typer(no_args_is_help=True)


@welder_registry_group.command("add-data", no_args_is_help=True)
def add_data_to_welder_registry(
    data_path: Annotated[Path, Option()],
    group: Annotated[str, Option()],
    group_key: Annotated[str, Option()],
    save_path: Annotated[Path | None, Option()] = None,
    registry_path: Annotated[Path, Option(exists=True, resolve_path=True)] = Path(
        "./static/welder-registry.xlsx"
    ),
    sub_group: Annotated[str, Option()] = "-"
):
    if not registry_path.exists():
        rich_print(f"[red]Welder registry file path doesn't exists ({registry_path})")
        return

    if not registry_path.is_file():
        rich_print(f"[red]Input path must be path to file ({registry_path})")
        return

    data = [
        CertDataDTO(**el) for el in json.load(open(data_path, "r", encoding="utf-8"))
    ]

    add_data = AddDataToWelderRegistryInteractor()

    wb = add_data(registry_path, data, group, group_key, sub_group)

    if save_path is not None:
        wb.save(save_path)

        return

    wb.save(registry_path)
