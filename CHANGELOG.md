# Changelog

## [0.0.4] - 2026-02-25
### Added
- Automated PyPI publishing via GitHub Actions (Trusted Publishers / OIDC)
- CI test workflow running pytest across Python 3.8-3.13
- Test suite covering GPR model, analytical fits, and point particle calculations
- Package `__init__.py` now exports main classes and `__version__`
- `scikit-learn` added to dependencies (was used but undeclared)
- Python 3.13 classifier

### Fixed
- Bug in `_evaluate_Sf_fit_at_Xfit`: was calling `_gpr_output_to_remnant_mass` instead of `_gpr_output_to_remnant_spin`
- Typo: renamed `_gpr_output_to_peak_lumoinosity` to `_gpr_output_to_peak_luminosity`
- Replaced `os.system('wget')` with `urllib.request.urlretrieve` for cross-platform compatibility

### Changed
- Dropped Python 3.7 support (EOL), minimum is now Python 3.8
- Removed unused imports (`argparse`, `sys`, `subprocess`)

## [0.0.3] - 2025-10-23
### Changed
- Migrated from setup.py to pyproject.toml
- Added explicit dependencies (numpy, matplotlib, scipy)
- Updated package metadata

## [0.0.2] - Previous release
...
