# Example Usage

This directory contains sample files to demonstrate the Logseq to Obsidian migration tool.

## Files Included

- `sample_logseq/pages/Sample Page.md` - Example page with tasks, properties, and links
- `sample_logseq/journals/2023_09_04.md` - Example journal entry

## Testing the Migration

1. **Run a dry-run test:**
   ```bash
   python3 logseq_to_obsidian.py --src examples/sample_logseq --out examples/output --frontmatter --status-tags --strip-properties --rename-journals --dry-run
   ```

2. **Run the actual migration:**
   ```bash
   python3 logseq_to_obsidian.py --src examples/sample_logseq --out examples/output --frontmatter --status-tags --strip-properties --rename-journals
   ```

3. **Check the output:**
   ```bash
   ls examples/output/
   cat examples/output/pages/Sample\ Page.md
   cat examples/output/journals/2023-09-04.md
   ```

## Expected Conversions

### Tasks
- `TODO` → `[ ]` with `#status/todo`
- `DOING` → `[ ]` with `#status/doing`  
- `DONE` → `[x]` with `#status/done`

### Journal Files
- `2023_09_04.md` → `2023-09-04.md`

### Frontmatter
- Properties converted to YAML frontmatter
- Dates extracted and formatted

### Links
- `[[2023_09_04]]` → `[[2023-09-04]]`
- Block references converted to Obsidian format
