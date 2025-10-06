"""Comprehensive unit tests for security validation utilities.

This module tests the dlsite_classification.common.security module with:
- Comprehensive security attack scenarios
- Path traversal attack prevention
- Symlink attack prevention
- Edge case handling
- 100% code coverage target
"""

import os
from pathlib import Path

import pytest

from dlsite_classification.common.security import (
    PathSecurityError,
    get_safe_path,
    is_path_safe,
    validate_path_within_root,
)


# ============================================================================
# Tests for validate_path_within_root
# ============================================================================

@pytest.mark.unit
@pytest.mark.security
class TestValidatePathWithinRoot:
    """Test suite for path validation function."""

    def test_valid_path_within_root(self, temp_dir):
        """Test validation of path within allowed root."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "test.txt")
        Path(test_file).write_text("test")

        result = validate_path_within_root(test_file, root)
        assert os.path.exists(result)
        assert os.path.isabs(result)

    def test_path_outside_root_raises_error(self, temp_dir):
        """Test that path outside root raises PathSecurityError."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        outside_file = os.path.join(temp_dir, "outside.txt")
        Path(outside_file).write_text("test")

        with pytest.raises(PathSecurityError) as exc_info:
            validate_path_within_root(outside_file, root)
        assert "outside allowed directory" in str(exc_info.value)

    @pytest.mark.parametrize("traversal_path", [
        "../../../etc/passwd",
        "../../.ssh/id_rsa",
        "./../secret.txt",
        "data/../../etc/passwd",
    ])
    def test_traversal_attack_prevention(self, temp_dir, traversal_path):
        """Test prevention of directory traversal attacks."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Construct full malicious path
        malicious_path = os.path.join(root, traversal_path)

        with pytest.raises(PathSecurityError):
            validate_path_within_root(malicious_path, root)

    def test_nonexistent_file_with_check_enabled(self, temp_dir):
        """Test that nonexistent file raises FileNotFoundError when check_exists=True."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        nonexistent = os.path.join(root, "nonexistent.txt")

        with pytest.raises(FileNotFoundError):
            validate_path_within_root(nonexistent, root, check_exists=True)

    def test_nonexistent_file_with_check_disabled(self, temp_dir):
        """Test that nonexistent file passes when check_exists=False."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        nonexistent = os.path.join(root, "nonexistent.txt")

        # Should not raise error
        result = validate_path_within_root(nonexistent, root, check_exists=False)
        assert os.path.isabs(result)

    def test_subdirectory_path(self, temp_dir):
        """Test validation of path in subdirectory."""
        root = os.path.join(temp_dir, "data")
        subdir = os.path.join(root, "subdir", "deep")
        os.makedirs(subdir)
        test_file = os.path.join(subdir, "file.txt")
        Path(test_file).write_text("test")

        result = validate_path_within_root(test_file, root)
        assert os.path.exists(result)

    def test_relative_path_resolution(self, temp_dir):
        """Test that relative paths are resolved correctly."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "test.txt")
        Path(test_file).write_text("test")

        # Change to root directory
        original_cwd = os.getcwd()
        try:
            os.chdir(root)
            result = validate_path_within_root("test.txt", root)
            assert os.path.isabs(result)
        finally:
            os.chdir(original_cwd)

    def test_absolute_path_outside_root(self, temp_dir):
        """Test absolute path that is outside root."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        with pytest.raises(PathSecurityError):
            validate_path_within_root("/etc/passwd", root)

    def test_symlink_attack_prevention(self, temp_dir):
        """Test prevention of symlink-based attacks."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Create file outside root
        outside = os.path.join(temp_dir, "secret.txt")
        Path(outside).write_text("secret")

        # Create symlink inside root pointing outside
        symlink = os.path.join(root, "link.txt")
        try:
            os.symlink(outside, symlink)

            # Should detect that resolved path is outside root
            with pytest.raises(PathSecurityError):
                validate_path_within_root(symlink, root)
        except OSError:
            # Skip test if symlinks not supported
            pytest.skip("Symlinks not supported on this system")


# ============================================================================
# Tests for is_path_safe
# ============================================================================

