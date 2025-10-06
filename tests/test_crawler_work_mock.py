"""Mock test suite for DLsite work crawler.

This module provides comprehensive mock testing for the DLsiteWorkCrawler class,
avoiding real HTTP requests while ensuring correct parsing and error handling.

Test Coverage:
    - Mock HTTP response handling
    - URL generation for different code prefixes (RJ/BJ/VJ)
    - HTML parsing logic
    - Tag conversion and text extraction
    - Error handling (invalid codes, empty responses, malformed HTML)
    - Async operation flow
"""

from unittest.mock import AsyncMock, patch

import pytest
from bs4 import BeautifulSoup

from dlsite_classification.common.dlsite import BJ_WEBPATH, RJ_WEBPATH, VJ_WEBPATH
from dlsite_classification.crawler.work import DLsiteWorkCrawler


# ============================================================================
# Mock HTML Response Fixtures
# ============================================================================

@pytest.fixture
def mock_complete_html() -> str:
    """Complete DLsite work page HTML with all fields."""
    return """
    <html>
        <head><title>Test Work</title></head>
        <body>
            <h1>【テストタイトル】Test Work Title</h1>
            <div id="work_right_inner">
                <span class="maker_name">
                    <a href="/maniax/maker/=/maker_id/RG12345.html">TestCompany</a>
                </span>
                <table id="work_outline">
                    <tr>
                        <th>販売日</th>
                        <td>2025年01月15日</td>
                    </tr>
                    <tr>
                        <th>ジャンル</th>
                        <td>
                            アドベンチャー
                            ファンタジー
                        </td>
                    </tr>
                    <tr>
                        <th>ファイル形式</th>
                        <td>アプリケーション</td>
                    </tr>
                    <tr>
                        <th>年齢指定</th>
                        <td>R-18</td>
                    </tr>
                    <tr>
                        <th>作品形式</th>
                        <td>ロールプレイング</td>
                    </tr>
                    <tr>
                        <th>声優</th>
                        <td>
                            Test Voice Actor 1
                            Test Voice Actor 2
                        </td>
                    </tr>
                    <tr>
                        <th>イラスト</th>
                        <td>Test Illustrator</td>
                    </tr>
                </table>
            </div>
            <div class="work_parts_area">
                これはテスト作品の紹介文です。
                This is a test introduction.
            </div>
            <div class="product-slider-data">
                <div data-src="//img.dlsite.jp/modpub/images/RJ123456_img_main.jpg"></div>
                <div data-src="//img.dlsite.jp/modpub/images/RJ123456_img_smp0.jpg"></div>
                <div data-src="//img.dlsite.jp/modpub/images/RJ123456_img_smp1.jpg"></div>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_minimal_html() -> str:
    """Minimal valid DLsite work page HTML with required fields only."""
    return """
    <html>
        <body>
            <h1>Minimal Work</h1>
            <div id="work_right_inner">
                <span class="maker_name">
                    <a href="/maker/RG99999.html">MinimalCompany</a>
                </span>
                <table id="work_outline">
                </table>
            </div>
            <div class="work_parts_area">
                Minimal introduction.
            </div>
            <div class="product-slider-data">
                <div data-src="//img.dlsite.jp/main.jpg"></div>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_missing_fields_html() -> str:
    """HTML with missing optional fields to test robustness."""
    return """
    <html>
        <body>
            <h1>Work Without Company</h1>
            <div id="work_right_inner">
                <span class="maker_name">
                    <!-- No anchor tag -->
                </span>
                <table id="work_outline">
                    <tr>
                        <th>販売日</th>
                        <td>2025年01月01日</td>
                    </tr>
                </table>
            </div>
            <div class="work_parts_area">Introduction text.</div>
            <div class="product-slider-data">
                <div data-src="//img.dlsite.jp/img.jpg"></div>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_empty_html() -> str:
    """Empty or invalid HTML structure."""
    return "<html><body></body></html>"


@pytest.fixture
def mock_malformed_html() -> str:
    """Malformed HTML that might cause parsing issues."""
    return """
    <html>
        <body>
            <!-- Missing h1 tag -->
            <div id="work_right_inner">
                <table id="work_outline"></table>
            </div>
        </body>
    </html>
    """


# ============================================================================
# Mock Image Data Fixtures
# ============================================================================

@pytest.fixture
def mock_image_data() -> tuple[dict, ...]:
    """Mock image data returned by CommonCrawler.get_images()."""
    return (
        {
            "data": b"fake_image_data_main",
            "url": "https://img.dlsite.jp/modpub/images/RJ123456_img_main.jpg",
            "name": "RJ123456_img_main.jpg"
        },
        {
            "data": b"fake_image_data_smp0",
            "url": "https://img.dlsite.jp/modpub/images/RJ123456_img_smp0.jpg",
            "name": "RJ123456_img_smp0.jpg"
        },
        {
            "data": b"fake_image_data_smp1",
            "url": "https://img.dlsite.jp/modpub/images/RJ123456_img_smp1.jpg",
            "name": "RJ123456_img_smp1.jpg"
        }
    )


# ============================================================================
# Test: URL Generation (_get_dlsite_url)
# ============================================================================

class TestGetDLsiteUrl:
    """Test URL generation for different work code prefixes."""

    def test_rj_code_url_generation(self):
        """RJ code should generate maniax URL."""
        crawler = DLsiteWorkCrawler(code="RJ123456")
        url = crawler._get_dlsite_url()
        assert url == f"{RJ_WEBPATH}RJ123456"

    def test_bj_code_url_generation(self):
        """BJ code should generate books URL."""
        crawler = DLsiteWorkCrawler(code="BJ234567")
        url = crawler._get_dlsite_url()
        assert url == f"{BJ_WEBPATH}BJ234567"

    def test_vj_code_url_generation(self):
        """VJ code should generate pro URL."""
        crawler = DLsiteWorkCrawler(code="VJ345678")
        url = crawler._get_dlsite_url()
        assert url == f"{VJ_WEBPATH}VJ345678"

    def test_re_code_url_generation(self):
        """RE code should also generate maniax URL (R prefix)."""
        crawler = DLsiteWorkCrawler(code="RE123456")
        url = crawler._get_dlsite_url()
        assert url == f"{RJ_WEBPATH}RE123456"

    def test_be_code_url_generation(self):
        """BE code should generate books URL (B prefix)."""
        crawler = DLsiteWorkCrawler(code="BE234567")
        url = crawler._get_dlsite_url()
        assert url == f"{BJ_WEBPATH}BE234567"

    def test_ve_code_url_generation(self):
        """VE code should generate pro URL (V prefix)."""
        crawler = DLsiteWorkCrawler(code="VE345678")
        url = crawler._get_dlsite_url()
        assert url == f"{VJ_WEBPATH}VE345678"

    def test_invalid_code_prefix_raises_error(self):
        """Invalid code prefix should raise ValueError."""
        crawler = DLsiteWorkCrawler(code="XX123456")
        with pytest.raises(ValueError, match="Not Code!"):
            crawler._get_dlsite_url()

    def test_empty_code_raises_error(self):
        """Empty code should raise ValueError."""
        crawler = DLsiteWorkCrawler(code="")
        with pytest.raises(ValueError, match="Not Code!"):
            crawler._get_dlsite_url()

    @pytest.mark.parametrize("code,expected_prefix", [
        ("RJ01234567", RJ_WEBPATH),
        ("BJ01234567", BJ_WEBPATH),
        ("VJ01234567", VJ_WEBPATH),
        ("RJ012345", RJ_WEBPATH),  # 6-digit code
        ("RJ01234567", RJ_WEBPATH),  # 8-digit code
    ])
    def test_various_code_lengths(self, code, expected_prefix):
        """Various code lengths should work correctly."""
        crawler = DLsiteWorkCrawler(code=code)
        url = crawler._get_dlsite_url()
        assert url == f"{expected_prefix}{code}"


# ============================================================================
# Test: Text and URL Extraction (_get_text_url_in_a)
# ============================================================================

class TestGetTextUrlInA:
    """Test anchor tag text and URL extraction."""

    def test_extract_text_and_url_from_anchor(self):
        """Should extract both text and href from anchor tag."""
        html = '<div><a href="/maker/RG12345.html">TestCompany</a></div>'
        soup = BeautifulSoup(html, "lxml")
        meta = soup.find("div")

        crawler = DLsiteWorkCrawler()
        result = crawler._get_text_url_in_a(meta)

        assert result == ["TestCompany", "/maker/RG12345.html"]

    def test_extract_text_with_newlines(self):
        """Should remove newlines from extracted text."""
        html = '<div><a href="/test.html">\n  Multi\n  Line\n  Text\n  </a></div>'
        soup = BeautifulSoup(html, "lxml")
        meta = soup.find("div")

        crawler = DLsiteWorkCrawler()
        result = crawler._get_text_url_in_a(meta)

        assert result[0] == "  Multi  Line  Text  "
        assert "\n" not in result[0]

    def test_missing_anchor_tag_returns_empty(self):
        """Should return empty strings when anchor tag is missing."""
        html = '<div><span>No anchor here</span></div>'
        soup = BeautifulSoup(html, "lxml")
        meta = soup.find("div")

        crawler = DLsiteWorkCrawler()
        result = crawler._get_text_url_in_a(meta)

        assert result == ["", ""]

    def test_anchor_without_href(self):
        """Should handle anchor tag without href attribute."""
        html = '<div><a>No href attribute</a></div>'
        soup = BeautifulSoup(html, "lxml")
        meta = soup.find("div")

        crawler = DLsiteWorkCrawler()
        result = crawler._get_text_url_in_a(meta)

        assert result == ["No href attribute", ""]

    def test_empty_anchor_tag(self):
        """Should handle empty anchor tag."""
        html = '<div><a href="/test.html"></a></div>'
        soup = BeautifulSoup(html, "lxml")
        meta = soup.find("div")

        crawler = DLsiteWorkCrawler()
        result = crawler._get_text_url_in_a(meta)

        assert result == ["", "/test.html"]


# ============================================================================
# Test: Tag Conversion to Dictionary (_tag_convert_dict)
# ============================================================================

class TestTagConvertDict:
    """Test conversion of HTML table rows to dictionary."""

    def test_convert_single_row_to_dict(self):
        """Should convert single table row to dict entry."""
        html = '<table><tr><th>販売日</th><td>2025年01月01日</td></tr></table>'
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("tr")

        crawler = DLsiteWorkCrawler()
        result = crawler._tag_convert_dict(tables)

        assert "販売日" in result
        assert result["販売日"].text == "2025年01月01日"

    def test_convert_multiple_rows_to_dict(self):
        """Should convert multiple table rows to dict."""
        html = """
        <table>
            <tr><th>販売日</th><td>2025年01月01日</td></tr>
            <tr><th>ジャンル</th><td>アドベンチャー</td></tr>
            <tr><th>ファイル形式</th><td>アプリケーション</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("tr")

        crawler = DLsiteWorkCrawler()
        result = crawler._tag_convert_dict(tables)

        assert len(result) == 3
        assert "販売日" in result
        assert "ジャンル" in result
        assert "ファイル形式" in result

    def test_convert_empty_table_list(self):
        """Should handle empty table list."""
        crawler = DLsiteWorkCrawler()
        result = crawler._tag_convert_dict([])

        assert result == {}

    def test_preserve_td_element_not_just_text(self):
        """Should preserve td element (not just text) for further processing."""
        html = '<table><tr><th>Key</th><td>Value</td></tr></table>'
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("tr")

        crawler = DLsiteWorkCrawler()
        result = crawler._tag_convert_dict(tables)

        # td should be a BeautifulSoup element, not string
        assert hasattr(result["Key"], "text")
        assert result["Key"].text == "Value"


