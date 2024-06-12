import sys
import json
from pathlib import Path
from typing import Annotated

import rich
import typer
from loguru import logger

app: typer.Typer = typer.Typer()


@app.command()
def reformat_json(
    file_path: str,
    *,
    write_file: Annotated[bool, typer.Option("--write", "-w", help="Write formatted JSON to file in-place.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Print formatted JSON to console.")] = False,
):
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG" if verbose else "INFO")
    with Path(file_path).open() as f:
        logger.debug(f"Reformatting JSON file: {file_path}")
        data: dict = json.load(f)

    if not write_file or verbose:
        logger.debug("Printing formatted JSON to console")
        rich.print(data)
    else:
        logger.debug("Writing formatted JSON to file in-place")
        with Path(file_path).open("w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    app()
