
import sys
from pathlib import Path
from typing import Annotated
import typer
from loguru import logger
from .io import json_utils

app = typer.Typer()
json_app = typer.Typer()
app.add_typer(json_app, name="json")


@json_app.command("format")
def reformat_json(
    file_path: str,
    *,
    write_file: Annotated[
        bool,
        typer.Option("--write", "-w", help="Write formatted JSON to file in-place."),
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Print formatted JSON to console.")
    ] = False,
):
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter="my_module",
        level="DEBUG" if verbose else "INFO",
    )
    json_utils.reformat_json_file(file_path, write_file=write_file, verbose=verbose)


@json_app.command("split")
def split_json_file(
    file_path: str,
    *,
    depth: Annotated[
        int, typer.Option("--depth", "-d", help="Depth to split JSON file at.")
    ] = 1,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Print debug logs to console.")
    ] = False,
):
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter="my_module",
        level="DEBUG" if verbose else "INFO",
    )
    try:
        json_utils.split_json_file(file_path, depth=depth, verbose=verbose)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)


@app.command()
def basename(file_path: Path=None):
    """
    Get the basename of a file path.
    """
    if file_path is None:
        try:
            import pyperclip
            logger.info("No file path provided. Getting file path from clipboard.")
            file_path = pyperclip.paste()
        except ImportError:
            logger.error("pyperclip is not installed. Please install it using pip.")
            raise typer.Exit(code=1)
    logger.debug(f"Getting basename of file path: {file_path}")
    return Path(file_path).stem


if __name__ == "__main__":
    app()
