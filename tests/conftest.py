"""Busylight Core for Humans pytest configuration file."""

from pathlib import Path

import pytest
import tomllib


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the root path of the project."""
    return Path.cwd()


@pytest.fixture(scope="session")
def pyproject_path(project_root: Path) -> Path:
    """Return the path to the pyproject.toml file."""
    return project_root / "pyproject.toml"


@pytest.fixture(scope="session")
def pyproject_toml(pyproject_path: Path) -> dict:
    """Return the contents of the pyproject.toml file."""
    return tomllib.load(pyproject_path.open("rb"))


@pytest.fixture(scope="session")
def project_version(pyproject_toml: dict) -> str:
    """Return the project version from pyproject.toml."""
    return pyproject_toml["project"]["version"]