@pytest.mark.unit
@pytest.mark.security
class TestIsPathSafe:
    """Test suite for boolean path safety check."""

    def test_safe_path_returns_true(self, temp_dir):
        """Test that safe path returns True."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "test.txt")
        Path(test_file).write_text("test")

        assert is_path_safe(test_file, root) is True

    def test_unsafe_path_returns_false(self, temp_dir):
        """Test that unsafe path returns False."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        outside_file = os.path.join(temp_dir, "outside.txt")
        Path(outside_file).write_text("test")

        assert is_path_safe(outside_file, root) is False

    @pytest.mark.parametrize("malicious_path", [
        "/etc/passwd",
        "/root/.bash_history",
        "../../../etc/passwd",
    ])
    def test_malicious_paths_return_false(self, temp_dir, malicious_path):
        """Test that malicious paths return False."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Construct full path if relative
        if not os.path.isabs(malicious_path):
            full_path = os.path.join(root, malicious_path)
        else:
            full_path = malicious_path

        assert is_path_safe(full_path, root) is False

    def test_nonexistent_path_returns_true(self, temp_dir):
        """Test that nonexistent path within root returns True.

        Note: is_path_safe uses check_exists=False internally.
        """
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        nonexistent = os.path.join(root, "nonexistent.txt")

        assert is_path_safe(nonexistent, root) is True


# ============================================================================
# Tests for get_safe_path
# ============================================================================

@pytest.mark.unit
@pytest.mark.security
class TestGetSafePath:
    """Test suite for safe path retrieval."""

    def test_safe_path_returns_path(self, temp_dir):
        """Test that safe path returns resolved path."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "test.txt")
        Path(test_file).write_text("test")

        result = get_safe_path(test_file, root)
        assert result is not None
        assert os.path.isabs(result)

    def test_unsafe_path_returns_none(self, temp_dir):
        """Test that unsafe path returns None."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        outside_file = os.path.join(temp_dir, "outside.txt")
        Path(outside_file).write_text("test")

        result = get_safe_path(outside_file, root)
        assert result is None

    @pytest.mark.parametrize("malicious_path", [
        "../../../etc/passwd",
        "/etc/passwd",
        "../../.ssh/id_rsa",
    ])
    def test_malicious_paths_return_none(self, temp_dir, malicious_path):
        """Test that malicious paths return None."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        if not os.path.isabs(malicious_path):
            full_path = os.path.join(root, malicious_path)
        else:
            full_path = malicious_path

        result = get_safe_path(full_path, root)
        assert result is None


# ============================================================================
# Real-World Scenarios
# ============================================================================

