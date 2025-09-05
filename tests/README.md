# Testing Guide

This directory contains comprehensive tests for the Logseq to Obsidian migration tool.

## Test Structure

### Core Tests (`test_logseq_to_obsidian.py`)
Tests all the core functionality of the migration script:

- **Task Status Conversion**: Tests conversion of TODO, DOING, DONE, etc. to Obsidian format
- **Frontmatter Generation**: Tests YAML frontmatter creation and parsing
- **Journal File Renaming**: Tests conversion from `YYYY_MM_DD.md` to `YYYY-MM-DD.md`
- **Property Stripping**: Tests removal of Logseq-specific properties
- **Block Reference Conversion**: Tests conversion of `((uuid))` references
- **Tag Conversion**: Tests conversion of `#[[Tag With Spaces]]` to `#tag-with-spaces`
- **Date Link Conversion**: Tests conversion of `[[YYYY_MM_DD]]` to `[[YYYY-MM-DD]]`
- **Scheduled/Deadline Conversion**: Tests conversion of scheduled and deadline properties
- **Error Handling**: Tests graceful handling of malformed files
- **Dry Run Mode**: Tests that dry-run mode doesn't create files
- **Command Line Interface**: Tests help output and argument parsing

### Integration Tests (`test_examples.py`)
Tests the script with the provided example files:

- **Dry Run with Examples**: Tests dry-run mode with sample files
- **Full Migration with Examples**: Tests complete migration with all options
- **Minimal Migration**: Tests basic migration without conversion options

## Running Tests

### Quick Test Run
```bash
# Run all tests
python3 tests/run_tests.py

# Run specific test file
python3 -m unittest tests.test_logseq_to_obsidian -v

# Run specific test class
python3 -m unittest tests.test_logseq_to_obsidian.TestLogseqToObsidian.test_task_status_conversion -v
```

### Manual Testing
```bash
# Test with example files
python3 logseq_to_obsidian.py --src examples/sample_logseq --out test_output --frontmatter --status-tags --strip-properties --rename-journals --dry-run

# Test actual migration
python3 logseq_to_obsidian.py --src examples/sample_logseq --out test_output --frontmatter --status-tags --strip-properties --rename-journals
```

## Test Coverage

The tests cover all major functionality claimed by the script:

### ✅ Task Status Conversion
- TODO → `[ ]` with `#status/todo`
- DOING → `[ ]` with `#status/doing`
- NOW → `[ ]` with `#status/now`
- LATER → `[ ]` with `#status/later`
- WAITING → `[ ]` with `#status/waiting`
- DONE → `[x]` with `#status/done`
- CANCELED/CANCELLED → `[x]` with `#status/done`

### ✅ Frontmatter Features
- YAML frontmatter generation
- Title extraction from filename
- Date extraction from filename or properties
- Tag conversion from properties
- Error handling for malformed YAML

### ✅ File Operations
- Journal file renaming (underscore to hyphen)
- Property stripping
- Block reference conversion
- Tag format conversion
- Date link conversion

### ✅ Error Handling
- Malformed YAML frontmatter
- Missing source directories
- Empty directories
- Invalid command line arguments

### ✅ Command Line Interface
- Help output
- All command line options
- Dry-run mode
- Error reporting

## Test Data

### Sample Files
- `examples/sample_logseq/pages/Sample Page.md` - Contains various task statuses, properties, and links
- `examples/sample_logseq/journals/2023_09_04.md` - Sample journal entry

### Generated Test Files
Tests create temporary files with specific content to test individual features.

## Continuous Integration

The GitHub Actions workflow (`.github/workflows/test.yml`) automatically runs these tests on:
- Every push to main branch
- Every pull request
- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)

## Adding New Tests

When adding new features to the script:

1. **Add test case** to `test_logseq_to_obsidian.py`
2. **Test the feature** with various inputs
3. **Test error cases** and edge conditions
4. **Update documentation** if needed
5. **Run tests** to ensure they pass

### Test Case Template
```python
def test_new_feature(self):
    """Test description of what this feature does"""
    # Setup test data
    content = """# Test Content
    
    Test content here.
    """
    self.create_test_file('pages/Test Feature.md', content)
    
    # Run migration
    result = self.run_script([
        '--src', self.test_dir,
        '--out', os.path.join(self.test_dir, 'output'),
        '--new-option'
    ])
    
    # Verify results
    self.assertEqual(result.returncode, 0)
    
    # Check output
    output_file = os.path.join(self.test_dir, 'output', 'pages', 'Test Feature.md')
    self.assertTrue(os.path.exists(output_file))
    
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()
    
    # Verify specific conversions
    self.assertIn('expected output', output_content)
    self.assertNotIn('unexpected content', output_content)
```

## Troubleshooting Tests

### Common Issues

1. **Import Errors**: Make sure the script path is correct
2. **Permission Errors**: Ensure test directories are writable
3. **Path Issues**: Use absolute paths for test files
4. **Encoding Issues**: Always specify UTF-8 encoding

### Debug Mode
```bash
# Run with verbose output
python3 -m unittest tests.test_logseq_to_obsidian -v

# Run single test with debug output
python3 -c "
import sys
sys.path.insert(0, 'tests')
from test_logseq_to_obsidian import TestLogseqToObsidian
import unittest
suite = unittest.TestLoader().loadTestsFromName('test_logseq_to_obsidian.TestLogseqToObsidian.test_task_status_conversion')
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
"
```

## Test Results

A successful test run should show:
- All tests passing ✅
- No failures or errors
- Proper file conversions
- Correct output format
- Error handling working as expected

The tests validate that the script does exactly what it claims to do in the README and documentation.
