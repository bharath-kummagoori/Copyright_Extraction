from pathlib import Path
from typing import Union


def _read_text(path: Union[str, Path]) -> str:
    """Read and return text from the given path.

    Parameters
    ----------
    path: Union[str, Path]
        Path to the text file.

    Returns
    -------
    str
        The contents of the file.
    """
    p = Path(path)
    # Path.read_text will raise FileNotFoundError if the path does not exist
    # and IsADirectoryError if the path is a directory.
    return p.read_text()
