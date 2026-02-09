import sys

from typer import Typer

from rencons.cli import app_group, naks_group, templater_group, welder_registry_group


def entrypoint():
    cli = Typer(no_args_is_help=True)
    cli.add_typer(app_group)
    cli.add_typer(naks_group, name="naks")
    cli.add_typer(welder_registry_group, name="welder-regitry")
    cli.add_typer(templater_group, name="templater")

    if len(sys.argv) == 1:
        sys.argv.append('--help')

    try:
        cli()
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
