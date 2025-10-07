"""Tests for miscellaneous dlsite_classification.tools modules."""
from __future__ import annotations

from pathlib import Path

import pytest

from dlsite_classification.tools.copy import copy_data
from dlsite_classification.tools.rep import replace_file_name
from dlsite_classification.tools.saerch import search_file_code
from dlsite_classification.tools.scan import get_folder_cla_struct


@pytest.mark.asyncio
async def test_copy_data_copies_file(tmp_path: Path):
    origin = tmp_path / "origin.bin"
    origin.write_bytes(b"abc123")
    target = tmp_path / "copied.bin"

    await copy_data(str(origin), str(target))

    assert target.read_bytes() == b"abc123"
    assert origin.read_bytes() == b"abc123"


@pytest.mark.asyncio
async def test_copy_data_missing_origin(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        await copy_data(str(tmp_path / "missing.bin"), str(tmp_path / "target.bin"))


def test_replace_file_name_replaces_invalid_chars():
    assert replace_file_name("file:name?.txt") == "file_name_.txt"


def test_replace_file_name_handles_non_string():
    """Test that non-string inputs are converted to string and processed."""
    # When passed a non-string object, it should convert to string
    obj = object()
    result = replace_file_name(obj)
    # Result should be a string representation with invalid chars replaced
    assert isinstance(result, str)
    assert "_object" in result.lower()  # object repr contains "object"


def test_search_file_code_finds_code_in_folders(tmp_path: Path):
    folder = tmp_path / "[Circle]"
    target = folder / "RJ123456_Title"
    target.mkdir(parents=True)
    assert search_file_code(str(tmp_path)) == "RJ123456"


def test_search_file_code_reads_files(tmp_path: Path):
    folder = tmp_path / "Circle"
    folder.mkdir()
    (folder / "info_RJ888999.txt").write_text("data", encoding="utf-8")
    assert search_file_code(str(tmp_path)) == "RJ888999"


def test_search_file_code_returns_empty_when_missing(tmp_path: Path):
    (tmp_path / "no_codes").mkdir()
    assert search_file_code(str(tmp_path)) == ""


def test_get_folder_cla_struct_returns_mapping(tmp_path: Path):
    company = tmp_path / "[Maker]"
    work = company / "RJ111222 Work"
    info = work / "RJ111222_info"
    info.mkdir(parents=True)
    mapping = get_folder_cla_struct(str(tmp_path))
    assert list(mapping.keys()) == ["[Maker]"]
    assert work.name in mapping["[Maker]"]
    assert mapping["[Maker]"][work.name] == str(work)
