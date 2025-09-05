# Logseq to Obsidian Migration Tool

A Python script to migrate your Logseq graph to Obsidian format with enhanced features and robust error handling.

## Features

- **Frontmatter Conversion**: Adds YAML frontmatter with dates and titles
- **Journal Renaming**: Converts journal files from `YYYY_MM_DD.md` to `YYYY-MM-DD.md` format
- **Status Tags**: Converts Logseq task status to Obsidian-compatible format
- **Property Stripping**: Removes Logseq-specific properties
- **Block References**: Converts Logseq block references to Obsidian format
- **Error Handling**: Robust YAML parsing with graceful error handling
- **Dry Run Support**: Test migrations before applying changes

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/logseq-to-obsidian-migration.git
cd logseq-to-obsidian-migration
```

2. Create a virtual environment:
```bash
python3 -m venv logseq_env
source logseq_env/bin/activate  # On Windows: logseq_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install pyyaml
```

## Usage

### Basic Migration
```bash
python3 logseq_to_obsidian.py --src /path/to/logseq/graph --out /path/to/obsidian/vault --frontmatter --status-tags --strip-properties --rename-journals
```

### Dry Run (Test First)
```bash
python3 logseq_to_obsidian.py --src /path/to/logseq/graph --out /path/to/obsidian/vault --frontmatter --status-tags --strip-properties --rename-journals --dry-run
```

### Options

- `--src`: Source Logseq graph directory (required)
- `--out`: Output Obsidian vault directory (optional, defaults to in-place conversion)
- `--dry-run`: Test the migration without making changes
- `--frontmatter`: Add YAML frontmatter to files
- `--status-tags`: Convert task status to tags
- `--strip-properties`: Remove Logseq properties
- `--rename-journals`: Rename journal files to hyphen format

## What Gets Converted

### Task Status
- `TODO` → `[ ]` with `#status/todo` tag
- `DOING` → `[ ]` with `#status/doing` tag
- `DONE` → `[x]` with `#status/done` tag
- `LATER` → `[ ]` with `#status/later` tag
- `WAITING` → `[ ]` with `#status/waiting` tag

### Journal Files
- `2023_09_04.md` → `2023-09-04.md`

### Block References
- `((uuid))` → `[[page-title#^uuid]]`

### Tags
- `#[[Tag With Spaces]]` → `#tag-with-spaces`

### Date Links
- `[[2023_09_04]]` → `[[2023-09-04]]`

## Example Output

**Before (Logseq):**
```markdown
- TODO Complete project proposal
- DONE Review documentation
tags:: project, work
```

**After (Obsidian):**
```markdown
---
tags: [project, work]
date: '2023-09-04'
---

- [ ] Complete project proposal #status/todo
- [x] Review documentation #status/done
```

## Requirements

- Python 3.6+
- PyYAML

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
