"""
Tests for dlsite_classification.common.regex module

Testing regex patterns for DLsite codes, company folders, and path validation.
"""

import pytest

from dlsite_classification.common.regex import (
    REGEX_COMPANY_FOLDER,
    REGEX_PATH_REPLACE,
    REGEX_RG,
    REGEX_RJ,
)


@pytest.mark.unit
class TestRegexCompanyFolder:
    """Test REGEX_COMPANY_FOLDER pattern"""

    @pytest.mark.parametrize("folder_name", [
        "[CompanyName]",
        "[Company Name]",
        "[会社名]",
        "[123]",
        "[Company-Name_123]",
        "[Company & Co.]",
        "[CompanyName]_[RG12345]",
        "[Company Name]_[RG99999]",
        "[会社名]_[RG00001]",
    ])
    def test_matches_valid_company_folders(self, folder_name):
        """Test that valid company folder names match the pattern."""
        assert REGEX_COMPANY_FOLDER.match(folder_name) is not None

    @pytest.mark.parametrize("folder_name", [
        "CompanyName",  # Missing brackets
        "[CompanyName",  # Missing closing bracket
        "CompanyName]",  # Missing opening bracket
        "[]",  # Empty brackets
        "[Company][Name]",  # Multiple bracket pairs without underscore
        "[CompanyName]_",  # Trailing underscore without second part
        "_[CompanyName]",  # Leading underscore
        "[CompanyName]_[RG12345]_extra",  # Extra part
        "prefix_[CompanyName]",  # Prefix before brackets
    ])
    def test_does_not_match_invalid_company_folders(self, folder_name):
        """Test that invalid company folder names don't match."""
        assert REGEX_COMPANY_FOLDER.match(folder_name) is None

    def test_matches_unicode_company_names(self):
        """Test matching Unicode company names."""
        assert REGEX_COMPANY_FOLDER.match("[日本語会社名]") is not None
        assert REGEX_COMPANY_FOLDER.match("[中文公司名]") is not None
        assert REGEX_COMPANY_FOLDER.match("[한국회사]") is not None


@pytest.mark.unit
class TestRegexRJ:
    """Test REGEX_RJ pattern for DLsite work codes"""

    @pytest.mark.parametrize("code,expected_match", [
        # RJ codes (valid)
        ("RJ123456", "RJ123456"),
        ("RJ01234567", "RJ01234567"),
        ("RJ12345678", "RJ12345678"),
        # BJ codes (valid)
        ("BJ123456", "BJ123456"),
        ("BJ01234567", "BJ01234567"),
        # VJ codes (valid)
        ("VJ123456", "VJ123456"),
        ("VJ12345678", "VJ12345678"),
        # RE codes (valid)
        ("RE123456", "RE123456"),
        # BE codes (valid)
        ("BE123456", "BE123456"),
        # VE codes (valid)
        ("VE123456", "VE123456"),
    ])
    def test_matches_valid_work_codes(self, code, expected_match):
        """Test that valid DLsite work codes match."""
        match = REGEX_RJ.search(code)
        assert match is not None
        assert match.group() == expected_match

    @pytest.mark.parametrize("code", [
        "RJ12345",  # Too short (5 digits)
        "RJ123",  # Too short (3 digits)
        "XJ123456",  # Invalid prefix
        "R123456",  # Missing J
        "J123456",  # Missing R
        "rj123456",  # Lowercase
        "RJ",  # No digits
        "",  # Empty string
    ])
    def test_does_not_match_invalid_codes(self, code):
        """Test that invalid codes don't match."""
        assert REGEX_RJ.search(code) is None

    def test_extracts_code_from_text(self):
        """Test extracting code from surrounding text."""
        text = "Download RJ123456 from DLsite"
        match = REGEX_RJ.search(text)
        assert match is not None
        assert match.group() == "RJ123456"

    def test_extracts_code_from_folder_name(self):
        """Test extracting code from typical folder name."""
        folder_name = "[RJ123456]_[CompanyName]_[RG12345] Work Title"
        match = REGEX_RJ.search(folder_name)
        assert match is not None
        assert match.group() == "RJ123456"

    def test_finds_all_codes_in_text(self):
        """Test finding multiple codes in text."""
        text = "Works: RJ123456, BJ789012, VJ345678"
        matches = REGEX_RJ.findall(text)
        assert len(matches) == 3
        assert matches == ["RJ123456", "BJ789012", "VJ345678"]


