
[![Release][badge-release]][release]
![Version][badge-pypi-version]
![Release Date][badge-release-date]
![Python Version][badge-python-version]
![License][badge-license]
![Monthly Downloads][badge-monthly-downloads]
# busylight_core - Busylight Core for Humans

> Busylight Core Implementation for Humans, presumably like you!

<!-- project description -->

## Features

<!-- project features --> 

## Installation

### pip

```console
python3 -m pip install busylight_core
```

### uvx
```console
uvx --from busylight_core busylight_core
```

### uv

```console
uvx pip install busylight_core
```

## Usage

```console
busylight_core --help
```


## Development

This project and it's virtual environment is managed using [uv][uv] and
is configured to support automatic activation of virtual environments
using [direnv][direnv]. Development activites such as linting and testing
are automated via [Poe The Poet][poethepoet], run `poe` after cloning
this repo.

### Clone
```console
git clone https://github.com/JnyJny/busylight_core
cd busylight_core
```
### Allow Direnv _optional_ but recommended
```console
direnv allow
```

### Create a Virtual Environment
```console
uv venv
```
### Install Dependencies
```console
uv sync
```
### Run `poe`
```console
poe --help
```

### Release Management

This project uses automated release management with GitHub Actions:

#### Version Bumping
- `poe publish_patch` - Bump patch version, commit, tag, and push
- `poe publish_minor` - Bump minor version, commit, tag, and push  
- `poe publish_major` - Bump major version, commit, tag, and push

#### Release Notes
- `poe changelog` - Generate changelog since last tag
- `poe release-notes` - Generate release notes file

#### Automatic Releases
When you push a version tag (e.g., `v1.0.0`), the unified GitHub Actions workflow will:
1. **Test** - Run tests across all supported Python versions and OS combinations
2. **Publish** - Build and publish to PyPI (only if tests pass)
3. **GitHub Release** - Create GitHub release with auto-generated notes and artifacts (only if PyPI publish succeeds)

This ensures a complete release pipeline where each step depends on the previous step's success.

#### MkDocs Documentation
- `poe docs-serve` - Serve documentation locally
- `poe docs-build` - Build documentation
- `poe docs-deploy` - Deploy to GitHub Pages

The template includes MkDocs with material theme and automatic deployment to GitHub Pages.

<hr>

[![gh:JnyJny/python-package-cookiecutter][python-package-cookiecutter-badge]][python-package-cookiecutter]

<!-- End Links -->

[python-package-cookiecutter-badge]: https://img.shields.io/badge/Made_With_Cookiecutter-python--package--cookiecutter-green?style=for-the-badge
[python-package-cookiecutter]: https://github.com/JnyJny/python-package-cookiecutter
[badge-release]: https://github.com/JnyJny/busylight_core/actions/workflows/release.yaml/badge.svg
[release]: https://github.com/JnyJny/busylight_core/actions/workflows/release.yaml
[badge-pypi-version]: https://img.shields.io/pypi/v/busylight_core
[badge-release-date]: https://img.shields.io/github/release-date/JnyJny/busylight_core
[badge-python-version]: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FJnyJny%2Fbusylight_core%2Fmain%2Fpyproject.toml
[badge-license]: https://img.shields.io/github/license/JnyJny/busylight_core
[badge-monthly-downloads]: https://img.shields.io/pypi/dm/busylight_core
[poe]: https://poethepoet.natn.io
[uv]: https://docs.astral.sh/uv/
[direnv]: https://direnv.net