@pytest.mark.unit
@pytest.mark.security
class TestRealWorldScenarios:
    """Test real-world attack and usage scenarios."""

    def test_dlsite_image_path(self, sample_company_structure):
        """Test validation of typical DLsite image path."""
        root = sample_company_structure["root"]
        info_folder = sample_company_structure["info_folder"]
        image_path = os.path.join(info_folder, "RJ123456_img_main.jpg")

        result = validate_path_within_root(image_path, root)
        assert os.path.exists(result)

    def test_nested_directory_access(self, temp_dir):
        """Test deeply nested directory access."""
        root = os.path.join(temp_dir, "data")
        nested = os.path.join(root, "a", "b", "c", "d", "e", "f", "g")
        os.makedirs(nested)
        test_file = os.path.join(nested, "file.txt")
        Path(test_file).write_text("test")

        result = validate_path_within_root(test_file, root)
        assert os.path.exists(result)

    def test_windows_style_attack(self, temp_dir):
        """Test Windows-style directory traversal."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Windows-style path traversal
        malicious = os.path.join(root, "..\\..\\..\\windows\\system32\\config\\sam")

        # On Unix systems, backslashes are literal characters in filenames,
        # so this path is safe (doesn't exist). On Windows, should raise error.
        if os.name == 'nt':
            with pytest.raises(PathSecurityError):
                validate_path_within_root(malicious, root)
        else:
            # On Unix, path doesn't traverse, but file doesn't exist either
            with pytest.raises((PathSecurityError, FileNotFoundError)):
                validate_path_within_root(malicious, root, check_exists=True)

    def test_mixed_slash_types(self, temp_dir):
        """Test paths with mixed forward/backward slashes."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Mixed slashes in path
        mixed_path = os.path.join(root, "folder\\..\\..\\secret.txt")

        # On Unix, backslashes are literal characters, not path separators
        if os.name == 'nt':
            with pytest.raises(PathSecurityError):
                validate_path_within_root(mixed_path, root)
        else:
            # On Unix, this is a weird filename, not a traversal
            with pytest.raises((PathSecurityError, FileNotFoundError)):
                validate_path_within_root(mixed_path, root, check_exists=True)

    def test_case_sensitive_paths(self, temp_dir):
        """Test path validation with different cases (Unix)."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "Test.txt")
        Path(test_file).write_text("test")

        # On case-sensitive systems, this should work
        result = validate_path_within_root(test_file, root)
        assert os.path.exists(result)


# ============================================================================
# Error Messages and Exception Details
# ============================================================================

@pytest.mark.unit
class TestErrorMessages:
    """Test error message clarity and usefulness."""

    def test_path_outside_root_message_clarity(self, temp_dir):
        """Test that error message clearly indicates the issue."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        outside = os.path.join(temp_dir, "outside.txt")
        Path(outside).write_text("test")

        with pytest.raises(PathSecurityError) as exc_info:
            validate_path_within_root(outside, root)

        error_msg = str(exc_info.value)
        # Message should mention both the path and the root
        assert "outside" in error_msg.lower() or "access denied" in error_msg.lower()

    def test_file_not_found_message_clarity(self, temp_dir):
        """Test that file not found message is clear."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        nonexistent = os.path.join(root, "nonexistent.txt")

        with pytest.raises(FileNotFoundError) as exc_info:
            validate_path_within_root(nonexistent, root, check_exists=True)

        error_msg = str(exc_info.value)
        assert "not found" in error_msg.lower()

    def test_exception_type_inheritance(self):
        """Test that PathSecurityError is a ValueError."""
        assert issubclass(PathSecurityError, ValueError)

        # Test instantiation
        exc = PathSecurityError("test message")
        assert str(exc) == "test message"
        assert isinstance(exc, ValueError)


# ============================================================================
# Edge Cases and Boundary Conditions
# ============================================================================

@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_root_path_itself(self, temp_dir):
        """Test validating the root path itself."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Validating root against itself
        result = validate_path_within_root(root, root)
        assert result == os.path.realpath(root)

    def test_empty_path_string(self, temp_dir):
        """Test handling of empty path strings."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        with pytest.raises((PathSecurityError, ValueError, OSError)):
            validate_path_within_root("", root)

    def test_none_path(self, temp_dir):
        """Test handling of None as path."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        with pytest.raises((TypeError, AttributeError)):
            validate_path_within_root(None, root)

    def test_invalid_path_type(self, temp_dir):
        """Test handling of invalid path types that cause OSError."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)

        # Path with null bytes causes OSError in realpath
        invalid_path = "/path/with\x00null"

        with pytest.raises(PathSecurityError) as exc_info:
            validate_path_within_root(invalid_path, root)
        assert "Invalid path" in str(exc_info.value)

    def test_path_with_trailing_slash(self, temp_dir):
        """Test path with trailing slash."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_dir = os.path.join(root, "subdir")
        os.makedirs(test_dir)

        # Path with trailing slash
        result = validate_path_within_root(test_dir + "/", root)
        assert os.path.isdir(result)

    def test_duplicate_slashes(self, temp_dir):
        """Test path with duplicate slashes."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "file.txt")
        Path(test_file).write_text("test")

        # Path with duplicate slashes (should be normalized)
        weird_path = root + "//file.txt"
        result = validate_path_within_root(weird_path, root)
        assert os.path.exists(result)

    def test_current_directory_reference(self, temp_dir):
        """Test path with ./. references."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "file.txt")
        Path(test_file).write_text("test")

        # Path with ./ references
        dotted_path = os.path.join(root, ".", "file.txt")
        result = validate_path_within_root(dotted_path, root)
        assert os.path.exists(result)


# ============================================================================
# Performance and Consistency Tests
# ============================================================================

@pytest.mark.unit
class TestPerformance:
    """Test performance and consistency."""

    def test_validation_is_consistent(self, temp_dir):
        """Test that validation is deterministic."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        test_file = os.path.join(root, "test.txt")
        Path(test_file).write_text("test")

        # Run validation multiple times
        results = [validate_path_within_root(test_file, root) for _ in range(10)]

        # All results should be identical
        assert all(r == results[0] for r in results)

    def test_rejection_is_consistent(self, temp_dir):
        """Test that rejection is deterministic."""
        root = os.path.join(temp_dir, "data")
        os.makedirs(root)
        malicious = "../../../etc/passwd"

        # All attempts should fail
        for _ in range(10):
            with pytest.raises(PathSecurityError):
                validate_path_within_root(malicious, root)
