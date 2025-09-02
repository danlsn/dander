try:
    from git import Repo
except ImportError:
    msg = f"""
        GitPython is not installed. Please install the dander git extra using:

        ```bash
        pip install dander[git]
        ```
        """
    raise ImportError(msg)
