"""Security utilities for path validation and access control.

This module provides security-focused utility functions for validating
file paths and preventing directory traversal attacks. Following the
Single Responsibility Principle, it focuses solely on security validation.

Usage:
    from dlsite_classification.common.security import validate_path_within_root

    # Validate that a path is within allowed directory
    try:
        validate_path_within_root("/data/images/file.jpg", "/data")
        # Path is safe, proceed with file access
    except ValueError as e:
        # Path is outside allowed directory or invalid
        print(f"Security violation: {e}")
"""

import os


class PathSecurityError(ValueError):
    """Raised when a path fails security validation.

    This exception indicates a potential directory traversal attack
    or attempt to access files outside the allowed root directory.
    """


def validate_path_within_root(
    file_path: str, root_path: str, check_exists: bool = True
) -> str:
    """Validate that a file path is within the allowed root directory.

    Performs security checks to prevent directory traversal attacks:
    1. Resolves both paths to absolute real paths (following symlinks)
    2. Ensures the file path starts with the root path
    3. Optionally checks if the file exists

    This implements the Dependency Inversion Principle by accepting
    any root path, making it reusable across different contexts.

    Args:
        file_path: The file path to validate
        root_path: The root directory that must contain the file
        check_exists: If True, raises error if file doesn't exist (default: True)

    Returns:
        The resolved absolute path if validation passes

    Raises:
        PathSecurityError: If path is outside root or validation fails
        FileNotFoundError: If check_exists=True and file doesn't exist

    Example:
        >>> validate_path_within_root("/data/work/img.jpg", "/data")
        '/data/work/img.jpg'

        >>> validate_path_within_root("/etc/passwd", "/data")
        PathSecurityError: Path is outside allowed directory

        >>> # Prevents traversal attacks
        >>> validate_path_within_root("/data/../etc/passwd", "/data")
        PathSecurityError: Path is outside allowed directory
    """
    # Resolve to absolute real paths (follows symlinks)
    try:
        real_file_path = os.path.realpath(file_path)
        real_root_path = os.path.realpath(root_path)
    except (OSError, ValueError) as e:
        raise PathSecurityError(f"Invalid path: {e}") from e

    # Security check: ensure file is within root directory
    # Use os.path.commonpath to prevent prefix-based bypasses (e.g., /data2)
    try:
        common = os.path.commonpath([real_file_path, real_root_path])
        if common != real_root_path:
            raise PathSecurityError(
                f"Access denied: path '{file_path}' is outside "
                f"allowed directory '{root_path}'"
            )
    except ValueError as e:
        # Paths are on different drives (Windows) or one is relative
        raise PathSecurityError(
            f"Access denied: path '{file_path}' is outside "
            f"allowed directory '{root_path}'"
        ) from e

    # Optional existence check
    if check_exists and not os.path.exists(real_file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return real_file_path


def is_path_safe(file_path: str, root_path: str) -> bool:
    """Check if a path is safe without raising exceptions.

    Convenience function for boolean path safety checks.
    Returns True if path passes validation, False otherwise.

    Args:
        file_path: The file path to check
        root_path: The root directory that must contain the file

    Returns:
        True if path is safe, False otherwise

    Example:
        >>> is_path_safe("/data/work/img.jpg", "/data")
        True

        >>> is_path_safe("/etc/passwd", "/data")
        False
    """
    try:
        validate_path_within_root(file_path, root_path, check_exists=False)
        return True
    except (PathSecurityError, FileNotFoundError):
        return False


def get_safe_path(file_path: str, root_path: str) -> str | None:
    """Get validated path or None if invalid.

    Convenience function for safely getting a validated path.
    Returns the resolved path if valid, None if invalid.

    Args:
        file_path: The file path to validate
        root_path: The root directory that must contain the file

    Returns:
        Resolved absolute path if valid, None otherwise

    Example:
        >>> get_safe_path("/data/work/img.jpg", "/data")
        '/data/work/img.jpg'

        >>> get_safe_path("/etc/passwd", "/data")
        None
    """
    try:
        return validate_path_within_root(file_path, root_path, check_exists=False)
    except (PathSecurityError, FileNotFoundError):
        return None
