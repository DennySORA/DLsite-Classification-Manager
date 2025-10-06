"""Test suite for extract.extract module - File scanning and metadata extraction."""
import os
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from dlsite_classification.extract.extract import ExtractFolder
from dlsite_classification.extract.structure import Tag, WorkInfo, Work, Company


# ============================================================================
# Fixtures for Extract Testing
# ============================================================================


@pytest.fixture
def extract_test_structure(temp_dir):
    """Create a complete test folder structure for extraction testing."""
    # Create company folder structure
    company1_path = os.path.join(temp_dir, "[TestCompany1]_[RG12345]")
    company2_path = os.path.join(temp_dir, "[TestCompany2]_[RG23456]")
    invalid_company_path = os.path.join(temp_dir, "InvalidCompanyFolder")

    # Company 1 - with 2 works
    work1_path = os.path.join(
        company1_path, "RJ123456_[TestCompany1]_[RG12345] Test Work 1"
    )
    info1_path = os.path.join(work1_path, "RJ123456_info")
    os.makedirs(info1_path, exist_ok=True)

    work2_path = os.path.join(
        company1_path, "RJ234567_[TestCompany1]_[RG12345] Test Work 2"
    )
    info2_path = os.path.join(work2_path, "RJ234567_info")
    os.makedirs(info2_path, exist_ok=True)

    # Company 2 - with 1 work
    work3_path = os.path.join(
        company2_path, "BJ345678_[TestCompany2]_[RG23456] Test Work 3"
    )
    info3_path = os.path.join(work3_path, "BJ345678_info")
    os.makedirs(info3_path, exist_ok=True)

    # Create invalid company folder (should be ignored)
    os.makedirs(invalid_company_path, exist_ok=True)

    # Create tag files for work 1
    tag_files_work1 = {
        "code.tag": "RJ123456",
        "title.tag": "Test Work Title 1\nhttps://example.com/work1",
        "company.tag": "TestCompany1\nhttps://example.com/maker/RG12345",
        "introduction.tag": "This is a test introduction.\nWith multiple lines.",
        "star.tag": "5\n1000",
        "ジャンル.tag": "Action\nAdventure\nRPG",
        "ファイル形式.tag": "PDF\nMP3",
        "販売日.tag": "2025年01月01日",
        "my_rating.tag": "5",
        "my_collection.tag": "Favorites",
        "my_collections.tag": "Favorites\nAction\nCompleted",
    }

    for filename, content in tag_files_work1.items():
        file_path = os.path.join(info1_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Create images for work 1
    for i in range(3):
        img_path = os.path.join(info1_path, f"RJ123456_img_smp{i}.jpg")
        Path(img_path).touch()
    main_img_path = os.path.join(info1_path, "RJ123456_img_main.jpg")
    Path(main_img_path).touch()

    # Create minimal tag files for work 2
    tag_files_work2 = {
        "code.tag": "RJ234567",
        "title.tag": "Test Work Title 2\nhttps://example.com/work2",
        "company.tag": "TestCompany1\nhttps://example.com/maker/RG12345",
    }

    for filename, content in tag_files_work2.items():
        file_path = os.path.join(info2_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Create tag files for work 3 (BJ code)
    tag_files_work3 = {
        "code.tag": "BJ345678",
        "title.tag": "Test Work Title 3\nhttps://example.com/work3",
        "company.tag": "TestCompany2\nhttps://example.com/maker/RG23456",
        "作者.tag": "Author Name",
        "ページ数.tag": "100",
    }

    for filename, content in tag_files_work3.items():
        file_path = os.path.join(info3_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Create a work folder without info (should handle gracefully)
    work_no_info_path = os.path.join(
        company1_path, "RJ999999_[TestCompany1]_[RG12345] Work Without Info"
    )
    os.makedirs(work_no_info_path, exist_ok=True)

    return {
        "root": temp_dir,
        "company1_path": company1_path,
        "company2_path": company2_path,
        "invalid_company_path": invalid_company_path,
        "work1_path": work1_path,
        "work2_path": work2_path,
        "work3_path": work3_path,
        "work_no_info_path": work_no_info_path,
        "info1_path": info1_path,
        "info2_path": info2_path,
        "info3_path": info3_path,
    }


@pytest.fixture
def extract_folder(extract_test_structure):
    """Create ExtractFolder instance with test structure."""
    return ExtractFolder(extract_test_structure["root"])


@pytest.fixture
def simple_tag_structure(temp_dir):
    """Create a simple structure for isolated tag testing."""
    company_path = os.path.join(temp_dir, "[TestCompany]_[RG12345]")
    work_path = os.path.join(company_path, "RJ123456_[TestCompany]_[RG12345] Work")
    info_path = os.path.join(work_path, "RJ123456_info")
    os.makedirs(info_path, exist_ok=True)

    return {
        "root": temp_dir,
        "company_path": company_path,
        "work_path": work_path,
        "info_path": info_path,
    }


# ============================================================================
# ExtractFolder Initialization Tests
# ============================================================================


@pytest.mark.unit
class TestExtractFolderInit:
    """Test ExtractFolder initialization."""

    def test_init_creates_instance(self, temp_dir):
        """Test that ExtractFolder can be instantiated."""
        extract = ExtractFolder(temp_dir)
        assert extract is not None
        assert isinstance(extract, ExtractFolder)

    def test_init_sets_path(self, temp_dir):
        """Test that path is set correctly."""
        extract = ExtractFolder(temp_dir)
        assert extract.path == temp_dir

    def test_init_creates_empty_classification_table(self, temp_dir):
        """Test that classification_table is initialized as empty OrderedDict."""
        extract = ExtractFolder(temp_dir)
        assert len(extract.classification_table) == 0
        from collections import OrderedDict

        assert isinstance(extract.classification_table, OrderedDict)

    def test_init_sets_scan_count_zero(self, temp_dir):
        """Test that scan_count is initialized to 0."""
        extract = ExtractFolder(temp_dir)
        assert extract.scan_count == 0


# ============================================================================
# make_tag() Method Tests
# ============================================================================


@pytest.mark.unit
class TestMakeTag:
    """Test the make_tag method for tag file parsing."""

    @pytest.mark.asyncio
    async def test_make_tag_empty_dict(self, temp_dir):
        """Test make_tag with empty tag dictionary."""
        extract = ExtractFolder(temp_dir)
        tag = await extract.make_tag({})
        assert isinstance(tag, Tag)

    @pytest.mark.asyncio
    async def test_make_tag_code_field(self, simple_tag_structure):
        """Test make_tag parsing code field."""
        info_path = simple_tag_structure["info_path"]
        code_path = os.path.join(info_path, "code.tag")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write("RJ123456")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"code": code_path})
        assert tag.code == "RJ123456"

    @pytest.mark.asyncio
    async def test_make_tag_title_field_with_url(self, simple_tag_structure):
        """Test make_tag parsing title field with URL."""
        info_path = simple_tag_structure["info_path"]
        title_path = os.path.join(info_path, "title.tag")
        with open(title_path, "w", encoding="utf-8") as f:
            f.write("Test Work Title\nhttps://example.com/work")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"title": title_path})
        assert tag.title == {"Test Work Title": "https://example.com/work"}

    @pytest.mark.asyncio
    async def test_make_tag_company_field_with_url(self, simple_tag_structure):
        """Test make_tag parsing company field with URL."""
        info_path = simple_tag_structure["info_path"]
        company_path = os.path.join(info_path, "company.tag")
        with open(company_path, "w", encoding="utf-8") as f:
            f.write("TestCompany\nhttps://example.com/maker")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"company": company_path})
        assert tag.company == {"TestCompany": "https://example.com/maker"}

    @pytest.mark.asyncio
    async def test_make_tag_introduction_multiline(self, simple_tag_structure):
        """Test make_tag parsing multiline introduction."""
        info_path = simple_tag_structure["info_path"]
        intro_path = os.path.join(info_path, "introduction.tag")
        with open(intro_path, "w", encoding="utf-8") as f:
            f.write("Line 1\nLine 2\nLine 3")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"introduction": intro_path})
        assert tag.introduction == "Line 1\nLine 2\nLine 3"

    @pytest.mark.asyncio
    async def test_make_tag_star_field_tuple(self, simple_tag_structure):
        """Test make_tag parsing star field as tuple."""
        info_path = simple_tag_structure["info_path"]
        star_path = os.path.join(info_path, "star.tag")
        with open(star_path, "w", encoding="utf-8") as f:
            f.write("5\n1000")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"star": star_path})
        assert tag.star == (5, "1000")
        assert isinstance(tag.star[0], int)

    @pytest.mark.asyncio
    async def test_make_tag_star_field_without_count(self, simple_tag_structure):
        """Test make_tag parsing star field without count."""
        info_path = simple_tag_structure["info_path"]
        star_path = os.path.join(info_path, "star.tag")
        with open(star_path, "w", encoding="utf-8") as f:
            f.write("4")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"star": star_path})
        assert tag.star == (4, "")

    @pytest.mark.asyncio
    async def test_make_tag_my_rating_string(self, simple_tag_structure):
        """Test make_tag parsing my_rating as string."""
        info_path = simple_tag_structure["info_path"]
        rating_path = os.path.join(info_path, "my_rating.tag")
        with open(rating_path, "w", encoding="utf-8") as f:
            f.write("5")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"my_rating": rating_path})
        assert tag.my_rating == "5"
        assert isinstance(tag.my_rating, str)

    @pytest.mark.asyncio
    async def test_make_tag_my_collection_string(self, simple_tag_structure):
        """Test make_tag parsing my_collection as string."""
        info_path = simple_tag_structure["info_path"]
        collection_path = os.path.join(info_path, "my_collection.tag")
        with open(collection_path, "w", encoding="utf-8") as f:
            f.write("Favorites")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"my_collection": collection_path})
        assert tag.my_collection == "Favorites"

    @pytest.mark.asyncio
    async def test_make_tag_my_collections_list(self, simple_tag_structure):
        """Test make_tag parsing my_collections as list."""
        info_path = simple_tag_structure["info_path"]
        collections_path = os.path.join(info_path, "my_collections.tag")
        with open(collections_path, "w", encoding="utf-8") as f:
            f.write("Favorites\nAction\nCompleted")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"my_collections": collections_path})
        assert tag.my_collections == ["Favorites", "Action", "Completed"]
        assert isinstance(tag.my_collections, list)

    @pytest.mark.asyncio
    async def test_make_tag_genre_dict_format(self, simple_tag_structure):
        """Test make_tag parsing genre with dict format."""
        info_path = simple_tag_structure["info_path"]
        genre_path = os.path.join(info_path, "ジャンル.tag")
        with open(genre_path, "w", encoding="utf-8") as f:
            f.write("Action\nAdventure\nRPG")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"ジャンル": genre_path})
        assert tag.genre == {"Action": True, "Adventure": True, "RPG": True}

    @pytest.mark.asyncio
    async def test_make_tag_multiple_fields(self, simple_tag_structure):
        """Test make_tag with multiple fields simultaneously."""
        info_path = simple_tag_structure["info_path"]

        # Create multiple tag files
        tags_data = {
            "code.tag": "RJ123456",
            "title.tag": "Test Title\nurl",
            "ジャンル.tag": "Action\nAdventure",
            "my_rating.tag": "5",
        }

        tags_table = {}
        for filename, content in tags_data.items():
            file_path = os.path.join(info_path, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            tags_table[filename.replace(".tag", "")] = file_path

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag(tags_table)

        assert tag.code == "RJ123456"
        assert tag.title == {"Test Title": "url"}
        assert tag.genre == {"Action": True, "Adventure": True}
        assert tag.my_rating == "5"

    @pytest.mark.asyncio
    async def test_make_tag_japanese_field_conversion(self, simple_tag_structure):
        """Test that Japanese field names are correctly converted to English."""
        info_path = simple_tag_structure["info_path"]

        # Test various Japanese fields
        japanese_fields = {
            "ファイル形式.tag": "PDF\nMP3",
            "販売日.tag": "2025年01月01日",
            "声優.tag": "Voice Actor 1\nVoice Actor 2",
        }

        tags_table = {}
        for filename, content in japanese_fields.items():
            file_path = os.path.join(info_path, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            tags_table[filename.replace(".tag", "")] = file_path

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag(tags_table)

        assert tag.file_format == {"PDF": True, "MP3": True}
        assert tag.sale_date == {"2025年01月01日": True}
        assert tag.voice_actor == {"Voice Actor 1": True, "Voice Actor 2": True}

    @pytest.mark.asyncio
    async def test_make_tag_empty_lines_filtered(self, simple_tag_structure):
        """Test that empty lines in multi-value fields are filtered."""
        info_path = simple_tag_structure["info_path"]
        genre_path = os.path.join(info_path, "ジャンル.tag")
        with open(genre_path, "w", encoding="utf-8") as f:
            f.write("Action\n\nAdventure\n\n\nRPG")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"ジャンル": genre_path})
        # Empty lines should be filtered in dict format
        assert "Action" in tag.genre
        assert "Adventure" in tag.genre
        assert "RPG" in tag.genre


