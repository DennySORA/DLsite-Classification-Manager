"""Tests for dlsite_classification.tools.move module."""
from __future__ import annotations

from pathlib import Path

import pytest

from dlsite_classification.tools import move as move_module
from dlsite_classification.tools.move import (
    extract_folder_top,
    merge_folder_name_move,
    move_folder,
    move_subfolder,
)


@pytest.fixture
def nested_structure(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "root"
    origin = root / "origin"
    target = root / "target"
    (origin / "sub1").mkdir(parents=True)
    (origin / "sub2").mkdir(parents=True)
    (origin / "sub1" / "file.txt").write_text("data", encoding="utf-8")
    (origin / "sub2" / "more.txt").write_text("more", encoding="utf-8")
    target.mkdir(parents=True)
    return root, origin, target


def test_move_subfolder_moves_all_children(nested_structure: tuple[Path, Path, Path]):
    root, origin, target = nested_structure
    move_subfolder(str(origin), str(target))
    assert not any(origin.iterdir())
    assert (target / "sub1" / "file.txt").read_text(encoding="utf-8") == "data"
    assert (target / "sub2" / "more.txt").read_text(encoding="utf-8") == "more"


def test_move_subfolder_with_cleanup(nested_structure: tuple[Path, Path, Path]):
    root, origin, target = nested_structure
    move_subfolder(str(origin), str(target), need_del=True)
    assert not origin.exists()


def test_move_subfolder_logs_errors(monkeypatch, nested_structure):
    root, origin, target = nested_structure
    seen = {"called": False}
    original = move_module.os.rename

    def flaky_rename(src, dst):
        if not seen["called"]:
            seen["called"] = True
            raise OSError("rename failed")

        return original(src, dst)

    monkeypatch.setattr("dlsite_classification.tools.move.os.rename", flaky_rename)
    move_subfolder(str(origin), str(target))

    assert seen["called"] is True


def test_move_folder_success(tmp_path: Path):
    root = tmp_path
    (root / "code" / "dest").mkdir(parents=True)
    origin_folder = "to_move"
    (root / origin_folder).mkdir()
    new_path = move_folder(str(root), "code", origin_folder)
    assert Path(new_path).is_dir()
    assert Path(new_path).parent == root / "code"


def test_move_folder_failure(monkeypatch, tmp_path: Path):
    root = tmp_path
    origin_folder = "folder"
    (root / origin_folder).mkdir()

    def bad_rename(_src, _dst):
        raise OSError("boom")

    monkeypatch.setattr("dlsite_classification.tools.move.os.rename", bad_rename)
    result = move_folder(str(root), "target", origin_folder)
    assert result == ""


def test_merge_folder_name_move_success(tmp_path: Path):
    base = tmp_path / "parent"
    (base / "child").mkdir(parents=True)
    result = merge_folder_name_move(str(base), "child", need_del=True)
    assert Path(result).is_dir()
    assert not base.exists()


def test_merge_folder_name_move_with_trailing_slash(tmp_path: Path):
    base = tmp_path / "with_slash"
    (base / "inner").mkdir(parents=True)
    result = merge_folder_name_move(str(base) + "/", "inner", need_del=False)
    assert Path(result).is_dir()
    # Parent should remain because need_del=False
    assert base.exists()


def test_merge_folder_name_move_failure(monkeypatch, tmp_path: Path):
    base = tmp_path / "broken"
    (base / "inner").mkdir(parents=True)

    def bad_rename(_src, _dst):
        raise OSError("fail")

    monkeypatch.setattr("dlsite_classification.tools.move.os.rename", bad_rename)
    assert merge_folder_name_move(str(base), "inner") == ""


def test_extract_folder_top_promotes_nested_structure(tmp_path: Path):
    root = tmp_path / "root"
    nested = root / "A" / "B"
    nested.mkdir(parents=True)
    (nested / "payload.txt").write_text("payload", encoding="utf-8")

    extract_folder_top(str(root))

    promoted = root / "AB"
    assert promoted.is_dir()
    assert (promoted / "payload.txt").read_text(encoding="utf-8") == "payload"
    assert not (root / "A").exists()


def test_extract_folder_top_no_action_when_files_present(tmp_path: Path):
    root = tmp_path / "root_with_file"
    root.mkdir()
    (root / "file.txt").write_text("data", encoding="utf-8")
    extract_folder_top(str(root))
    # Nothing should move because a file already lives at top level
    assert (root / "file.txt").exists()


def test_extract_folder_top_handles_failed_merge(monkeypatch, tmp_path: Path):
    root = tmp_path / "root_skip"
    (root / "A" / "B").mkdir(parents=True)

    monkeypatch.setattr(
        "dlsite_classification.tools.move.merge_folder_name_move",
        lambda _path, _name, _need_del=False: "",
    )

    extract_folder_top(str(root))
    # Original structure should remain because merge failed
    assert (root / "A" / "B").exists()
