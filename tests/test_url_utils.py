"""Comprehensive unit tests for URL encoding/decoding utilities.

This module tests the dlsite_classification.tools.url module with:
- Parametrized tests for efficiency
- Fixtures for data reuse
- Clear test organization
- 100% code coverage target
"""

import pytest

from dlsite_classification.tools.url import (
    build_image_url,
    decode_url_path,
    encode_path_for_url,
)


# ============================================================================
# Parametrized Tests for encode_path_for_url
# ============================================================================

@pytest.mark.unit
@pytest.mark.parametrize("original,expected", [
    # Spaces
    ("/path/file name.txt", "/path/file%20name.txt"),
    ("/path/multiple  spaces.txt", "/path/multiple%20%20spaces.txt"),

    # Special characters
    ("/path/Work & Title.txt", "/path/Work%20%26%20Title.txt"),
    ("/path/[folder]/file.txt", "/path/%5Bfolder%5D/file.txt"),
    ("/path/file+name.txt", "/path/file%2Bname.txt"),
    ("/path/100%.txt", "/path/100%25.txt"),
    ("/path/file=value.txt", "/path/file%3Dvalue.txt"),
    ("/path/file?query.txt", "/path/file%3Fquery.txt"),

    # Unicode characters
    ("/path/文件.txt", "/path/%E6%96%87%E4%BB%B6.txt"),
    ("/path/画像.jpg", "/path/%E7%94%BB%E5%83%8F.jpg"),
    ("/path/Ää Öö.txt", "/path/%C3%84%C3%A4%20%C3%96%C3%B6.txt"),

    # Mixed special characters
    ("/data/[Company] & Name/file [1].txt",
     "/data/%5BCompany%5D%20%26%20Name/file%20%5B1%5D.txt"),
])
def test_encode_path_for_url(original: str, expected: str):
    """Test URL encoding of various path formats."""
    result = encode_path_for_url(original)
    assert result == expected


@pytest.mark.unit
def test_encode_preserves_slashes():
    """Test that path separators are preserved."""
    path = "/home/user/folder/subfolder/file.txt"
    result = encode_path_for_url(path)
    assert result.count("/") == path.count("/")
    assert result.startswith("/")


@pytest.mark.unit
def test_encode_preserves_colons():
    """Test that colons are preserved (for Windows drive letters)."""
    path = "C:/Users/Public/file.txt"
    result = encode_path_for_url(path)
    assert "C:" in result
    assert "%3A" not in result  # Colon should not be encoded


@pytest.mark.unit
def test_encode_custom_safe_chars():
    """Test custom safe characters parameter."""
    path = "/path/file:name.txt"
    # Default: safe_chars='/:' - colon is safe
    result_default = encode_path_for_url(path, safe_chars='/:')
    assert result_default == "/path/file:name.txt"

    # Custom: safe_chars='/' - colon should be encoded
    result_custom = encode_path_for_url(path, safe_chars='/')
    assert result_custom == "/path/file%3Aname.txt"


# ============================================================================
# Parametrized Tests for decode_url_path
# ============================================================================

@pytest.mark.unit
@pytest.mark.parametrize("encoded,expected", [
    # Spaces
    ("/path/file%20name.txt", "/path/file name.txt"),

    # Special characters
    ("/path/Work%20%26%20Title.txt", "/path/Work & Title.txt"),
    ("/path/%5Bfolder%5D/file.txt", "/path/[folder]/file.txt"),
    ("/path/file%2Bname.txt", "/path/file+name.txt"),
    ("/path/100%25.txt", "/path/100%.txt"),

    # Unicode
    ("/path/%E6%96%87%E4%BB%B6.txt", "/path/文件.txt"),

    # Plus sign (should decode to plus, not space)
    ("/path/file+name.txt", "/path/file+name.txt"),
])
def test_decode_url_path(encoded: str, expected: str):
    """Test URL decoding of various encoded paths."""
    result = decode_url_path(encoded)
    assert result == expected


@pytest.mark.unit
def test_decode_unencoded_path():
    """Test that unencoded paths pass through unchanged."""
    path = "/simple/path/file.txt"
    result = decode_url_path(path)
    assert result == path


# ============================================================================
# Round-trip Tests
# ============================================================================

@pytest.mark.unit
def test_encode_decode_roundtrip(special_char_paths):
    """Test that encode->decode returns original path."""
    test_paths = [original for original, _ in special_char_paths]

    for original in test_paths:
        encoded = encode_path_for_url(original)
        decoded = decode_url_path(encoded)
        assert decoded == original, f"Roundtrip failed for: {original}"


@pytest.mark.unit
def test_roundtrip_real_dlsite_paths():
    """Test round-trip with real DLsite path structures."""
    paths = [
        "/mnt/d/R18/DLsite/[Company]_[ID]/[Code]_[Company]_[ID] Title/info/img.jpg",
        "/data/[nii-Cri]_[RG18556]/[RJ119254] Alice & The Room/RJ119254_info/img_main.jpg",
        "/path/with spaces/[brackets] & ampersands/file (1).txt",
    ]

    for original in paths:
        encoded = encode_path_for_url(original)
        decoded = decode_url_path(encoded)
        assert decoded == original


