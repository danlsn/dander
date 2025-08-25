import sys
from pathlib import Path
from typing import Annotated
import typer
from loguru import logger
import dander.io.json_utils as json_utils
import dander.io.xml_utils as xml_utils

app = typer.Typer()
json_app = typer.Typer()
app.add_typer(json_app, name="json")
xml_app = typer.Typer()
app.add_typer(xml_app, name="xml")


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


@xml_app.command("format")
def reformat_xml(
    file_path: str,
    *,
    strict: Annotated[
        bool,
        typer.Option(
            "--strict",
            "-s",
            help="Enforce strict-mode XML formatting, input file must be an XML file.",
        ),
    ] = True,
    indent: Annotated[
        int,
        typer.Option(
            "--indent",
            "-i",
            help="Number of spaces used per indentation level for XML formatting.",
        ),
    ] = 2,
    write_file: Annotated[
        bool,
        typer.Option("--write", "-w", help="Write formatted XML to file in-place."),
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Print formatted XML to console.")
    ] = False,
):
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter="my_module",
        level="DEBUG" if verbose else "INFO",
    )
    xml_utils.reformat_xml_file(
        file_path, strict=strict, indent=indent, write_file=write_file, verbose=verbose
    )


@app.command()
def basename(file_path: Path = None):
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
