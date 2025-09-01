"""Common utilities for pre-commit hooks."""
from __future__ import annotations

import argparse
import sys
from typing import Callable


def main(
    argv: list[str] | None = None,
    *,
    description: str | None = None,
    hook: Callable | None = None,
) -> int:
    """Main function for pre-commit hooks.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])
        description: Description for the argument parser
        hook: The hook function to call

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    if hook is None:
        return 0

    return hook(args.filenames)


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"ERROR: {message}", file=sys.stderr)


def print_warning(message: str) -> None:
    """Print a warning message to stderr."""
    print(f"WARNING: {message}", file=sys.stderr)
