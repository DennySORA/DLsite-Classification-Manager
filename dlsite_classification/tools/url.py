"""URL encoding and decoding utilities.

This module provides pure utility functions for URL encoding and decoding operations.
Following the Single Responsibility Principle, it only handles URL transformations.

Usage:
    from dlsite_classification.tools.url import encode_path_for_url, decode_url_path

    # Encode a file path for use in URL
    encoded = encode_path_for_url("/path/to/file with spaces & special.jpg")
    # Result: "/path/to/file%20with%20spaces%20%26%20special.jpg"

    # Decode a URL-encoded path
    decoded = decode_url_path("/path/to/file%20with%20spaces%20%26%20special.jpg")
    # Result: "/path/to/file with spaces & special.jpg"
"""

from urllib.parse import quote, unquote


def encode_path_for_url(file_path: str, safe_chars: str = "/:") -> str:
    """Encode a file path for safe use in URLs.

    Encodes special characters (spaces, &, [], etc.) while preserving
    path separators and colons. This ensures the path can be safely
    transmitted as a URL query parameter.

    Args:
        file_path: The file system path to encode
        safe_chars: Characters that should not be encoded (default: '/:',
                   preserves directory separators and drive letters)

    Returns:
        URL-encoded path string

    Example:
        >>> encode_path_for_url("/home/user/file name.txt")
        '/home/user/file%20name.txt'

        >>> encode_path_for_url("/data/[folder] & stuff/image.jpg")
        '/data/%5Bfolder%5D%20%26%20stuff/image.jpg'
    """
    return quote(file_path, safe=safe_chars)


def decode_url_path(url_path: str) -> str:
    """Decode a URL-encoded path back to file system path.

    Converts URL-encoded special characters (%20, %26, %5B, etc.)
    back to their original characters for file system operations.

    Args:
        url_path: URL-encoded path string

    Returns:
        Decoded file system path

    Example:
        >>> decode_url_path("/home/user/file%20name.txt")
        '/home/user/file name.txt'

        >>> decode_url_path("/data/%5Bfolder%5D%20%26%20stuff/image.jpg")
        '/data/[folder] & stuff/image.jpg'
    """
    return unquote(url_path)


def build_image_url(file_path: str) -> str:
    """Build a complete image URL from a file path.

    Encodes the file path and wraps it in the /image endpoint format.
    This is a convenience function that combines path encoding with
    URL construction.

    Args:
        file_path: Absolute file system path to the image

    Returns:
        Complete URL path for the image endpoint

    Example:
        >>> build_image_url("/data/work/RJ123456_info/img_main.jpg")
        '/image?path=/data/work/RJ123456_info/img_main.jpg'

        >>> build_image_url("/data/[Company]/Work & Title/img.jpg")
        '/image?path=/data/%5BCompany%5D/Work%20%26%20Title/img.jpg'
    """
    encoded_path = encode_path_for_url(file_path)
    return f"/image?path={encoded_path}"
