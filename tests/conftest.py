"""Test configuration and utilities."""
from __future__ import annotations

import pytest


@pytest.fixture
def temp_files(tmp_path):
    """Create temporary files for testing."""
    files = []

    def _create_file(name: str, content: str = "") -> str:
        file_path = tmp_path / name
        file_path.write_text(content)
        files.append(str(file_path))
        return str(file_path)

    yield _create_file

    # Cleanup
    for file_path in files:
        try:
            import os

            os.unlink(file_path)
        except OSError:
            pass