@pytest.mark.unit
class TestRegexRG:
    """Test REGEX_RG pattern for company codes"""

    @pytest.mark.parametrize("code,expected_match", [
        # RG codes (valid)
        ("RG12345", "RG12345"),
        ("RG00001", "RG00001"),
        ("RG99999", "RG99999"),
        # BG codes (valid)
        ("BG12345", "BG12345"),
        # VG codes (valid)
        ("VG12345", "VG12345"),
    ])
    def test_matches_valid_company_codes(self, code, expected_match):
        """Test that valid company codes match."""
        match = REGEX_RG.search(code)
        assert match is not None
        assert match.group() == expected_match

    @pytest.mark.parametrize("code", [
        "RG1234",  # Too short (4 digits)
        "RG",  # No digits
        "XG12345",  # Invalid prefix
        "rg12345",  # Lowercase
        "R12345",  # Missing G
        "G12345",  # Missing R
        "",  # Empty string
    ])
    def test_does_not_match_invalid_codes(self, code):
        """Test that invalid company codes don't match."""
        assert REGEX_RG.search(code) is None

    def test_matches_exactly_5_digits(self):
        """Test that RG pattern matches exactly 5 digits (not more)."""
        # RG123456 has 6 digits, but regex will match first 5
        code = "RG123456"
        match = REGEX_RG.search(code)
        assert match is not None
        assert match.group() == "RG12345"  # Only first 5 digits

    def test_extracts_company_code_from_folder_name(self):
        """Test extracting company code from folder name."""
        folder_name = "[CompanyName]_[RG12345]"
        match = REGEX_RG.search(folder_name)
        assert match is not None
        assert match.group() == "RG12345"

    def test_distinguishes_rg_from_rj(self):
        """Test that RG pattern doesn't match RJ codes."""
        text = "RJ123456 and RG12345"
        matches = REGEX_RG.findall(text)
        assert len(matches) == 1
        assert matches[0] == "RG12345"


@pytest.mark.unit
class TestRegexPathReplace:
    """Test REGEX_PATH_REPLACE pattern for invalid path characters"""

    @pytest.mark.parametrize("char", [
        "\\", "/", ":", "*", "?", '"', "<", ">", "|"
    ])
    def test_matches_invalid_path_characters(self, char):
        """Test that invalid path characters are matched."""
        assert REGEX_PATH_REPLACE.search(char) is not None

    @pytest.mark.parametrize("char", [
        "a", "1", " ", "-", "_", ".", "(", ")", "[", "]",
        "!", "@", "#", "$", "%", "^", "&", "+", "=", "~"
    ])
    def test_does_not_match_valid_characters(self, char):
        """Test that valid characters are not matched."""
        assert REGEX_PATH_REPLACE.search(char) is None

    def test_replaces_invalid_characters_in_string(self):
        """Test replacing invalid characters in a string."""
        text = "File:Name*With?Invalid<Chars>"
        result = REGEX_PATH_REPLACE.sub("_", text)
        assert result == "File_Name_With_Invalid_Chars_"

    def test_multiple_replacements(self):
        """Test replacing multiple invalid characters."""
        text = "C:\\Users\\File<Name>?Test*"
        result = REGEX_PATH_REPLACE.sub("-", text)
        # The backslash is followed by a letter, so \\U is treated as one match
        assert result == "C--Users-File-Name--Test-"

    def test_preserves_valid_characters(self):
        """Test that valid characters are preserved."""
        text = "Valid_File-Name.123"
        result = REGEX_PATH_REPLACE.sub("_", text)
        assert result == text

    def test_handles_unicode_text(self):
        """Test handling Unicode text with invalid characters."""
        text = "日本語:ファイル名<テスト>"
        result = REGEX_PATH_REPLACE.sub("_", text)
        assert result == "日本語_ファイル名_テスト_"

    def test_finds_all_invalid_characters(self):
        """Test finding all invalid characters in text."""
        text = "File:Name/With\\Invalid*Chars"
        matches = REGEX_PATH_REPLACE.findall(text)
        assert matches == [":", "/", "\\", "*"]


@pytest.mark.unit
class TestRegexCombinedUsage:
    """Test combined usage of multiple regex patterns"""

    def test_real_world_folder_structure(self):
        """Test parsing a real DLsite folder structure."""
        company_folder = "[CompanyName]_[RG12345]"
        work_folder = "[RJ123456]_[CompanyName]_[RG12345] Work Title"

        # Company folder should match
        assert REGEX_COMPANY_FOLDER.match(company_folder) is not None

        # Extract work code
        rj_match = REGEX_RJ.search(work_folder)
        assert rj_match is not None
        assert rj_match.group() == "RJ123456"

        # Extract company code
        rg_match = REGEX_RG.search(work_folder)
        assert rg_match is not None
        assert rg_match.group() == "RG12345"

    def test_sanitize_folder_name(self):
        """Test sanitizing a folder name for file system."""
        raw_name = 'Work:Title/With<Invalid>Characters*?'
        sanitized = REGEX_PATH_REPLACE.sub("_", raw_name)

        # Should not contain any invalid characters
        assert not any(c in sanitized for c in r'\/:*?"<>|')
        assert sanitized == "Work_Title_With_Invalid_Characters__"

    def test_parse_multiple_codes_from_path(self):
        """Test parsing multiple codes from a complex path."""
        path = "/data/[Company]_[RG12345]/[RJ123456]_Work/[BJ789012]_Extra"

        rj_codes = REGEX_RJ.findall(path)
        rg_codes = REGEX_RG.findall(path)

        assert rj_codes == ["RJ123456", "BJ789012"]
        assert rg_codes == ["RG12345"]