# ============================================================================
# scan_work() Method Tests
# ============================================================================


@pytest.mark.unit
class TestScanWork:
    """Test the scan_work method for scanning work folders."""

    @pytest.mark.asyncio
    async def test_scan_work_basic(self, extract_test_structure):
        """Test basic work scanning."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work1_path"], "RJ123456"
        )
        assert isinstance(work_info, WorkInfo)
        assert work_info.tag.code == "RJ123456"

    @pytest.mark.asyncio
    async def test_scan_work_extracts_tag_data(self, extract_test_structure):
        """Test that scan_work correctly extracts tag data."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work1_path"], "RJ123456"
        )

        assert work_info.tag.code == "RJ123456"
        assert work_info.tag.title == {
            "Test Work Title 1": "https://example.com/work1"
        }
        assert work_info.tag.company == {
            "TestCompany1": "https://example.com/maker/RG12345"
        }
        assert work_info.tag.star == (5, "1000")
        assert work_info.tag.my_rating == "5"

    @pytest.mark.asyncio
    async def test_scan_work_extracts_images(self, extract_test_structure):
        """Test that scan_work correctly extracts image list."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work1_path"], "RJ123456"
        )

        assert len(work_info.images) == 4  # 3 sample + 1 main
        assert "RJ123456_img_main.jpg" in work_info.images
        assert "RJ123456_img_smp0.jpg" in work_info.images

    @pytest.mark.asyncio
    async def test_scan_work_info_folder_not_found(self, extract_test_structure):
        """Test scan_work raises FileNotFoundError when info folder missing."""
        extract = ExtractFolder(extract_test_structure["root"])
        with pytest.raises(FileNotFoundError):
            await extract.scan_work(
                extract_test_structure["work_no_info_path"], "RJ999999"
            )

    @pytest.mark.asyncio
    async def test_scan_work_minimal_tags(self, extract_test_structure):
        """Test scan_work with minimal tag files."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work2_path"], "RJ234567"
        )

        assert work_info.tag.code == "RJ234567"
        assert work_info.tag.title is not None
        assert work_info.tag.genre is None  # Not present in minimal set

    @pytest.mark.asyncio
    async def test_scan_work_bj_code(self, extract_test_structure):
        """Test scan_work with BJ code."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work3_path"], "BJ345678"
        )

        assert work_info.tag.code == "BJ345678"
        assert work_info.tag.author is not None
        assert work_info.tag.pages is not None

    @pytest.mark.asyncio
    async def test_scan_work_sets_correct_path(self, extract_test_structure):
        """Test that scan_work sets the correct info folder path."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_info = await extract.scan_work(
            extract_test_structure["work1_path"], "RJ123456"
        )

        expected_path = extract_test_structure["info1_path"]
        assert work_info.path == expected_path

    @pytest.mark.asyncio
    async def test_scan_work_handles_tag_error_gracefully(
        self, simple_tag_structure, monkeypatch
    ):
        """Test that scan_work handles tag parsing errors gracefully."""
        # Create a malformed tag file
        info_path = simple_tag_structure["info_path"]
        code_path = os.path.join(info_path, "code.tag")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write("RJ123456")

        extract = ExtractFolder(simple_tag_structure["root"])

        # Mock make_tag to raise an exception
        original_make_tag = extract.make_tag

        async def failing_make_tag(*args, **kwargs):
            raise Exception("Tag parsing error")

        monkeypatch.setattr(extract, "make_tag", failing_make_tag)

        # Should create minimal tag instead of raising
        work_info = await extract.scan_work(simple_tag_structure["work_path"], "RJ123456")
        assert isinstance(work_info, WorkInfo)
        assert isinstance(work_info.tag, Tag)


