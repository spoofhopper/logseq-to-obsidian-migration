# Changelog

All notable changes to the Logseq to Obsidian Migration Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-04

### Added
- Initial release of Logseq to Obsidian migration tool
- Support for converting Logseq graphs to Obsidian format
- Frontmatter conversion with YAML metadata
- Journal file renaming from `YYYY_MM_DD.md` to `YYYY-MM-DD.md` format
- Task status conversion to Obsidian checkboxes with status tags
- Property stripping to remove Logseq-specific properties
- Block reference conversion from `((uuid))` to `[[page#^uuid]]`
- Tag conversion from `#[[Tag With Spaces]]` to `#tag-with-spaces`
- Date link conversion from `[[YYYY_MM_DD]]` to `[[YYYY-MM-DD]]`
- Dry-run mode for testing migrations
- Comprehensive error handling for YAML parsing
- Robust file copying with proper directory handling
- Command-line interface with multiple options
- MIT License
- Comprehensive README with usage examples
- Contributing guidelines
- Example files for testing
- Python requirements file

### Features
- **Frontmatter**: Adds YAML frontmatter with dates and titles
- **Status Tags**: Converts task status to Obsidian-compatible format
- **Journal Renaming**: Converts journal files to hyphen format
- **Property Stripping**: Removes Logseq-specific properties
- **Block References**: Converts Logseq block references to Obsidian format
- **Error Handling**: Robust YAML parsing with graceful error handling
- **Dry Run**: Test migrations before applying changes

### Technical Details
- Python 3.6+ compatibility
- PyYAML dependency for frontmatter processing
- Cross-platform file handling
- Unicode normalization for slug generation
- Comprehensive regex patterns for various conversions

## [Unreleased]

### Planned
- Automated testing with GitHub Actions
- Issue templates for bug reports and feature requests
- Performance optimizations for large graphs
- Additional date format support
- Verbose logging options
- Batch processing for multiple graphs
- GUI interface (optional)
- Obsidian plugin integration

### Known Issues
- None currently documented

---

## Version History

- **1.0.0** (2024-09-04): Initial release with core migration functionality