# ============================================================================
# Test: HTML Format Parsing (format method)
# ============================================================================

@pytest.mark.asyncio
class TestFormatMethod:
    """Test HTML parsing and data extraction."""

    async def test_parse_complete_html(self, mock_complete_html, mock_image_data):
        """Should parse complete HTML with all fields."""
        soup = BeautifulSoup(mock_complete_html, "lxml")
        url = f"{RJ_WEBPATH}RJ123456"

        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch.object(
            crawler.__class__,
            "_get_dlsite_url",
            return_value=url
        ):
            # Mock get_images to avoid actual HTTP requests
            with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                      new_callable=AsyncMock,
                      return_value=mock_image_data):
                info = await crawler.format(soup, url)

        # Verify basic fields
        assert "title" in info
        assert "【テストタイトル】Test Work Title" in info["title"][0]
        assert url in info["title"][1]

        assert "code" in info
        assert info["code"] == "RJ123456"

        assert "company" in info
        assert "TestCompany" in info["company"][0]

        assert "introduction" in info
        assert "これはテスト作品の紹介文です。" in info["introduction"]

        # Verify metadata fields
        assert "販売日" in info
        assert "ジャンル" in info
        assert "ファイル形式" in info

        # Verify images
        assert "images" in info
        assert len(info["images"]) == 3

    async def test_parse_minimal_html(self, mock_minimal_html):
        """Should parse minimal HTML with only required fields."""
        soup = BeautifulSoup(mock_minimal_html, "lxml")
        url = f"{RJ_WEBPATH}RJ999999"

        crawler = DLsiteWorkCrawler(code="RJ999999")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock,
                  return_value=[{"data": b"img", "url": "test.jpg", "name": "test.jpg"}]):
            info = await crawler.format(soup, url)

        assert "title" in info
        assert "company" in info
        assert "code" in info
        assert "introduction" in info
        assert "images" in info

    async def test_parse_missing_company_anchor(self, mock_missing_fields_html):
        """Should handle missing company anchor tag gracefully."""
        soup = BeautifulSoup(mock_missing_fields_html, "lxml")
        url = f"{RJ_WEBPATH}RJ888888"

        crawler = DLsiteWorkCrawler(code="RJ888888")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock,
                  return_value=[{"data": b"img", "url": "test.jpg", "name": "test.jpg"}]):
            info = await crawler.format(soup, url)

        # Should have empty company info
        assert "company" in info
        assert info["company"] == ["", ""]

    async def test_parse_multiline_genre_field(self, mock_complete_html, mock_image_data):
        """Should correctly parse genre field with multiple lines."""
        soup = BeautifulSoup(mock_complete_html, "lxml")
        url = f"{RJ_WEBPATH}RJ123456"

        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock,
                  return_value=mock_image_data):
            info = await crawler.format(soup, url)

        # Genre field should be split and stripped
        assert "ジャンル" in info
        assert isinstance(info["ジャンル"], list)
        assert "アドベンチャー" in info["ジャンル"]
        assert "ファンタジー" in info["ジャンル"]

    async def test_extract_images_with_https_prefix(self, mock_complete_html, mock_image_data):
        """Should add https: prefix to image URLs."""
        soup = BeautifulSoup(mock_complete_html, "lxml")
        url = f"{RJ_WEBPATH}RJ123456"

        crawler = DLsiteWorkCrawler(code="RJ123456")

        # Capture the arguments passed to get_images
        with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock,
                  return_value=mock_image_data) as mock_get_images:
            await crawler.format(soup, url)

            # Verify get_images was called with correct URLs
            call_args = mock_get_images.call_args[0][0]
            assert all(url.startswith("https:") for url in call_args)
            assert any("RJ123456_img_main.jpg" in url for url in call_args)

    async def test_empty_html_raises_descriptive_error(self, mock_empty_html):
        """Empty HTML should raise a descriptive ValueError."""
        soup = BeautifulSoup(mock_empty_html, "lxml")
        url = f"{RJ_WEBPATH}RJ000000"

        crawler = DLsiteWorkCrawler(code="RJ000000")

        with pytest.raises(ValueError, match="missing <h1>"):
            await crawler.format(soup, url)


