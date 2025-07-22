# CHANGELOG

## [v0.9.2](https://github.com/JnyJny/busylight-core/releases/tag/v0.9.2) - 2025-07-22 16:15:24

## Changes since v0.9.1

- v0.9.2 (93ff63d)
- Updated CLAUDE.md (73eceb6)
- cicd: Updated release workflow to include automatic changelog updates. (7fa49dc)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.9.1...v0.9.2

## [v0.9.1](https://github.com/JnyJny/busylight-core/releases/tag/v0.9.1) - 2025-07-22 01:20:47

## Changes since v0.9.0

- v0.9.1 (00d8145)
- satisfying ruff check in src and tests (4aca9d7)
- ruff check updates, refactor of the blinkstick claims methods. (2d3f681)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.9.0...v0.9.1

### Feature

- general:
  - Enhanced async task management with prioritization and error handling ([a395382](https://github.com/JnyJny/busylight-core/commit/a3953820965d7051090c55ed1d8ab8542680ad2c)) ([#8](https://github.com/JnyJny/busylight-core/pull/8))

### Documentation

- general:
  - Restore proper docstrings with Google/JavaDoc style formatting ([185e04a](https://github.com/JnyJny/busylight-core/commit/185e04a16a6fbb3959b265bace1db294c28cb62f)) ([#8](https://github.com/JnyJny/busylight-core/pull/8))

### Refactor

- general:
  - Updated agile innovative blinkstick classes with a parameterized _claims classmethod ([267de41](https://github.com/JnyJny/busylight-core/commit/267de41de4d3fb5f5d04922ad83a78669bd33cf8))
  - Replace try/except/pass with contextlib.suppress ([942c245](https://github.com/JnyJny/busylight-core/commit/942c2454bfb9a28a644227ce5713c8f1f3c9cd4d)) ([#8](https://github.com/JnyJny/busylight-core/pull/8))
  - Clean up async task management code ([ca28010](https://github.com/JnyJny/busylight-core/commit/ca280108a0dcd66e386a2c360328ac40f40f5ecb)) ([#8](https://github.com/JnyJny/busylight-core/pull/8))
  - Remove plan.md from repository ([eebd65a](https://github.com/JnyJny/busylight-core/commit/eebd65a7f5cba2113887c5d188704df45ccf98ca)) ([#7](https://github.com/JnyJny/busylight-core/pull/7))
  - complete vendor base class hierarchy standardization ([1f61902](https://github.com/JnyJny/busylight-core/commit/1f6190270737c5667d2a29235646900d66d881ff)) ([#7](https://github.com/JnyJny/busylight-core/pull/7))
  - implement Phase 1 foundation improvements ([de94f2f](https://github.com/JnyJny/busylight-core/commit/de94f2f4a19a01b943ec98382d69220d8826afe6)) ([#7](https://github.com/JnyJny/busylight-core/pull/7))

## [v0.8.0](https://github.com/JnyJny/busylight-core/releases/tag/v0.8.0) - 2025-07-20 23:20:05

## Changes since v0.7.0

- v0.8.0 (0dd8f69)
- Updated Kuando _busylight.ScaledColorField to work with 3.11 and 3.12 (73778cc)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.7.0...v0.8.0

## [v0.6.0](https://github.com/JnyJny/busylight-core/releases/tag/v0.6.0) - 2025-07-20 19:54:09

## Changes since v0.5.0

- v0.6.0 (ffba88b)
- Cleaned up poe tasks in pyproject. (073df3a)
- Ruff updates to tests. (80e4975)
- Add comprehensive tests for CompuLab fit-statUSB device (22f835a)
- Add comprehensive tests for Light.udev_rules classmethod (3aac874)
- Ruff check fixes. (ccc92a9)
- Refactored Kuando Busylight tests. (ec00ad7)
- Clean up docstrings and standardize color property documentation (367874b)
- Renamed Kuando Busylight Alpha test suite. (dab57e9)
- Refactored Kuando Busylight family and updated tests. (eac743d)
- Refactor color handling architecture across all devices (af4d85d)
- Updated .gitignore (2c26238)
- Bugfix for blinkstick_base.BlinkStickBase (35df5b8)
- Updated busylight_core.light.Light (42b8597)
- Updated Luxafor tests for proper Busy Tag vendor name. (53a935e)
- Update: Busy Tag device now in the Luxafor family of devices. (ef2ef45)
- Updated Agile Innovative BlinkStick family (f8da555)
- Updated Agile Innovative BlinkStick family of imports. (95396da)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.5.0...v0.6.0

## [v0.5.0](https://github.com/JnyJny/busylight-core/releases/tag/v0.5.0) - 2025-07-19 22:47:18

## Changes since v0.4.1

- v0.5.0 (b0948ce)
- Updated Embrava blynclight test, removed check for deleted struct property. (f640d11)
- Add BlinkStickBase abstract base class for Agile Innovative devices (889ba11)
- Simplify Embrava Blynclight implementation and improve documentation (e617c68)
- Enhance Embrava Blynclight implementation with color field support (b5a1de4)
- Enhance exception handling and improve hardware robustness (801d92a)
- Fix exception implementation and hardware handle property (d9ab8b7)
- Enhance Light class documentation and type safety (68c8e91)
- Updated test_light (db665f1)
- Updated Agile Innovative tests: ruff check (d255617)
- Updated README with link to Busylight For Humans™ (e650fc7)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.4.1...v0.5.0

## [v0.4.1](https://github.com/JnyJny/busylight-core/releases/tag/v0.4.1) - 2025-07-18 20:08:10

## Changes since v0.4.0

- v0.4.1 (f17d9d0)
- Added check to subclasses method to exclude Light subclasses whose supported_device_ids dictionary is None (1904d9e)
- Updated README.md (b11f457)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.4.0...v0.4.1

## [v0.4.0](https://github.com/JnyJny/busylight-core/releases/tag/v0.4.0) - 2025-07-18 17:42:19

## Changes since v0.3.5

- v0.4.0 (28c52e4)
- Added support for remainder of the Agile Innovative BlinkStick family of devices: BlinkStick, BlickStick Pro, BlickStick Nano, BlickStick Flex, and BlickStick Strip (3b3a4c9)
- Update BlinkStick tests for new State API (c1b0ed5)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.3.5...v0.4.0

## [v0.3.5](https://github.com/JnyJny/busylight-core/releases/tag/v0.3.5) - 2025-07-18 15:08:53

## Changes since v0.3.4

- v0.3.5 (8d9dd0c)
- Fix descriptor protocol handling for Python 3.11 compatibility (2f03dab)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.3.4...v0.3.5

## [v0.3.3](https://github.com/JnyJny/busylight-core/releases/tag/v0.3.3) - 2025-07-17 17:36:57

## Changes since v0.3.2

- v0.3.3 (e938e3f)
- Renamed Light.reset property to Light.was_reset since it shadowed the reset method. Whoops. (b29c7d7)
- ruff format tests updated unpacking. (a10f704)
- Updated MuteSync (5521c69)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.3.2...v0.3.3

## [v0.3.2](https://github.com/JnyJny/busylight-core/releases/tag/v0.3.2) - 2025-07-17 14:56:16

## Changes since v0.3.1

- v0.3.2 (888df84)
- Update mutesync claims method (38d849b)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.3.1...v0.3.2

## [v0.3.0](https://github.com/JnyJny/busylight-core/releases/tag/v0.3.0) - 2025-07-16 23:34:43

## Changes since v0.2.4

- v0.3.0 (fb45e0e)
- bug: Fixed typo in busylight_alpha (6ab20ee)
- Updated project dependencies (9939a28)
- Improve API design and test coverage with property refactoring (df3a436)
- Fix all ruff check issues in test suite and complete pytest compliance (3d47216)
- Fix all ruff check issues in src directory (c6752f7)
- Update old exception references to new exception names (0f5d07d)
- Updated base class implementations to satisfy ruff check (24b03db)
- Updated source with ruff format (52f7102)
- Updated pyproject.toml ruff check options (4e577cb)
- Updated busylight_core/light.py (254ba9d)
- Updated Vendor Embrava __init__ (8096084)
- Updated EPOS Busylight (ed88619)
- EPOS Busylight Support (ba756be)
- Updated Tests (b25f72d)
- Refactored Embrava Blynclight (c964555)
- Fixed light.Light.__hash__ (070fcbb)
- Updated MuteMe vendor tests to include MuteSync (28dc5d1)
- Removed empty vendor test for busytag (1b30067)
- Updated tests" -m "Moved MuteSync fixtures to MuteMe module. (c232f91)
- Refactor Light API to simplify device support pattern (e6a09c4)
- MuteSync now vendored by MuteMe (577913a)
- MuteSync now vendored by MuteMe (dd24156)
- Moved BusyTag to the Luxafor vendor subdirectory. (8ee7ed0)
- Updated tests/conftest.py (420361a)
- Updated pyproject.toml (204bf44)
- Updated README.md (602a686)
- Updated gitignore for .claude (1435089)
- Updated envrc (f40fbc8)
- Updated docs to highlight busylight_core.Light class (c1059d6)
- Updated .envrc (e008dfb)
- Fix API Reference navigation to properly show Light class (b3e6bda)
- Prominently feature Light class in API reference (2f26ff4)
- Improve API reference navigation with organized table of contents (2f2f48f)
- Remove pre-commit hook installation from contributing docs (aac516e)
- Update documentation to remove CLI references and expand features (76f5bf3)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight-core/compare/v0.2.4...v0.3.0

### Bug Fixes

- general:
  - Fixed typo in busylight_alpha ([6ab20ee](https://github.com/JnyJny/busylight-core/commit/6ab20eea31b9c5514bb2a083c6db1f1915fbf51d))

## [v0.2.4](https://github.com/JnyJny/busylight-core/releases/tag/v0.2.4) - 2025-07-13 20:33:04

## Changes since v0.2.3

- v0.2.4 (35e68df)
- Increased minimum python version to 3.11 (e312f9d)
## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.


**Full Changelog**: https://github.com/JnyJny/busylight_core/compare/v0.2.3...v0.2.4

\* *This CHANGELOG was automatically generated by [auto-generate-changelog](https://github.com/BobAnkh/auto-generate-changelog)*
