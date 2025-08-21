# DANDER API Design

DANDER (Data Analytics & Data Engineering Resources) gathers a wide range of
small utilities that make a data practitioner's day a bit easier. The project
offers a Python API and a Typer powered CLI that wrap common patterns found in
the data ecosystem.  Each module is intentionally light‑weight so that teams can
mix and match only the pieces they need.

## Package layout

```text
dander/
├── cli.py              # Command line interface
├── io/                 # File input/output helpers
│   ├── json_utils.py   # JSON formatting, splitting, validation
│   ├── csv_utils.py    # CSV helpers
│   ├── excel_utils.py  # Spreadsheet helpers (xls/xlsx/ods)
│   └── convert.py      # Convert between tabular formats
├── transform/          # Data transformation helpers
│   ├── dataframe.py    # Pandas / Polars helpers
│   └── dates.py        # Calendar arithmetic and parsing
├── profile/            # Dataset profiling
│   └── pandas_profile.py
├── db/                 # Database helpers
│   ├── connection.py   # Connection helpers (SQLAlchemy, etc.)
│   ├── query.py        # Simplified query execution
│   ├── duckdb.py       # DuckDB convenience wrappers
│   └── sqlite.py       # Thin layer over Python's sqlite3
├── datapack/           # [Frictionless] data package helpers
│   └── frictionless.py
├── dbt/                # Light wrappers around dbtRunner
│   ├── runner.py       # run/test/seed/compile/ls
│   └── artifacts.py    # read manifest, run results, catalog
├── validation/         # Data quality checks
│   └── checks.py
├── stdlib/             # Ergonomic wrappers over stdlib modules
│   ├── path.py         # Pathlib convenience helpers
│   ├── compression.py  # gzip/zip/tar helpers
│   └── csvlib.py       # High level wrappers for csv module
├── ids/                # Unique identifier utilities
│   ├── uuid_utils.py   # UUID1/4/6/7
│   └── ulid_utils.py   # ULID generation and parsing
└── hashing/            # Hashing and checksums
    └── digest.py       # sha256/md5/xxhash/crc32 helpers
```

## Key modules and ideas

### I/O helpers and file conversion

The `io` package focuses on mundane file operations:

- `json_utils` formats JSON, splits documents, and performs schema
  validation using `jsonschema`.
- `csv_utils` wraps the standard library `csv` module and pandas for
  quick CSV inspection.
- `excel_utils` uses `openpyxl`/`odfpy` to read and write spreadsheet
  files, normalising column names and data types.
- `convert` provides one‑liners to convert between JSON, CSV, Parquet and
  Arrow by leaning on `pandas` and `pyarrow`.

```bash
# Convert CSV to Parquet
$ dander convert input.csv output.parquet

# Preview a CSV file
$ dander csv head data.csv --rows 20
```

### Data transformations

`transform` groups helpers for small but frequent operations:

- `dataframe.py` offers column renaming, flattening of nested structures
  and lightweight schema enforcement for pandas/Polars DataFrames.
- `dates.py` standardises date parsing, timezone handling, business day
  offsets and rolling window calculations by wrapping `datetime`,
  `dateutil`, and `zoneinfo`.

```python
from dander.transform import dates

dates.parse_iso("2024-03-02T10:15:00Z")
dates.month_range("2024-01-01", months=3)
```

### Data profiling

