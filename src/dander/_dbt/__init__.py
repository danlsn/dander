try:
    from dbt.cli.main import dbtRunner, dbtRunnerResult
except ImportError:
    msg = f"""
        dbt is not installed. Please install the dander dbt extra using:
        
        ```bash
        pip install dander[dbt]
        ```
        """
    raise ImportError(msg)