# ============================================================================
# Test: Full get_use_code Workflow
# ============================================================================

@pytest.mark.asyncio
class TestGetUseCodeWorkflow:
    """Test complete workflow of fetching and parsing work data."""

    async def test_successful_code_fetch(self, mock_complete_html, mock_image_data):
        """Should successfully fetch and parse work data."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        # Mock the CommonCrawler.get_request method
        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request:
            soup = BeautifulSoup(mock_complete_html, "lxml")
            mock_request.return_value = (mock_complete_html, soup)

            # Mock get_images
            with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                      new_callable=AsyncMock,
                      return_value=mock_image_data):
                await crawler.get_use_code()

        # Verify crawler state updated correctly
        assert crawler.code == "RJ123456"
        assert crawler.title != ""
        assert len(crawler.info) > 0
        assert "title" in crawler.info
        assert "code" in crawler.info

    async def test_invalid_code_raises_error(self):
        """Should raise ValueError for invalid work code."""
        crawler = DLsiteWorkCrawler(code="INVALID123")

        with pytest.raises(ValueError, match="Not Code!"):
            await crawler.get_use_code()

    async def test_empty_response_raises_error(self, mock_empty_html):
        """Should raise ValueError when response has no data."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request:
            soup = BeautifulSoup(mock_empty_html, "lxml")
            mock_request.return_value = (mock_empty_html, soup)

            with pytest.raises(ValueError, match="missing <h1>"):
                await crawler.get_use_code()

    async def test_http_request_called_with_correct_url(self, mock_complete_html, mock_image_data):
        """Should call HTTP request with correctly generated URL."""
        crawler = DLsiteWorkCrawler(code="BJ234567")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request:
            soup = BeautifulSoup(mock_complete_html, "lxml")
            mock_request.return_value = (mock_complete_html, soup)

            with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                      new_callable=AsyncMock,
                      return_value=mock_image_data):
                await crawler.get_use_code()

            # Verify get_request was called with BJ URL
            expected_url = f"{BJ_WEBPATH}BJ234567"
            mock_request.assert_called_once_with(expected_url)

    async def test_code_and_title_updated_after_fetch(self, mock_complete_html, mock_image_data):
        """Should update code and title from fetched data."""
        # Start with different code/title
        crawler = DLsiteWorkCrawler(code="RJ999999", title="Old Title")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request:
            soup = BeautifulSoup(mock_complete_html, "lxml")
            mock_request.return_value = (mock_complete_html, soup)

            with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                      new_callable=AsyncMock,
                      return_value=mock_image_data):
                await crawler.get_use_code()

        # Code should be updated from parsed data
        assert crawler.code == "RJ999999"
        assert crawler.title == ["【テストタイトル】Test Work Title", f"{RJ_WEBPATH}RJ999999"]


