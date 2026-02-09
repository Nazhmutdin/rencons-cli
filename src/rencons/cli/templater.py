import json
from pathlib import Path
from typing import Annotated

from rich import print as rich_print
from typer import Option, Typer

from rencons.core.interactors.templater import (
    GenerateWelderExperienceAgeCertsInteractor,
    GenerateWelderNaksAgreementsInteractor,
    GenerateWelderNaksAttestationRequestsInteractor,
    WelderNaksAttesttaionConfig,
)

templater_group = Typer(no_args_is_help=True)


@templater_group.command("generate-welder-naks-attestation-docs", no_args_is_help=True)
def generate_welder_naks_attestation_requests(
    dir: Annotated[Path, Option()],
    templates_dir: Annotated[Path, Option()] = Path("./static/templates"),
):
    if not dir.exists():
        rich_print(f"[red]Data file path doesn't exists ({dir})")
        return

    if not dir.is_dir():
        rich_print(f"[red]Input path must be path to directory ({dir})")
        return

    generate_eqperience_certs = GenerateWelderExperienceAgeCertsInteractor(
        templates_dir
    )
    generate_requests = GenerateWelderNaksAttestationRequestsInteractor(templates_dir)
    generate_agreements = GenerateWelderNaksAgreementsInteractor(templates_dir)

    data: WelderNaksAttesttaionConfig = json.load(
        open(dir / "data.json", "r", encoding="utf-8")
    )
    
    for personal in data["personals"]:
        welder_dir = dir / f"{personal['passNumber']} {personal['name']}"

        welder_dir.mkdir(parents=True, exist_ok=True)

        for child in welder_dir.iterdir():
            if child.is_file():
                child.unlink()

    generate_requests(data, dir)
    generate_eqperience_certs(data, dir)
    generate_agreements(data, dir)
