"""Test suite for extract.structure module - Pydantic models and conversion table."""
import pytest
from pydantic import ValidationError

from dlsite_classification.extract.structure import (
    Company,
    Tag,
    Work,
    WorkInfo,
    conversion_table,
)


# ============================================================================
# Conversion Table Tests
# ============================================================================


@pytest.mark.unit
class TestConversionTable:
    """Test the conversion_table mapping from Japanese to English field names."""

    def test_conversion_table_exists(self):
        """Test that conversion_table is defined and not empty."""
        assert conversion_table is not None
        assert len(conversion_table) > 0

    def test_basic_fields_mapping(self):
        """Test that basic fields are correctly mapped."""
        expected_mappings = {
            "code": "code",
            "title": "title",
            "company": "company",
            "star": "star",
            "introduction": "introduction",
        }
        for japanese, english in expected_mappings.items():
            assert conversion_table[japanese] == english

    def test_japanese_metadata_fields_mapping(self):
        """Test that Japanese metadata fields are correctly mapped to English."""
        expected_mappings = {
            "シリーズ名": "series",
            "ジャンル": "genre",
            "ファイル容量": "file_capacity",
            "ファイル形式": "file_format",
            "作品形式": "work_format",
            "声優": "voice_actor",
            "年齢指定": "age",
            "販売日": "sale_date",
            "更新情報": "update_date",
            "動作環境": "operating_environment",
            "イラスト": "illustration",
            "シナリオ": "scenario",
            "作者": "author",
            "ページ数": "pages",
            "イベント": "event",
            "音楽": "music",
            "その他": "other",
            "対応言語": "languages",
        }
        for japanese, english in expected_mappings.items():
            assert conversion_table[japanese] == english

    def test_user_custom_fields_mapping(self):
        """Test that user custom fields are correctly mapped."""
        assert conversion_table["my_rating"] == "my_rating"
        assert conversion_table["my_collection"] == "my_collection"
        assert conversion_table["my_collections"] == "my_collections"

    def test_no_duplicate_values(self):
        """Test that all English field names are unique."""
        english_values = list(conversion_table.values())
        assert len(english_values) == len(set(english_values))

    def test_all_required_fields_present(self):
        """Test that all required fields are present in conversion table."""
        required_fields = [
            "code",
            "title",
            "company",
            "star",
            "introduction",
            "series",
            "genre",
            "file_format",
            "work_format",
            "voice_actor",
            "age",
            "sale_date",
            "my_rating",
            "my_collection",
        ]
        for field in required_fields:
            assert field in conversion_table.values()


# ============================================================================
# Tag Model Tests
# ============================================================================


