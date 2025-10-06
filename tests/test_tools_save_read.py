"""
Tests for dlsite_classification.tools.save_read module

Testing async file I/O operations.
"""

import os
import pytest
from dlsite_classification.tools.save_read import save_data, raed_data


@pytest.mark.unit
@pytest.mark.asyncio
class TestSaveData:
    """Test save_data function"""

    async def test_saves_string_data(self, temp_dir):
        """Test saving string data to file."""
        file_path = os.path.join(temp_dir, "test.txt")
        test_data = "Hello, World!"

        await save_data(file_path, test_data)

        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_data

    async def test_saves_unicode_data(self, temp_dir):
        """Test saving Unicode data (Japanese, Chinese, etc.)."""
        file_path = os.path.join(temp_dir, "unicode.txt")
        test_data = "日本語テスト 中文測試 한국어"

        await save_data(file_path, test_data)

        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_data

    async def test_saves_empty_string(self, temp_dir):
        """Test saving empty string."""
        file_path = os.path.join(temp_dir, "empty.txt")
        test_data = ""

        await save_data(file_path, test_data)

        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_data

    async def test_saves_multiline_data(self, temp_dir):
        """Test saving multiline text."""
        file_path = os.path.join(temp_dir, "multiline.txt")
        test_data = "Line 1\nLine 2\nLine 3\n"

        await save_data(file_path, test_data)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_data

    async def test_overwrites_existing_file(self, temp_dir):
        """Test that save_data overwrites existing files."""
        file_path = os.path.join(temp_dir, "overwrite.txt")

        # Write initial data
        await save_data(file_path, "initial content")

        # Overwrite with new data
        new_data = "new content"
        await save_data(file_path, new_data)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == new_data

    async def test_creates_file_in_existing_directory(self, temp_dir):
        """Test creating file in an existing directory."""
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        file_path = os.path.join(subdir, "test.txt")

        await save_data(file_path, "test content")

        assert os.path.exists(file_path)


@pytest.mark.unit
@pytest.mark.asyncio
class TestRaedData:
    """Test raed_data function (note: function name has typo 'raed')"""

    async def test_reads_string_data(self, temp_dir):
        """Test reading string data from file."""
        file_path = os.path.join(temp_dir, "test.txt")
        test_data = "Hello, World!"

        # Create file first
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_data)

        result = await raed_data(file_path)

        assert result == test_data

    async def test_reads_unicode_data(self, temp_dir):
        """Test reading Unicode data."""
        file_path = os.path.join(temp_dir, "unicode.txt")
        test_data = "日本語テスト 中文測試 한국어"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_data)

        result = await raed_data(file_path)

        assert result == test_data

    async def test_reads_empty_file(self, temp_dir):
        """Test reading empty file."""
        file_path = os.path.join(temp_dir, "empty.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

        result = await raed_data(file_path)

        assert result == ""

    async def test_reads_multiline_data(self, temp_dir):
        """Test reading multiline text."""
        file_path = os.path.join(temp_dir, "multiline.txt")
        test_data = "Line 1\nLine 2\nLine 3\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_data)

        result = await raed_data(file_path)

        assert result == test_data

    async def test_reads_special_characters(self, temp_dir):
        """Test reading file with special characters."""
        file_path = os.path.join(temp_dir, "special.txt")
        test_data = "Special: !@#$%^&*()[]{}|<>?~`"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_data)

        result = await raed_data(file_path)

        assert result == test_data

    async def test_returns_string_type(self, temp_dir):
        """Test that return value is string type."""
        file_path = os.path.join(temp_dir, "test.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("test")

        result = await raed_data(file_path)

        assert isinstance(result, str)


@pytest.mark.unit
@pytest.mark.asyncio
class TestSaveReadRoundtrip:
    """Test save and read operations together"""

    async def test_roundtrip_preserves_data(self, temp_dir):
        """Test that data saved and read back is identical."""
        file_path = os.path.join(temp_dir, "roundtrip.txt")
        original_data = "Test data with 日本語 and symbols: !@#$"

        await save_data(file_path, original_data)
        read_data = await raed_data(file_path)

        assert read_data == original_data

    async def test_multiple_roundtrips(self, temp_dir):
        """Test multiple save/read cycles."""
        file_path = os.path.join(temp_dir, "multi_roundtrip.txt")

        for i in range(5):
            test_data = f"Iteration {i}: Some content"
            await save_data(file_path, test_data)
            read_data = await raed_data(file_path)
            assert read_data == test_data

    async def test_concurrent_operations(self, temp_dir):
        """Test multiple concurrent save/read operations."""
        import asyncio

        async def save_and_read(index):
            file_path = os.path.join(temp_dir, f"concurrent_{index}.txt")
            data = f"Data {index}"
            await save_data(file_path, data)
            result = await raed_data(file_path)
            return result == data

        # Run 10 concurrent operations
        results = await asyncio.gather(*[save_and_read(i) for i in range(10)])

        assert all(results)
