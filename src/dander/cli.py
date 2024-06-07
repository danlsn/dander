import json
from pathlib import Path

import typer


app = typer.Typer()


@app.command()
def reformat_json(file_path: str):
    print(f"Reformatting JSON file: {file_path}")
    file_path = Path(file_path)
    with file_path.open() as f:
        data = json.load(f)
    with file_path.open('w') as f:
        json.dump(data, f, indent=4)
    print("Done.")


if __name__ == "__main__":
    app()
