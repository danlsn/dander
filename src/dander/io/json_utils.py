"""
JSON utilities: formatting, splitting, validation
"""
import json
from typing import Any, List, Optional

try:
    import jsonschema
except ImportError:
    jsonschema = None


def pretty_print(obj: Any, indent: int = 2) -> str:
    """Return a pretty-printed JSON string."""
    return json.dumps(obj, indent=indent, ensure_ascii=False)

def reformat_json_file(file_path: str, write_file: bool = False, verbose: bool = False):
    """Reformat a JSON file. Optionally write in-place or print to console."""
    from pathlib import Path
    import rich
    import json
    from loguru import logger
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

def split_json_file(file_path: str, depth: int = 1, verbose: bool = False):
    """Split a JSON file at the top level into separate files."""
    from pathlib import Path
    import json
    from loguru import logger
    file_path = Path(file_path)
    if file_path.is_dir():
        logger.error(f"Path is a directory: {file_path}")
        raise ValueError(f"Path is a directory: {file_path}")
    with file_path.open() as f:
        logger.debug(f"Reformatting JSON file: {file_path}")
        data: dict | list = json.load(f)
    if not isinstance(data, dict) and not isinstance(data, list):
        logger.error(f"JSON data is not a dict or list: {data}")
        raise ValueError(f"JSON data is not a dict or list: {data}")
    if isinstance(data, dict):
        output = {f"{file_path.stem}__{k}": v for k, v in data.items()}
    else:
        output = {f"{file_path.stem}__{i}": v for i, v in enumerate(data)}
    for k, v in output.items():
        logger.debug(f"Writing JSON file: {file_path.parent / f'{k}.json'}")
        with (file_path.parent / f"{k}.json").open("w") as f:
            json.dump(v, f, indent=2)

def split_json_array(json_str: str) -> List[Any]:
    """Split a JSON array string into a list of objects."""
    arr = json.loads(json_str)
    if not isinstance(arr, list):
        raise ValueError("Input is not a JSON array")
    return arr

def validate_json(instance: Any, schema: dict) -> Optional[str]:
    """Validate a JSON object against a schema. Returns None if valid, else error message."""
    if jsonschema is None:
        raise ImportError("jsonschema is required for validation")
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return None
    except jsonschema.ValidationError as e:
        return str(e)