# ============================================================================
# Test: get_info Method
# ============================================================================

class TestGetInfoMethod:
    """Test retrieval of parsed work information."""

    def test_get_info_returns_data_when_available(self):
        """Should return info dict when data has been fetched."""
        crawler = DLsiteWorkCrawler(code="RJ123456")
        crawler.info = {
            "title": ["Test Title", "http://example.com"],
            "code": "RJ123456",
            "company": ["TestCompany", "/maker/RG12345.html"]
        }

        result = crawler.get_info()

        assert result is not None
        assert result == crawler.info

    def test_get_info_returns_none_when_empty(self):
        """Should return None when no data has been fetched."""
        crawler = DLsiteWorkCrawler(code="RJ123456")
        crawler.info = {}

        result = crawler.get_info()

        assert result is None

    def test_get_info_returns_none_on_initialization(self):
        """Should return None on fresh initialization."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        result = crawler.get_info()

        assert result is None


# ============================================================================
# Test: Error Handling and Edge Cases
# ============================================================================

@pytest.mark.asyncio
class TestErrorHandlingEdgeCases:
    """Test error handling and edge cases."""

    async def test_network_error_propagates(self):
        """Network errors should propagate to caller."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock,
                  side_effect=Exception("Network error")):
            with pytest.raises(Exception, match="Network error"):
                await crawler.get_use_code()

    async def test_malformed_html_handling(self, mock_malformed_html):
        """Should handle malformed HTML gracefully."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request:
            soup = BeautifulSoup(mock_malformed_html, "lxml")
            mock_request.return_value = (mock_malformed_html, soup)

            with pytest.raises(ValueError, match="missing <h1>"):
                await crawler.get_use_code()

    async def test_missing_product_slider_data(self):
        """Should handle missing product slider data."""
        html = """
        <html>
            <body>
                <h1>Test Work</h1>
                <div id="work_right_inner">
                    <span class="maker_name"><a href="/maker/RG12345.html">Company</a></span>
                    <table id="work_outline"></table>
                </div>
                <div class="work_parts_area">Introduction</div>
                <!-- Missing product-slider-data div -->
            </body>
        </html>
        """

        crawler = DLsiteWorkCrawler(code="RJ123456")
        soup = BeautifulSoup(html, "lxml")
        url = f"{RJ_WEBPATH}RJ123456"

        with pytest.raises(ValueError, match="product-slider-data"):
            await crawler.format(soup, url)

    async def test_code_with_different_lengths(self):
        """Should handle codes with different digit lengths."""
        # 6-digit code
        crawler1 = DLsiteWorkCrawler(code="RJ123456")
        url1 = crawler1._get_dlsite_url()
        assert "RJ123456" in url1

        # 8-digit code
        crawler2 = DLsiteWorkCrawler(code="RJ01234567")
        url2 = crawler2._get_dlsite_url()
        assert "RJ01234567" in url2

    async def test_unicode_handling_in_text(self, mock_complete_html, mock_image_data):
        """Should correctly handle Japanese and Unicode characters."""
        soup = BeautifulSoup(mock_complete_html, "lxml")
        url = f"{RJ_WEBPATH}RJ123456"

        crawler = DLsiteWorkCrawler(code="RJ123456")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock,
                  return_value=mock_image_data):
            info = await crawler.format(soup, url)

        # Should preserve Japanese characters
        assert "これはテスト作品の紹介文です。" in info["introduction"]

    @pytest.mark.parametrize("code", [
        "RJ123456",
        "RJ01234567",
        "BJ123456",
        "VJ123456",
        "RE123456",
        "BE123456",
        "VE123456",
    ])
    async def test_various_valid_code_formats(self, code, mock_complete_html, mock_image_data):
        """Should handle all valid DLsite code formats."""
        crawler = DLsiteWorkCrawler(code=code)
        url = crawler._get_dlsite_url()

        # Should not raise error
        assert url.startswith("https://")
        assert code in url

    async def test_initialization_with_empty_strings(self):
        """Should handle initialization with empty strings."""
        crawler = DLsiteWorkCrawler(code="", title="")

        assert crawler.code == ""
        assert crawler.title == ""
        assert crawler.info == {}
        assert crawler.html is None
        assert crawler.bs4 is None

    async def test_initialization_with_title(self):
        """Should correctly initialize with code and title."""
        crawler = DLsiteWorkCrawler(code="RJ123456", title="Test Title")

        assert crawler.code == "RJ123456"
        assert crawler.title == "Test Title"


# ============================================================================
# Test: Integration-like Mock Tests
# ============================================================================

@pytest.mark.asyncio
class TestIntegrationMockScenarios:
    """Test realistic scenarios with full mock stack."""

    async def test_complete_workflow_rj_code(self, mock_complete_html, mock_image_data):
        """Test complete workflow for RJ code from start to finish."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        # Mock all external dependencies
        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request, \
             patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock) as mock_images:

            soup = BeautifulSoup(mock_complete_html, "lxml")
            mock_request.return_value = (mock_complete_html, soup)
            mock_images.return_value = mock_image_data

            # Execute workflow
            await crawler.get_use_code()

            # Verify all steps executed
            mock_request.assert_called_once()
            mock_images.assert_called_once()

            # Verify results
            info = crawler.get_info()
            assert info is not None
            assert "title" in info
            assert "code" in info
            assert "company" in info
            assert "images" in info
            assert len(info["images"]) == 3

    async def test_complete_workflow_bj_code(self, mock_minimal_html):
        """Test complete workflow for BJ code (books)."""
        crawler = DLsiteWorkCrawler(code="BJ234567")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock) as mock_request, \
             patch("dlsite_classification.crawler.work.CommonCrawler.get_images",
                  new_callable=AsyncMock) as mock_images:

            soup = BeautifulSoup(mock_minimal_html, "lxml")
            mock_request.return_value = (mock_minimal_html, soup)
            mock_images.return_value = [{"data": b"img", "url": "test.jpg", "name": "test.jpg"}]

            await crawler.get_use_code()

            # Verify correct URL was used
            call_args = mock_request.call_args[0][0]
            assert BJ_WEBPATH in call_args
            assert "BJ234567" in call_args

    async def test_retry_logic_not_implemented(self):
        """Verify that retry logic is not implemented (fails immediately)."""
        crawler = DLsiteWorkCrawler(code="RJ123456")

        call_count = 0

        async def failing_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise Exception("Network error")

        with patch("dlsite_classification.crawler.work.CommonCrawler.get_request",
                  new_callable=AsyncMock,
                  side_effect=failing_request):
            with pytest.raises(Exception, match="Network error"):
                await crawler.get_use_code()

            # Should fail immediately, not retry
            assert call_count == 1