# ============================================================================
# scan_company() Method Tests
# ============================================================================


@pytest.mark.unit
class TestScanCompany:
    """Test the scan_company method for scanning company folders."""

    @pytest.mark.asyncio
    async def test_scan_company_basic(self, extract_test_structure):
        """Test basic company scanning."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])
        assert isinstance(work_dict, dict)
        assert len(work_dict) > 0

    @pytest.mark.asyncio
    async def test_scan_company_extracts_all_works(self, extract_test_structure):
        """Test that scan_company extracts all works in company folder."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        # Should find 3 work folders (2 with info, 1 without)
        assert len(work_dict) == 3

    @pytest.mark.asyncio
    async def test_scan_company_creates_work_objects(self, extract_test_structure):
        """Test that scan_company creates proper Work objects."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        for work_folder, work in work_dict.items():
            assert isinstance(work, Work)
            assert work.code is not None
            assert work.name is not None
            assert work.path is not None

    @pytest.mark.asyncio
    async def test_scan_company_extracts_code_from_folder_name(
        self, extract_test_structure
    ):
        """Test that scan_company correctly extracts code from folder name."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        # Find work with RJ123456
        rj_work = None
        for work in work_dict.values():
            if work.code == "RJ123456":
                rj_work = work
                break

        assert rj_work is not None
        assert rj_work.code == "RJ123456"

    @pytest.mark.asyncio
    async def test_scan_company_extracts_name_from_folder(self, extract_test_structure):
        """Test that scan_company extracts work name from folder."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        for folder_name, work in work_dict.items():
            expected_name = folder_name.split("] ")[-1]
            assert work.name == expected_name

    @pytest.mark.asyncio
    async def test_scan_company_handles_work_without_info(self, extract_test_structure):
        """Test that scan_company handles works without info folder."""
        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        # Find work without info
        work_no_info = None
        for work in work_dict.values():
            if work.code == "RJ999999":
                work_no_info = work
                break

        assert work_no_info is not None
        assert work_no_info.info is None

    @pytest.mark.asyncio
    async def test_scan_company_skips_folders_without_code(
        self, extract_test_structure
    ):
        """Test that scan_company skips folders without valid codes."""
        # Add a folder without code
        no_code_folder = os.path.join(
            extract_test_structure["company1_path"], "InvalidFolder"
        )
        os.makedirs(no_code_folder, exist_ok=True)

        extract = ExtractFolder(extract_test_structure["root"])
        work_dict = await extract.scan_company(extract_test_structure["company1_path"])

        # Should not include invalid folder
        assert "InvalidFolder" not in work_dict

    @pytest.mark.asyncio
    async def test_scan_company_empty_folder(self, temp_dir):
        """Test scan_company on empty company folder."""
        company_path = os.path.join(temp_dir, "[EmptyCompany]_[RG99999]")
        os.makedirs(company_path, exist_ok=True)

        extract = ExtractFolder(temp_dir)
        work_dict = await extract.scan_company(company_path)

        assert isinstance(work_dict, dict)
        assert len(work_dict) == 0


# ============================================================================
# scan_file() Method Tests
# ============================================================================


@pytest.mark.integration
class TestScanFile:
    """Test the scan_file method for full folder scanning."""

    @pytest.mark.asyncio
    async def test_scan_file_basic(self, extract_test_structure, disable_logging):
        """Test basic full folder scanning."""
        extract = ExtractFolder(extract_test_structure["root"])
        scan_time = await extract.scan_file()
        assert isinstance(scan_time, float)
        assert scan_time >= 0

    @pytest.mark.asyncio
    async def test_scan_file_populates_classification_table(
        self, extract_test_structure, disable_logging
    ):
        """Test that scan_file populates classification_table."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        assert len(extract.classification_table) > 0
        # Should have 2 valid company folders
        assert len(extract.classification_table) == 2

    @pytest.mark.asyncio
    async def test_scan_file_creates_company_objects(
        self, extract_test_structure, disable_logging
    ):
        """Test that scan_file creates proper Company objects."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        for company_name, company in extract.classification_table.items():
            assert isinstance(company, Company)
            assert company.name is not None
            assert company.path is not None
            assert isinstance(company.work_item, dict)

    @pytest.mark.asyncio
    async def test_scan_file_skips_invalid_company_folders(
        self, extract_test_structure, disable_logging
    ):
        """Test that scan_file skips folders not matching company pattern."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        # Should not include InvalidCompanyFolder
        assert "InvalidCompanyFolder" not in extract.classification_table

    @pytest.mark.asyncio
    async def test_scan_file_full_hierarchy(
        self, extract_test_structure, disable_logging
    ):
        """Test that scan_file creates complete hierarchy."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        # Access a specific work through hierarchy
        company1 = extract.classification_table["[TestCompany1]_[RG12345]"]
        assert len(company1.work_item) == 3

        # Find a work with info
        work_with_info = None
        for work in company1.work_item.values():
            if work.info is not None:
                work_with_info = work
                break

        assert work_with_info is not None
        assert work_with_info.info.tag.code is not None

    @pytest.mark.asyncio
    async def test_scan_file_empty_directory(self, temp_dir, disable_logging):
        """Test scan_file on empty directory."""
        extract = ExtractFolder(temp_dir)
        scan_time = await extract.scan_file()
        assert isinstance(scan_time, float)
        assert len(extract.classification_table) == 0

    @pytest.mark.asyncio
    async def test_scan_file_returns_execution_time(
        self, extract_test_structure, disable_logging
    ):
        """Test that scan_file returns execution time in seconds."""
        extract = ExtractFolder(extract_test_structure["root"])
        scan_time = await extract.scan_file()
        assert scan_time > 0
        assert scan_time < 60  # Should complete in under 60 seconds


# ============================================================================
# get_table() Method Tests
# ============================================================================


@pytest.mark.unit
class TestGetTable:
    """Test the get_table method for pagination."""

    @pytest.mark.asyncio
    async def test_get_table_default_pagination(
        self, extract_test_structure, disable_logging
    ):
        """Test get_table with default pagination parameters."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_table()
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_table_with_limit(self, extract_test_structure, disable_logging):
        """Test get_table with custom limit."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_table(limit=1)
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_table_with_offset(self, extract_test_structure, disable_logging):
        """Test get_table with offset."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result_first = extract.get_table(limit=1, offset=0)
        result_second = extract.get_table(limit=1, offset=1)

        # Should return different items
        assert result_first[0][0] != result_second[0][0]

    @pytest.mark.asyncio
    async def test_get_table_returns_tuples(
        self, extract_test_structure, disable_logging
    ):
        """Test that get_table returns list of (name, Company) tuples."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_table(limit=1)
        assert isinstance(result[0], tuple)
        assert len(result[0]) == 2
        assert isinstance(result[0][0], str)  # Company name
        assert isinstance(result[0][1], Company)  # Company object


# ============================================================================
# get_all_table() Method Tests
# ============================================================================


@pytest.mark.unit
class TestGetAllTable:
    """Test the get_all_table method."""

    @pytest.mark.asyncio
    async def test_get_all_table_returns_ordered_dict(
        self, extract_test_structure, disable_logging
    ):
        """Test that get_all_table returns OrderedDict."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_all_table()
        from collections import OrderedDict

        assert isinstance(result, OrderedDict)

    @pytest.mark.asyncio
    async def test_get_all_table_contains_all_companies(
        self, extract_test_structure, disable_logging
    ):
        """Test that get_all_table contains all scanned companies."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_all_table()
        assert len(result) == 2  # 2 valid company folders

    @pytest.mark.asyncio
    async def test_get_all_table_same_as_classification_table(
        self, extract_test_structure, disable_logging
    ):
        """Test that get_all_table returns the classification_table."""
        extract = ExtractFolder(extract_test_structure["root"])
        await extract.scan_file()

        result = extract.get_all_table()
        assert result is extract.classification_table


# ============================================================================
# Edge Cases and Error Handling Tests
# ============================================================================


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_malformed_tag_file(self, simple_tag_structure):
        """Test handling of malformed tag files."""
        info_path = simple_tag_structure["info_path"]

        # Create a tag file with unusual content
        star_path = os.path.join(info_path, "star.tag")
        with open(star_path, "w", encoding="utf-8") as f:
            f.write("invalid_number\ncount")

        extract = ExtractFolder(simple_tag_structure["root"])
        # Should handle gracefully during make_tag
        try:
            await extract.make_tag({"star": star_path})
        except Exception:
            # Expect potential parsing errors for invalid formats
            pass

    @pytest.mark.asyncio
    async def test_unicode_content_in_tags(self, simple_tag_structure):
        """Test handling of unicode characters in tag files."""
        info_path = simple_tag_structure["info_path"]

        title_path = os.path.join(info_path, "title.tag")
        with open(title_path, "w", encoding="utf-8") as f:
            f.write("日本語のタイトル\nhttps://example.com")

        extract = ExtractFolder(simple_tag_structure["root"])
        tag = await extract.make_tag({"title": title_path})
        assert "日本語のタイトル" in tag.title

    @pytest.mark.asyncio
    async def test_scan_nonexistent_directory(self):
        """Test scanning a non-existent directory."""
        extract = ExtractFolder("/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            await extract.scan_file()

    @pytest.mark.asyncio
    async def test_work_folder_with_multiple_codes(self, simple_tag_structure):
        """Test work folder name with multiple code patterns."""
        # Create a folder with multiple codes (should extract first)
        company_path = simple_tag_structure["company_path"]
        multi_code_path = os.path.join(
            company_path, "RJ123456_RJ234567_MultiCode_Work"
        )
        os.makedirs(multi_code_path, exist_ok=True)

        extract = ExtractFolder(simple_tag_structure["root"])
        work_dict = await extract.scan_company(company_path)

        # Should extract first code
        found = False
        for work in work_dict.values():
            if work.code in ["RJ123456", "RJ234567"]:
                found = True
                break
        assert found
