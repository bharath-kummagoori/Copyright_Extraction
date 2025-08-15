import pytest
from pathlib import Path

from reader import _read_text


def test_read_text_nonexistent_path(tmp_path):
    # create a path that does not exist
    non_existent = tmp_path / "missing.txt"
    assert not non_existent.exists()
    with pytest.raises(FileNotFoundError):
        _read_text(non_existent)


def test_read_text_directory(tmp_path):
    # tmp_path is a directory itself
    with pytest.raises(IsADirectoryError):
        _read_text(tmp_path)
