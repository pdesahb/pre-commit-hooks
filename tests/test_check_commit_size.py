"""Tests for commit size check hook."""
from __future__ import annotations

import subprocess
from unittest.mock import patch

from pre_commit_hooks.check_commit_size import check_commit_size
from pre_commit_hooks.check_commit_size import get_commit_stats
from pre_commit_hooks.check_commit_size import main


class TestGetCommitStats:
    """Test the get_commit_stats function."""

    @patch("pre_commit_hooks.check_commit_size.subprocess.run")
    def test_get_commit_stats_success(self, mock_run):
        """Test successful git diff stats retrieval."""
        mock_run.return_value.stdout = "10\t5\tfile1.txt\n20\t15\tfile2.py\n"
        mock_run.return_value.check.return_value = None

        additions, deletions = get_commit_stats()

        assert additions == 30
        assert deletions == 20
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached", "--numstat"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("pre_commit_hooks.check_commit_size.subprocess.run")
    def test_get_commit_stats_with_binary_files(self, mock_run):
        """Test handling of binary files in git diff."""
        mock_run.return_value.stdout = (
            "10\t5\tfile1.txt\n-\t-\tfile2.bin\n15\t8\tfile3.py\n"
        )
        mock_run.return_value.check.return_value = None

        additions, deletions = get_commit_stats()

        assert additions == 25
        assert deletions == 13

    @patch("pre_commit_hooks.check_commit_size.subprocess.run")
    def test_get_commit_stats_empty_diff(self, mock_run):
        """Test handling of empty diff."""
        mock_run.return_value.stdout = ""
        mock_run.return_value.check.return_value = None

        additions, deletions = get_commit_stats()

        assert additions == 0
        assert deletions == 0

    @patch("pre_commit_hooks.check_commit_size.subprocess.run")
    def test_get_commit_stats_git_error(self, mock_run):
        """Test handling of git command errors."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git diff")

        additions, deletions = get_commit_stats()

        assert additions == 0
        assert deletions == 0

    @patch("pre_commit_hooks.check_commit_size.subprocess.run")
    def test_get_commit_stats_unexpected_error(self, mock_run):
        """Test handling of unexpected errors."""
        mock_run.side_effect = Exception("Unexpected error")

        additions, deletions = get_commit_stats()

        assert additions == 0
        assert deletions == 0


class TestCheckCommitSize:
    """Test the check_commit_size function."""

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_no_limits(self, mock_get_stats):
        """Test when no limits are set."""
        result = check_commit_size(["file1.txt"])

        assert result == 0
        mock_get_stats.assert_not_called()

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_within_limits(self, mock_get_stats):
        """Test when commit is within limits."""
        mock_get_stats.return_value = (50, 30)

        result = check_commit_size(["file1.txt"], max_additions=100, max_deletions=50)

        assert result == 0

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_additions_exceeded(self, mock_get_stats):
        """Test when additions exceed the limit."""
        mock_get_stats.return_value = (150, 30)

        result = check_commit_size(["file1.txt"], max_additions=100, max_deletions=50)

        assert result == 1

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_deletions_exceeded(self, mock_get_stats):
        """Test when deletions exceed the limit."""
        mock_get_stats.return_value = (50, 80)

        result = check_commit_size(["file1.txt"], max_additions=100, max_deletions=50)

        assert result == 1

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_only_additions_limit(self, mock_get_stats):
        """Test when only additions limit is set."""
        mock_get_stats.return_value = (150, 30)

        result = check_commit_size(["file1.txt"], max_additions=100)

        assert result == 1

    @patch("pre_commit_hooks.check_commit_size.get_commit_stats")
    def test_check_commit_size_only_deletions_limit(self, mock_get_stats):
        """Test when only deletions limit is set."""
        mock_get_stats.return_value = (50, 80)

        result = check_commit_size(["file1.txt"], max_deletions=50)

        assert result == 1


class TestMain:
    """Test the main function."""

    @patch("pre_commit_hooks.check_commit_size.check_commit_size")
    def test_main_with_additions_limit(self, mock_check):
        """Test main function with additions limit."""
        mock_check.return_value = 0

        result = main(["--max-additions", "100", "file1.txt"])

        assert result == 0
        mock_check.assert_called_once_with(
            ["file1.txt"],
            max_additions=100,
            max_deletions=None,
        )

    @patch("pre_commit_hooks.check_commit_size.check_commit_size")
    def test_main_with_deletions_limit(self, mock_check):
        """Test main function with deletions limit."""
        mock_check.return_value = 0

        result = main(["--max-deletions", "50", "file1.txt"])

        assert result == 0
        mock_check.assert_called_once_with(
            ["file1.txt"],
            max_additions=None,
            max_deletions=50,
        )

    @patch("pre_commit_hooks.check_commit_size.check_commit_size")
    def test_main_with_both_limits(self, mock_check):
        """Test main function with both limits."""
        mock_check.return_value = 0

        result = main(["--max-additions", "100", "--max-deletions", "50", "file1.txt"])

        assert result == 0
        mock_check.assert_called_once_with(
            ["file1.txt"],
            max_additions=100,
            max_deletions=50,
        )

    @patch("pre_commit_hooks.check_commit_size.check_commit_size")
    def test_main_no_limits(self, mock_check):
        """Test main function with no limits."""
        mock_check.return_value = 0

        result = main(["file1.txt"])

        assert result == 0
        mock_check.assert_called_once_with(
            ["file1.txt"],
            max_additions=None,
            max_deletions=None,
        )

    @patch("pre_commit_hooks.check_commit_size.check_commit_size")
    def test_main_hook_fails(self, mock_check):
        """Test main function when hook fails."""
        mock_check.return_value = 1

        result = main(["--max-additions", "100", "file1.txt"])

        assert result == 1