@pytest.mark.unit
class TestTagModel:
    """Test the Tag Pydantic model."""

    def test_tag_creation_empty(self):
        """Test creating an empty Tag with all fields None."""
        tag = Tag()
        assert tag.code is None
        assert tag.star is None
        assert tag.title is None
        assert tag.company is None
        assert tag.introduction is None

    def test_tag_creation_with_basic_fields(self):
        """Test creating a Tag with basic string fields."""
        tag = Tag(
            code="RJ123456",
            introduction="Test introduction text",
        )
        assert tag.code == "RJ123456"
        assert tag.introduction == "Test introduction text"

    def test_tag_star_field_tuple(self):
        """Test that star field accepts tuple of (int, str)."""
        tag = Tag(star=(5, "1000"))
        assert tag.star == (5, "1000")
        assert isinstance(tag.star[0], int)
        assert isinstance(tag.star[1], str)

    def test_tag_star_field_empty_count(self):
        """Test that star field accepts empty count string."""
        tag = Tag(star=(4, ""))
        assert tag.star == (4, "")

    def test_tag_title_and_company_dict_format(self):
        """Test that title and company use dict format {value: url}."""
        tag = Tag(
            title={"Test Work Title": "https://example.com/work/RJ123456"},
            company={"TestCompany": "https://example.com/maker/RG12345.html"},
        )
        assert tag.title == {"Test Work Title": "https://example.com/work/RJ123456"}
        assert tag.company == {"TestCompany": "https://example.com/maker/RG12345.html"}

    def test_tag_metadata_dict_format(self):
        """Test that metadata fields use dict format {value: True}."""
        tag = Tag(
            genre={"Action": True, "Adventure": True},
            voice_actor={"Voice Actor 1": True, "Voice Actor 2": True},
            file_format={"PDF": True, "MP3": True},
        )
        assert tag.genre == {"Action": True, "Adventure": True}
        assert tag.voice_actor == {"Voice Actor 1": True, "Voice Actor 2": True}
        assert tag.file_format == {"PDF": True, "MP3": True}

    def test_tag_user_rating_string(self):
        """Test that my_rating is stored as string."""
        tag = Tag(my_rating="5")
        assert tag.my_rating == "5"
        assert isinstance(tag.my_rating, str)

    def test_tag_user_collection_string(self):
        """Test that my_collection is stored as string."""
        tag = Tag(my_collection="Favorites")
        assert tag.my_collection == "Favorites"
        assert isinstance(tag.my_collection, str)

    def test_tag_user_collections_list(self):
        """Test that my_collections is stored as list."""
        tag = Tag(my_collections=["Favorites", "Action", "Completed"])
        assert tag.my_collections == ["Favorites", "Action", "Completed"]
        assert isinstance(tag.my_collections, list)

    def test_tag_all_metadata_fields_present(self):
        """Test that all metadata fields can be set."""
        tag = Tag(
            series={"Series Name": True},
            genre={"Genre": True},
            file_capacity={"1.2GB": True},
            file_format={"PDF": True},
            work_format={"Manga": True},
            voice_actor={"Actor": True},
            age={"18+": True},
            sale_date={"2025-01-01": True},
            update_date={"2025-01-15": True},
            operating_environment={"Windows": True},
            illustration={"Artist": True},
            scenario={"Writer": True},
            author={"Author": True},
            pages={"100": True},
            event={"Event": True},
            music={"Composer": True},
            other={"Extra": True},
            languages={"Japanese": True, "English": True},
        )
        assert tag.series is not None
        assert tag.genre is not None
        assert tag.languages is not None

    def test_tag_optional_fields_default_none(self):
        """Test that all fields default to None when not provided."""
        tag = Tag(code="RJ123456")
        assert tag.code == "RJ123456"
        assert tag.star is None
        assert tag.series is None
        assert tag.genre is None
        assert tag.my_rating is None

    def test_tag_request_failed_field(self):
        """Test the request_failed field for error tracking."""
        tag = Tag(request_failed="Network timeout")
        assert tag.request_failed == "Network timeout"

    def test_tag_serialization(self):
        """Test that Tag can be serialized to dict."""
        tag = Tag(
            code="RJ123456",
            title={"Test Title": "url"},
            star=(5, "100"),
            my_rating="4",
        )
        tag_dict = tag.model_dump()
        assert tag_dict["code"] == "RJ123456"
        assert tag_dict["title"] == {"Test Title": "url"}
        assert tag_dict["star"] == (5, "100")
        assert tag_dict["my_rating"] == "4"

    def test_tag_deserialization(self):
        """Test that Tag can be deserialized from dict."""
        data = {
            "code": "RJ123456",
            "title": {"Test Title": "url"},
            "star": (5, "100"),
            "my_rating": "4",
        }
        tag = Tag(**data)
        assert tag.code == "RJ123456"
        assert tag.title == {"Test Title": "url"}
        assert tag.star == (5, "100")

    def test_tag_with_multiline_introduction(self):
        """Test that introduction can handle multiline text."""
        intro = "Line 1\nLine 2\nLine 3"
        tag = Tag(introduction=intro)
        assert tag.introduction == intro
        assert "\n" in tag.introduction


# ============================================================================
# WorkInfo Model Tests
# ============================================================================


@pytest.mark.unit
class TestWorkInfoModel:
    """Test the WorkInfo Pydantic model."""

    def test_workinfo_creation_minimal(self):
        """Test creating WorkInfo with minimal required fields."""
        tag = Tag(code="RJ123456")
        work_info = WorkInfo(path="/test/path", tag=tag, images=[])
        assert work_info.path == "/test/path"
        assert work_info.tag.code == "RJ123456"
        assert work_info.images == []

    def test_workinfo_creation_with_images(self):
        """Test creating WorkInfo with image list."""
        tag = Tag(code="RJ123456")
        images = [
            "RJ123456_img_main.jpg",
            "RJ123456_img_smp0.jpg",
            "RJ123456_img_smp1.jpg",
        ]
        work_info = WorkInfo(path="/test/path", tag=tag, images=images)
        assert len(work_info.images) == 3
        assert "RJ123456_img_main.jpg" in work_info.images

    def test_workinfo_creation_with_full_tag(self):
        """Test creating WorkInfo with a fully populated Tag."""
        tag = Tag(
            code="RJ123456",
            title={"Test Work": "url"},
            company={"TestCompany": "url"},
            star=(5, "1000"),
            genre={"Action": True},
            my_rating="5",
        )
        work_info = WorkInfo(
            path="/company/work/RJ123456_info", tag=tag, images=["main.jpg"]
        )
        assert work_info.tag.code == "RJ123456"
        assert work_info.tag.star == (5, "1000")
        assert work_info.tag.my_rating == "5"

    def test_workinfo_path_absolute(self):
        """Test that path can be absolute."""
        tag = Tag()
        work_info = WorkInfo(
            path="/home/user/data/company/work/info", tag=tag, images=[]
        )
        assert work_info.path.startswith("/")

    def test_workinfo_images_empty_list(self):
        """Test that images can be empty list."""
        tag = Tag()
        work_info = WorkInfo(path="/test", tag=tag, images=[])
        assert work_info.images == []
        assert isinstance(work_info.images, list)

    def test_workinfo_serialization(self):
        """Test WorkInfo serialization to dict."""
        tag = Tag(code="RJ123456", my_rating="4")
        work_info = WorkInfo(path="/test", tag=tag, images=["img.jpg"])
        data = work_info.model_dump()
        assert data["path"] == "/test"
        assert data["tag"]["code"] == "RJ123456"
        assert data["images"] == ["img.jpg"]

    def test_workinfo_missing_required_fields(self):
        """Test that WorkInfo requires path, tag, and images."""
        with pytest.raises(ValidationError):
            WorkInfo()