# ============================================================================
# Tests for build_image_url
# ============================================================================

@pytest.mark.unit
def test_build_image_url_simple():
    """Test image URL construction with simple path."""
    path = "/data/work/image.jpg"
    result = build_image_url(path)
    assert result == "/image?path=/data/work/image.jpg"


@pytest.mark.unit
def test_build_image_url_with_spaces():
    """Test image URL construction encodes spaces."""
    path = "/data/work folder/image file.jpg"
    result = build_image_url(path)
    assert result == "/image?path=/data/work%20folder/image%20file.jpg"
    assert " " not in result.split("?path=")[1]


@pytest.mark.unit
@pytest.mark.parametrize("path,expected_encoded", [
    ("/data/[Company]/image.jpg", "%5BCompany%5D"),
    ("/data/Work & Title/image.jpg", "%26"),
    ("/data/100%/image.jpg", "100%25"),
])
def test_build_image_url_special_chars(path: str, expected_encoded: str):
    """Test that build_image_url properly encodes special characters."""
    result = build_image_url(path)
    assert result.startswith("/image?path=")
    assert expected_encoded in result


@pytest.mark.unit
def test_build_image_url_real_dlsite_path():
    """Test with actual DLsite directory structure."""
    path = "/mnt/d/R18/DLsite/[nii-Cri]_[RG18556]/[RJ119254]_[nii-Cri]_[RG18556] Alice & The Room/RJ119254_info/RJ119254_img_main.jpg"
    result = build_image_url(path)

    # Verify structure
    assert result.startswith("/image?path=/mnt/d/R18/DLsite/")

    # Verify special characters are encoded
    query_part = result.split("?path=")[1]
    assert "%5B" in query_part  # [ encoded
    assert "%5D" in query_part  # ] encoded
    assert "%26" in query_part  # & encoded
    assert "%20" in query_part  # space encoded
    assert "[" not in query_part  # No unencoded brackets
    assert "&" not in query_part  # No unencoded ampersands


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

@pytest.mark.unit
def test_empty_string():
    """Test handling of empty strings."""
    assert encode_path_for_url("") == ""
    assert decode_url_path("") == ""
    assert build_image_url("") == "/image?path="


@pytest.mark.unit
def test_root_path():
    """Test handling of root path."""
    assert encode_path_for_url("/") == "/"
    assert decode_url_path("/") == "/"
    assert build_image_url("/") == "/image?path=/"


@pytest.mark.unit
def test_no_special_chars():
    """Test paths without special characters pass through unchanged."""
    path = "/home/user/documents/file.txt"
    encoded = encode_path_for_url(path)
    assert encoded == path


@pytest.mark.unit
def test_already_encoded_is_double_encoded():
    """Test that already-encoded paths are double-encoded.

    This documents current behavior - the functions do not
    detect or prevent double encoding.
    """
    encoded_once = "/data/file%20name.txt"
    encoded_twice = encode_path_for_url(encoded_once)
    # %20 becomes %2520
    assert "%2520" in encoded_twice
    assert encoded_twice != encoded_once


@pytest.mark.unit
def test_decode_plus_sign():
    """Test that + is treated as literal plus, not space.

    urllib.parse.unquote treats + as literal +, not space.
    (Use unquote_plus for application/x-www-form-urlencoded)
    """
    result = decode_url_path("/path/1+1=2.txt")
    assert result == "/path/1+1=2.txt"  # Plus stays as plus


@pytest.mark.unit
def test_decode_malformed_encoding():
    """Test handling of malformed percent encoding."""
    # Incomplete encoding
    result1 = decode_url_path("/path/%2")
    assert result1 == "/path/%2"  # Passes through unchanged

    # Invalid hex digits
    result2 = decode_url_path("/path/%ZZ")
    assert result2 == "/path/%ZZ"  # Passes through unchanged


@pytest.mark.unit
def test_very_long_path():
    """Test encoding/decoding of very long paths."""
    # Create a path with 100 directory levels
    long_path = "/" + "/".join([f"dir{i}" for i in range(100)]) + "/file.txt"
    encoded = encode_path_for_url(long_path)
    decoded = decode_url_path(encoded)
    assert decoded == long_path


@pytest.mark.unit
def test_path_with_newlines():
    """Test paths containing newline characters."""
    path = "/path/file\nwith\nnewlines.txt"
    encoded = encode_path_for_url(path)
    assert "\n" not in encoded
    assert "%0A" in encoded

    decoded = decode_url_path(encoded)
    assert decoded == path


# ============================================================================
# Performance and Consistency Tests
# ============================================================================

@pytest.mark.unit
def test_encoding_is_consistent():
    """Test that encoding the same path always produces same result."""
    path = "/data/[Company] & Name/file with spaces.txt"
    results = [encode_path_for_url(path) for _ in range(10)]
    assert all(r == results[0] for r in results)


@pytest.mark.unit
def test_decoding_is_consistent():
    """Test that decoding the same path always produces same result."""
    encoded = "/data/%5BCompany%5D%20%26%20Name/file%20with%20spaces.txt"
    results = [decode_url_path(encoded) for _ in range(10)]
    assert all(r == results[0] for r in results)
