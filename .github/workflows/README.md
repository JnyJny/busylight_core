# GitHub Actions Workflows

This directory contains optimized CI/CD workflows for testing, building,
publishing, and documentation deployment.

## Workflow Architecture

The release workflow follows an efficient pipeline structure:

```
test (matrix) → build → [publish, github-release] (parallel) → docs
                ↓              ↓           ↓                     ↑
          [artifacts]    (cached artifacts) (cached artifacts)  └─(both complete)
```

## Workflows

### release.yaml
Main CI/CD pipeline triggered on version tags (e.g., `v1.2.3`).

**Stages:**
1. **test** - Matrix testing across OS/Python versions (Ubuntu, macOS, Windows × Python 3.11-3.13)
2. **build** - Single package build, uploads artifacts for reuse
3. **publish** - Publishes to PyPI using cached artifacts (parallel with github-release)
4. **github-release** - Creates GitHub release with changelog (parallel with publish)
5. **deploy-docs** - Triggers documentation deployment after successful release

**Key optimizations:**
- Package built once and reused via artifact caching
- Parallel execution of publish and release jobs
- Consolidated changelog generation
- ~3x faster than sequential builds

### docs.yml
Documentation deployment workflow.

**Triggers:**
- Repository dispatch after successful releases
- Manual workflow dispatch for ad-hoc builds

**Process:**
- Builds MkDocs documentation
- Deploys to GitHub Pages only after successful PyPI publish and GitHub release

## Requirements

The workflows require:
- PyPI project with [trusted publisher][trusted-publisher] configured
- Environment named "pypi" matching PyPI trusted publisher setup
- GitHub Pages enabled for documentation deployment

## Tricksy Jinja Formatting

The release.yaml workflow uses some Jinja templating that needs to be
hidden from cookiecutter to ensure the proper rendering of the file.

For instance this line will cause cookiecutter to choke when
attempting to render the file:


```yaml
  runs-on: ${{ matrix.os }}
```

There are a couple of ways to fix this, I chose to enclose the
offending lines with Jinja `raw` and `endraw` tags as described
[here][jinja-whitespace-control].

Checkout [this post][jinja-tricks] for a great breakdown of all the
different ways this problem can be addressed.

<!-- End Links -->
[pypi]: https://pypi.org
[trusted-publisher]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[semantic-version]: https://semver.org
[jinja-tricks]: https://github.com/cookiecutter/cookiecutter/issues/1624#issuecomment-2031117503
[jinja-whitespace-control]: https://jinja.palletsprojects.com/en/stable/templates/#whitespace-control