# ============================================================================
# Work Model Tests
# ============================================================================


@pytest.mark.unit
class TestWorkModel:
    """Test the Work Pydantic model."""

    def test_work_creation_minimal(self):
        """Test creating Work with minimal required fields."""
        work = Work(path="/test/path", code="RJ123456", name="Test Work")
        assert work.path == "/test/path"
        assert work.code == "RJ123456"
        assert work.name == "Test Work"
        assert work.info is None

    def test_work_creation_with_info(self):
        """Test creating Work with WorkInfo."""
        tag = Tag(code="RJ123456")
        work_info = WorkInfo(path="/test/info", tag=tag, images=[])
        work = Work(path="/test/path", code="RJ123456", name="Test Work", info=work_info)
        assert work.info is not None
        assert work.info.tag.code == "RJ123456"

    def test_work_code_formats(self):
        """Test Work with different code formats."""
        codes = ["RJ123456", "BJ123456", "VJ123456", "RE123456", "BE123456", "VE123456"]
        for code in codes:
            work = Work(path="/test", code=code, name="Test")
            assert work.code == code

    def test_work_name_extraction(self):
        """Test that work name can be extracted from folder name."""
        work = Work(
            path="/company/RJ123456_[Company]_[RG12345] Work Title",
            code="RJ123456",
            name="Work Title",
        )
        assert work.name == "Work Title"

    def test_work_without_info(self):
        """Test Work without info (not yet scanned)."""
        work = Work(path="/test", code="RJ123456", name="Test")
        assert work.info is None

    def test_work_serialization(self):
        """Test Work serialization to dict."""
        work = Work(path="/test", code="RJ123456", name="Test Work")
        data = work.model_dump()
        assert data["path"] == "/test"
        assert data["code"] == "RJ123456"
        assert data["name"] == "Test Work"
        assert data["info"] is None

    def test_work_with_full_info_serialization(self):
        """Test Work with full info serialization."""
        tag = Tag(code="RJ123456", title={"Test": "url"})
        work_info = WorkInfo(path="/info", tag=tag, images=["img.jpg"])
        work = Work(path="/test", code="RJ123456", name="Test", info=work_info)
        data = work.model_dump()
        assert data["info"]["tag"]["code"] == "RJ123456"
        assert data["info"]["images"] == ["img.jpg"]

    def test_work_missing_required_fields(self):
        """Test that Work requires path, code, and name."""
        with pytest.raises(ValidationError):
            Work()
        with pytest.raises(ValidationError):
            Work(path="/test")
        with pytest.raises(ValidationError):
            Work(path="/test", code="RJ123456")


# ============================================================================
# Company Model Tests
# ============================================================================


