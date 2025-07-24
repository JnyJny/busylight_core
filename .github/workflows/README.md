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
- [GitHub Pages enabled][github-pages] for documentation deployment

<!-- End Links -->
[pypi]: https://pypi.org
[trusted-publisher]: https://docs.pypi.org/trusted-publishers/
[github-pages]: https://docs.github.com/en/pages/getting-started-with-github-pages/enabling-github-pages-for-your-repository
