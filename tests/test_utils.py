"""Tests for utils module."""
from __future__ import annotations

from unittest.mock import patch

from pre_commit_hooks.utils import main
from pre_commit_hooks.utils import print_error
from pre_commit_hooks.utils import print_warning


def test_main_with_hook():
    """Test main function with a hook."""

    def test_hook(filenames):
        return 0 if "good.txt" in filenames else 1

    with patch("sys.argv", ["script.py", "good.txt"]):
        result = main(description="Test hook", hook=test_hook)
        assert result == 0

    with patch("sys.argv", ["script.py", "bad.txt"]):
        result = main(description="Test hook", hook=test_hook)
        assert result == 1


def test_main_without_hook():
    """Test main function without a hook."""
    with patch("sys.argv", ["script.py", "test.txt"]):
        result = main(description="Test hook")
        assert result == 0


def test_main_with_custom_argv():
    """Test main function with custom argv."""

    def test_hook(filenames):
        return 0 if filenames else 1

    result = main(argv=["test.txt"], description="Test hook", hook=test_hook)
    assert result == 0


@patch("sys.stderr")
def test_print_error(mock_stderr):
    """Test print_error function."""
    print_error("Test error message")
    mock_stderr.write.assert_called()


@patch("sys.stderr")
def test_print_warning(mock_stderr):
    """Test print_warning function."""
    print_warning("Test warning message")
    mock_stderr.write.assert_called()