@pytest.mark.unit
class TestCompanyModel:
    """Test the Company Pydantic model."""

    def test_company_creation_empty_works(self):
        """Test creating Company with empty work_item dict."""
        company = Company(path="/test/path", name="TestCompany", work_item={})
        assert company.path == "/test/path"
        assert company.name == "TestCompany"
        assert company.work_item == {}

    def test_company_creation_with_works(self):
        """Test creating Company with works."""
        work1 = Work(path="/work1", code="RJ123456", name="Work 1")
        work2 = Work(path="/work2", code="RJ234567", name="Work 2")
        work_item = {"RJ123456": work1, "RJ234567": work2}
        company = Company(path="/test", name="TestCompany", work_item=work_item)
        assert len(company.work_item) == 2
        assert "RJ123456" in company.work_item
        assert company.work_item["RJ123456"].name == "Work 1"

    def test_company_name_format(self):
        """Test company name in folder format."""
        company = Company(
            path="/data/[TestCompany]_[RG12345]",
            name="[TestCompany]_[RG12345]",
            work_item={},
        )
        assert "[TestCompany]" in company.name
        assert "[RG12345]" in company.name

    def test_company_work_item_dict_type(self):
        """Test that work_item is a dict with string keys and Work values."""
        work = Work(path="/test", code="RJ123456", name="Test")
        company = Company(path="/test", name="Company", work_item={"work1": work})
        assert isinstance(company.work_item, dict)
        assert isinstance(company.work_item["work1"], Work)

    def test_company_serialization(self):
        """Test Company serialization to dict."""
        work = Work(path="/work", code="RJ123456", name="Work")
        company = Company(path="/test", name="Company", work_item={"w1": work})
        data = company.model_dump()
        assert data["path"] == "/test"
        assert data["name"] == "Company"
        assert "w1" in data["work_item"]
        assert data["work_item"]["w1"]["code"] == "RJ123456"

    def test_company_missing_required_fields(self):
        """Test that Company requires path, name, and work_item."""
        with pytest.raises(ValidationError):
            Company()
        with pytest.raises(ValidationError):
            Company(path="/test")
        with pytest.raises(ValidationError):
            Company(path="/test", name="Company")


# ============================================================================
# Integration Tests - Full Model Hierarchy
# ============================================================================


@pytest.mark.unit
class TestModelIntegration:
    """Test the full hierarchy of models working together."""

    def test_full_hierarchy_creation(self):
        """Test creating full hierarchy: Company -> Work -> WorkInfo -> Tag."""
        # Create Tag
        tag = Tag(
            code="RJ123456",
            title={"Test Work": "url"},
            company={"TestCompany": "url"},
            star=(5, "1000"),
            genre={"Action": True, "Adventure": True},
            my_rating="5",
            my_collection="Favorites",
        )

        # Create WorkInfo
        work_info = WorkInfo(
            path="/company/work/RJ123456_info",
            tag=tag,
            images=["RJ123456_img_main.jpg", "RJ123456_img_smp0.jpg"],
        )

        # Create Work
        work = Work(
            path="/company/RJ123456_Work",
            code="RJ123456",
            name="Test Work",
            info=work_info,
        )

        # Create Company
        company = Company(
            path="/data/[TestCompany]_[RG12345]",
            name="[TestCompany]_[RG12345]",
            work_item={"RJ123456_Work": work},
        )

        # Verify full hierarchy
        assert company.work_item["RJ123456_Work"].code == "RJ123456"
        assert company.work_item["RJ123456_Work"].info.tag.code == "RJ123456"
        assert company.work_item["RJ123456_Work"].info.tag.my_rating == "5"
        assert len(company.work_item["RJ123456_Work"].info.images) == 2

    def test_multiple_works_in_company(self):
        """Test Company with multiple works."""
        works = {}
        for i in range(5):
            code = f"RJ12345{i}"
            tag = Tag(code=code)
            work_info = WorkInfo(path=f"/info/{code}", tag=tag, images=[])
            work = Work(path=f"/work/{code}", code=code, name=f"Work {i}", info=work_info)
            works[f"work_{i}"] = work

        company = Company(path="/test", name="Company", work_item=works)
        assert len(company.work_item) == 5
        for i in range(5):
            assert f"work_{i}" in company.work_item

    def test_serialization_full_hierarchy(self):
        """Test serialization of full hierarchy."""
        tag = Tag(code="RJ123456", my_rating="5")
        work_info = WorkInfo(path="/info", tag=tag, images=["img.jpg"])
        work = Work(path="/work", code="RJ123456", name="Work", info=work_info)
        company = Company(path="/company", name="Company", work_item={"w1": work})

        # Serialize
        data = company.model_dump()

        # Deserialize
        company_restored = Company(**data)
        assert company_restored.work_item["w1"].info.tag.code == "RJ123456"
        assert company_restored.work_item["w1"].info.tag.my_rating == "5"

    def test_work_without_info_in_company(self):
        """Test Company with works that don't have info yet."""
        work1 = Work(path="/work1", code="RJ123456", name="Work 1")  # No info
        tag2 = Tag(code="RJ234567")
        work_info2 = WorkInfo(path="/info2", tag=tag2, images=[])
        work2 = Work(path="/work2", code="RJ234567", name="Work 2", info=work_info2)

        company = Company(path="/test", name="Company", work_item={"w1": work1, "w2": work2})

        assert company.work_item["w1"].info is None
        assert company.work_item["w2"].info is not None

    def test_empty_company_serialization(self):
        """Test serialization of company with no works."""
        company = Company(path="/test", name="EmptyCompany", work_item={})
        data = company.model_dump()
        assert data["work_item"] == {}
        company_restored = Company(**data)
        assert len(company_restored.work_item) == 0
