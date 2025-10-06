"""
Tests for dlsite_classification.tools.check module

Testing folder creation and file checking utilities.
"""

import os
import pytest
from dlsite_classification.tools.check import (
    check_and_make_folder,
    check_folder_has_file
)


@pytest.mark.unit
class TestCheckAndMakeFolder:
    """Test check_and_make_folder function"""

    def test_creates_folder_if_not_exists(self, temp_dir):
        """Test that folder is created when it doesn't exist."""
        new_folder = os.path.join(temp_dir, "new_test_folder")
        assert not os.path.exists(new_folder)

        check_and_make_folder(new_folder)

        assert os.path.isdir(new_folder)

    def test_does_nothing_if_folder_exists(self, temp_dir):
        """Test that existing folder is not affected."""
        existing_folder = os.path.join(temp_dir, "existing")
        os.makedirs(existing_folder)

        # Create a test file to verify folder isn't recreated
        test_file = os.path.join(existing_folder, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        check_and_make_folder(existing_folder)

        # Folder and file should still exist
        assert os.path.isdir(existing_folder)
        assert os.path.isfile(test_file)

    def test_creates_nested_folders(self, temp_dir):
        """Test that nested folders are created."""
        nested_path = os.path.join(temp_dir, "level1", "level2", "level3")
        assert not os.path.exists(nested_path)

        check_and_make_folder(nested_path)

        assert os.path.isdir(nested_path)

    def test_handles_relative_paths(self, temp_dir):
        """Test that relative paths work correctly."""
        # Change to temp_dir
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            relative_path = "relative_folder"

            check_and_make_folder(relative_path)

            assert os.path.isdir(relative_path)
        finally:
            os.chdir(original_cwd)

    def test_handles_makedirs_exception(self, temp_dir, monkeypatch):
        """Errors from os.makedirs should be swallowed and not raise."""

        def boom(_path):
            raise OSError("boom")

        monkeypatch.setattr("os.makedirs", boom)

        target = os.path.join(temp_dir, "cannot_create")
        check_and_make_folder(target)
        assert not os.path.exists(target)


@pytest.mark.unit
class TestCheckFolderHasFile:
    """Test check_folder_has_file function"""

    def test_returns_true_when_folder_has_files(self, temp_dir):
        """Test returns True when folder contains files."""
        # Create a test file
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        has_file, dir_list = check_folder_has_file(temp_dir)

        assert has_file is True
        assert "test.txt" in dir_list

    def test_returns_false_when_folder_empty(self, temp_dir):
        """Test returns False when folder is empty."""
        empty_folder = os.path.join(temp_dir, "empty")
        os.makedirs(empty_folder)

        has_file, dir_list = check_folder_has_file(empty_folder)

        assert has_file is False
        assert dir_list == []

    def test_returns_false_when_folder_has_only_subdirs(self, temp_dir):
        """Test returns False when folder contains only subdirectories."""
        # Create only subdirectories
        subdir1 = os.path.join(temp_dir, "subdir1")
        subdir2 = os.path.join(temp_dir, "subdir2")
        os.makedirs(subdir1)
        os.makedirs(subdir2)

        has_file, dir_list = check_folder_has_file(temp_dir)

        assert has_file is False
        assert set(dir_list) == {"subdir1", "subdir2"}

    def test_returns_true_with_mixed_content(self, temp_dir):
        """Test returns True when folder has both files and directories."""
        # Create file and directory
        test_file = os.path.join(temp_dir, "file.txt")
        test_dir = os.path.join(temp_dir, "subdir")

        with open(test_file, "w") as f:
            f.write("test")
        os.makedirs(test_dir)

        has_file, dir_list = check_folder_has_file(temp_dir)

        assert has_file is True
        assert "file.txt" in dir_list
        assert "subdir" in dir_list

    def test_returns_correct_dir_list(self, temp_dir):
        """Test that dir_list contains all items in folder."""
        # Create multiple files and directories
        items = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"file{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"content{i}")
            items.append(f"file{i}.txt")

        for i in range(2):
            dir_path = os.path.join(temp_dir, f"dir{i}")
            os.makedirs(dir_path)
            items.append(f"dir{i}")

        has_file, dir_list = check_folder_has_file(temp_dir)

        assert has_file is True
        assert set(dir_list) == set(items)

    def test_detects_hidden_files(self, temp_dir):
        """Test that hidden files (starting with .) are detected."""
        hidden_file = os.path.join(temp_dir, ".hidden")
        with open(hidden_file, "w") as f:
            f.write("hidden content")

        has_file, dir_list = check_folder_has_file(temp_dir)

        assert has_file is True
        assert ".hidden" in dir_list
