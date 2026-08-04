# Changelog

## 0.3.0

### Fixed

- Fit Nerd Font symbols within a single half-width cell
  - Symbols previously kept their source size and overflowed into neighboring cells
  - Powerline glyphs (`U+E0B0`–`U+E0D4`) now stretch to fill the full cell so prompt separators connect seamlessly

### Changed

- Verify sha256 checksums of downloaded source archives
- Derive source archive names from `config.ini` versions
- Merge `check_metrics.py` checks into `test_font.py`

## 0.2.0

### Changed

- Update Nerd Fonts symbols from 3.4.0 to 3.5.0
  - Add Braille, Obsidian, Wireshark, and zsh icons
  - Update Codicons to 0.0.45, Devicons to 2.17.0, Font Logos to 1.4.0

## 0.1.0

Initial release.

### Added

- `Mabyko Mono NF`
- `Mabyko Mono`
- `Mabyko Mono NL`
- `Thin`, `Light`, `Regular`, `Medium`, `SemiBold`, `Bold` weights
- JetBrains Mono latin glyphs combined with D2Coding Hangul/full-width metrics
- Nerd Font symbols in the `NF` variant
- Reproducible build scripts using FontForge, fontTools, and uv
- Docker build environment
- Release packaging script
- Metric and shaping checks for VS Code-friendly `600/1200` half/full width behavior
