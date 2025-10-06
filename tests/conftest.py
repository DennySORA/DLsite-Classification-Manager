"""Shared pytest fixtures and configuration."""
import os
import tempfile
import shutil
from pathlib import Path
import pytest
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create a temporary file for testing."""
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def sample_company_structure(temp_dir: str) -> dict:
    """Create a sample company folder structure for testing."""
    company_folder = os.path.join(temp_dir, "[TestCompany]_[RG12345]")
    work_folder = os.path.join(company_folder, "RJ123456_[TestCompany]_[RG12345] Test Work")
    info_folder = os.path.join(work_folder, "RJ123456_info")

    os.makedirs(info_folder, exist_ok=True)

    # Create sample tag files
    tag_files = {
        "code.tag": "RJ123456",
        "title.tag": "Test Work Title",
        "company.tag": "TestCompany",
        "genre.tag": "Test Genre",
        "my_rating.tag": "5",
        "my_collection.tag": "Favorites",
    }

    for filename, content in tag_files.items():
        file_path = os.path.join(info_folder, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Create sample image files
    for i in range(3):
        img_path = os.path.join(info_folder, f"RJ123456_img_smp{i}.jpg")
        Path(img_path).touch()

    main_img_path = os.path.join(info_folder, "RJ123456_img_main.jpg")
    Path(main_img_path).touch()

    return {
        "root": temp_dir,
        "company_folder": company_folder,
        "work_folder": work_folder,
        "info_folder": info_folder,
        "tag_files": tag_files,
    }


@pytest.fixture
def sample_work_codes() -> dict:
    """Provide sample DLsite work codes for testing."""
    return {
        "rj": ["RJ123456", "RJ01234567", "RJ012345"],
        "bj": ["BJ123456", "BJ01234567"],
        "vj": ["VJ123456", "VJ01234567"],
        "re": ["RE123456", "RE01234567"],
        "be": ["BE123456", "BE01234567"],
        "ve": ["VE123456", "VE01234567"],
        "rg": ["RG12345"],
        "bg": ["BG12345"],
        "vg": ["VG12345"],
        "invalid": ["XX123456", "123456", "RJABCDEF", ""],
    }


@pytest.fixture
def mock_html_response() -> str:
    """Provide mock HTML response for DLsite work page."""
    return """
    <html>
        <head><title>Test Work</title></head>
        <body>
            <h1 id="work_name">Test Work Title</h1>
            <div class="maker_name">
                <span>
                    <a href="/maker/RG12345.html">TestCompany</a>
                </span>
            </div>
            <div id="work_outline">
                <table>
                    <tr>
                        <th>ジャンル</th>
                        <td>
                            <a href="/genre/test">Test Genre</a>
                        </td>
                    </tr>
                    <tr>
                        <th>ファイル形式</th>
                        <td>PDF</td>
                    </tr>
                    <tr>
                        <th>販売日</th>
                        <td>2025年01月01日</td>
                    </tr>
                </table>
            </div>
            <div class="work_parts_area">
                <p>This is a test introduction.</p>
            </div>
            <div class="product-slider-data">
                <div class="product-slider-item" data-src="//img.dlsite.jp/test_smp1.jpg"></div>
                <div class="product-slider-item" data-src="//img.dlsite.jp/test_smp2.jpg"></div>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def disable_logging(monkeypatch):
    """Disable logging during tests to reduce noise."""
    import logging
    monkeypatch.setattr(logging, "info", lambda *args, **kwargs: None)
    monkeypatch.setattr(logging, "warning", lambda *args, **kwargs: None)
    monkeypatch.setattr(logging, "error", lambda *args, **kwargs: None)
    monkeypatch.setattr(logging, "debug", lambda *args, **kwargs: None)


# ============================================================================
# URL Testing Fixtures
# ============================================================================

@pytest.fixture
def special_char_paths() -> list[tuple[str, str]]:
    """Provide test data for paths with special characters.

    Returns:
        List of (original_path, expected_encoded_path) tuples
    """
    return [
        ("/path/file name.txt", "/path/file%20name.txt"),
        ("/path/Work & Title.txt", "/path/Work%20%26%20Title.txt"),
        ("/path/[folder]/file.txt", "/path/%5Bfolder%5D/file.txt"),
        ("/path/文件.txt", "/path/%E6%96%87%E4%BB%B6.txt"),
        ("/path/file+name.txt", "/path/file%2Bname.txt"),
        ("/path/100%.txt", "/path/100%25.txt"),
        ("/path/file=value.txt", "/path/file%3Dvalue.txt"),
        ("/path/file?query.txt", "/path/file%3Fquery.txt"),
    ]


@pytest.fixture
def malicious_paths() -> list[str]:
    """Provide test data for malicious path traversal attempts."""
    return [
        "../../../etc/passwd",
        "../../.ssh/id_rsa",
        "./../secret.txt",
        "/etc/passwd",
        "/root/.bash_history",
        "data/../../etc/passwd",
        "/data/../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",  # Windows style
    ]


# ============================================================================
# Test Markers Configuration
# ============================================================================

def pytest_configure(config):
    """Register custom markers for test categorization."""
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test (fast, isolated)"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (slower, multiple components)"
    )
    config.addinivalue_line(
        "markers",
        "e2e: mark test as an end-to-end test (slowest, full system)"
    )
    config.addinivalue_line(
        "markers",
        "security: mark test as a security-related test"
    )
