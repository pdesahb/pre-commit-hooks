"""Check commit size limits."""
from __future__ import annotations

import argparse
import fnmatch
import logging
import subprocess

from pre_commit_hooks.utils import print_error
from pre_commit_hooks.utils import print_warning


logger = logging.getLogger(__name__)


def get_commit_stats(exclude: list[str] = []) -> tuple[int, int]:
    """Get the number of additions and deletions for the current commit.

    Returns:
        Tuple of (additions, deletions)
    """
    try:
        # Get the diff stats for the staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--numstat"],
            capture_output=True,
            text=True,
            check=True,
        )

        additions = 0
        deletions = 0

        for line in result.stdout.strip().split("\n"):
            if line.strip():
                try:
                    added, deleted, filename = line.split("\t")
                    if not any(
                        fnmatch.fnmatch(filename, pattern) for pattern in exclude
                    ):
                        additions += int(added) if added != "-" else 0
                        deletions += int(deleted) if deleted != "-" else 0
                    else:
                        print_warning(f"{filename} is excluded")
                except ValueError:
                    continue

        return additions, deletions

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get git diff stats: {e}")
        return 0, 0
    except Exception as e:
        print_error(f"Unexpected error getting commit stats: {e}")
        return 0, 0


def check_commit_size(
    exclude: list[str] = [],
    max_additions: int | None = None,
    max_deletions: int | None = None,
) -> int:
    """Check if the commit size is within limits.

    Args:
        filenames: List of filenames (not used, but required by pre-commit)
        max_additions: Maximum number of additions allowed
        max_deletions: Maximum number of deletions allowed

    Returns:
        0 if within limits, 1 if limits exceeded
    """
    if max_additions is None and max_deletions is None:
        # No limits set, always pass
        return 0

    additions, deletions = get_commit_stats(exclude=exclude)

    if max_additions is not None and additions > max_additions:
        print_error(
            f"Commit has {additions} additions, "
            f"which exceeds the limit of {max_additions}",
        )
        return 1

    if max_deletions is not None and deletions > max_deletions:
        print_error(
            f"Commit has {deletions} deletions, "
            f"which exceeds the limit of {max_deletions}",
        )
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    """Main function for the commit size check hook.

    Args:
        argv: Command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Check commit size limits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check that additions don't exceed 1000 lines
  check-commit-size --max-additions 1000

  # Check that deletions don't exceed 500 lines
  check-commit-size --max-deletions 500

  # Check both additions and deletions
  check-commit-size --max-additions 1000 --max-deletions 500
        """,
    )
    parser.add_argument(
        "--max-additions",
        type=int,
        help="Maximum number of additions allowed",
        default=500,
    )
    parser.add_argument(
        "--max-deletions",
        type=int,
        help="Maximum number of deletions allowed",
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="*",
        help="Files not to consider for computing the diff size",
        default=["*.csv"],
    )

    args = parser.parse_args(argv)

    return check_commit_size(
        exclude=args.exclude,
        max_additions=args.max_additions,
        max_deletions=args.max_deletions,
    )


if __name__ == "__main__":
    exit(main())