Inspired by tools like
[ydata-profiling](https://github.com/ydataai/pandas-profiling), the
`profile` module produces quick HTML or Markdown reports that summarise a
dataset.

```bash
$ dander profile df.parquet --output report.html
```

### Database helpers and lightweight engines

The `db` package abstracts common SQL workflows:

- `connection.py` standardises creating SQLAlchemy engines and managing
  credentials.
- `query.py` executes parametrised SQL and returns DataFrames.
- `duckdb.py` exposes in‑process DuckDB for ad‑hoc analytics and easy
  integration with parquet/CSV/Arrow sources.
- `sqlite.py` leans on the Python stdlib's `sqlite3` for tiny
  reproducible datasets.

```python
from dander.db import duckdb

with duckdb.session() as con:
    con.sql("CREATE TABLE numbers AS SELECT range AS id FROM range(10)")
    df = con.sql("SELECT * FROM numbers").df()
```

### Data package integrations

To encourage reproducibility, `datapack` wraps the
[Frictionless](https://github.com/frictionlessdata/frictionless-py)
library.  Utilities allow quick creation, validation and publishing of
Data Packages.

```bash
# Validate a datapackage.json
$ dander datapack validate datapackage.json
```

### dbt integrations

DANDER bundles thin wrappers around `dbtRunner` so Python scripts and CLI
commands can orchestrate dbt without invoking the shell.  The `runner`
module exposes `run`, `test`, `seed`, `compile` and `ls` functions that
return structured results.  `artifacts.py` provides helpers to read the
`manifest.json`, `run_results.json` and `catalog.json` files and expose
them as DataFrames for further analysis.

```python
from dander.dbt.runner import run

res = run(project_dir="my_project", select="stg_users")
print(res.status, res.execution_time)
```

### Standard‑library conveniences

The `stdlib` package offers ergonomic wrappers over modules that data
teams regularly touch but are clunky to use:

- `path.py` adds helpers for temporary directories and atomic file
  writes.
- `compression.py` unifies `gzip`, `zipfile` and `tarfile` interfaces to
  make archive creation and extraction trivial.
- `csvlib.py` layers a pandas‑like interface over the built‑in `csv`
  reader for quick scripting.

### Date and time utilities

While many projects end up writing their own date helpers, DANDER's
`transform.dates` module consolidates common needs: ISO8601 parsing,
timezone conversions, calendar arithmetic, relative date ranges and
business day calculations.  The aim is to surface the most useful bits of
`datetime`, `dateutil`, and `pandas` without pulling in heavy
dependencies.

### Unique identifiers and hashing

The `ids` and `hashing` packages provide predictable interfaces for
generating identifiers and verifying data integrity:

- `ids.uuid_utils` exposes UUID1/4/6/7 helpers.
- `ids.ulid_utils` generates and parses ULIDs for lexicographically
  sortable IDs.
- `hashing.digest` computes md5/sha256/xxhash digests and file checksums
  and includes helpers for comparing directories.

```bash
$ dander ids uuid --version 7 --count 3
$ dander hash sha256 path/to/file.csv
```

### Validation

`validation.checks` allows developers to declare simple row/column rules
and run them against DataFrames or CSV files, returning structured error
reports that can feed into CI pipelines.

## Example Python API

```python
from dander.io import convert
from dander.profile.pandas_profile import profile
from dander.ids import ulid_utils

# Convert a CSV file and profile the result
convert.to_parquet("customers.csv", "customers.parquet")
profile("customers.parquet", output="profile.html")

# Generate a sortable identifier
order_id = ulid_utils.new()
```

## CLI overview

Each top level package registers a CLI subcommand:

```bash
$ dander json format data.json --write
$ dander csv to-json data.csv out.json
$ dander db duckdb-query "select count(*) from 'data.parquet'"
$ dander dbt run --project-dir my_dbt_project
$ dander ids ulid --count 5
$ dander hash md5 customers.parquet
```

## Design principles

* **Simple abstractions** – prefer a thin layer over existing libraries.
* **Composable** – functions return data structures that can be piped to the next utility.
* **Typed** – use type hints for discoverability and tooling.
* **Observable** – rely on `loguru` for logging and make logging opt‑in via the CLI.
* **Cross‑platform** – keep dependencies light and avoid OS‑specific features.
* **Batteries included** – expose common stdlib features behind ergonomic APIs so
  analysts don't have to remember incidental details.

This outline gives DANDER space to grow into a convenient toolkit that
mirrors the daily workflow of modern data professionals.

