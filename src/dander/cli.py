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


@app.command()
def split_json_file(
        file_path: str,
        *,
        depth: Annotated[int, typer.Option("--depth", "-d", help="Depth to split JSON file at.")] = 1,
        verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Print debug logs to console.")] = False,
):
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG" if verbose else "INFO")
    file_path: Path = Path(file_path)
    if file_path.is_dir():
        logger.error(f"Path is a directory: {file_path}")
        raise typer.Exit(code=1)

    with Path(file_path).open() as f:
        logger.debug(f"Reformatting JSON file: {file_path}")
        data: dict | list = json.load(f)

    if not isinstance(data, dict) and not isinstance(data, list):
        logger.error(f"JSON data is not a dict or list: {data}")
        raise typer.Exit(code=1)

    if isinstance(data, dict):
        output = {f"{file_path.stem}__{k}": v for k, v in data.items()}
    else:
        output = {f"{file_path.stem}__{i}": v for i, v in enumerate(data)}

    for k, v in output.items():
        logger.debug(f"Writing JSON file: {file_path.parent / f'{k}.json'}")
        with Path(file_path.parent / f"{k}.json").open("w") as f:
            json.dump(v, f, indent=2)

    # if not write_file or verbose:
    #     logger.debug("Printing formatted JSON to console")
    #     rich.print(data)
    # else:
    #     logger.debug("Writing formatted JSON to file in-place")
    #     with Path(file_path).open("w") as f:
    #         json.dump(data, f, indent=4)


if __name__ == "__main__":
    app()
