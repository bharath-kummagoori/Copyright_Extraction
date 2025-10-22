# Copyright Extractor

A comprehensive Python module for extracting copyright statements from text in various formats.

## Features

### Supported Copyright Formats

The extractor recognizes ALL of the following copyright variations:

✅ **copyright** (lowercase)
✅ **COPYRIGHT** (UPPERCASE)
✅ **CopyRight, copyRight** (mixed case)
✅ **©** (Unicode copyright symbol)
✅ **(c)** or **(C)** (ASCII alternatives)

### Additional Features

- 📝 Extract from text strings or files
- 📁 Search entire directories recursively
- 🔍 Handles year ranges (e.g., 2020-2023)
- 📅 Handles multiple years (e.g., 2020, 2021, 2022)
- 📍 Provides line numbers and positions
- 🎯 Get unique copyright statements
- 💬 Works with code comments (Python, C, C++, JavaScript, etc.)

## Installation

No external dependencies required! Just use Python 3.6+.

```bash
# Clone or download the repository
# No pip install needed - it's a standalone module
```

## Quick Start

### Basic Usage

```python
from copyright_extractor import CopyrightExtractor

# Create an extractor instance
extractor = CopyrightExtractor()

# Sample text with various copyright formats
text = """
copyright 2023 John Doe
COPYRIGHT 2022 Jane Smith
© 2021 ACME Corp
(c) 2020 Test Company
"""

# Extract copyrights
results = extractor.extract_from_text(text)

# Display results
print(extractor.format_results(results))
```

### Convenience Functions

```python
from copyright_extractor import extract_copyright, extract_copyright_from_file

# Extract from text (returns list of statements)
statements = extract_copyright("copyright 2023 Example")

# Extract from file
statements = extract_copyright_from_file("myfile.py")
```

## Usage Examples

### 1. Extract from Text

```python
from copyright_extractor import CopyrightExtractor

text = """
This file is copyright 2023 by John Doe
© 2022 Another Company
(C) 2021-2023 Third Corp
"""

extractor = CopyrightExtractor()
results = extractor.extract_from_text(text)

for result in results:
    print(f"Line {result['line_number']}: {result['statement']}")
```

### 2. Extract from a File

```python
from copyright_extractor import CopyrightExtractor

extractor = CopyrightExtractor()
results = extractor.extract_from_file("example.py")

print(extractor.format_results(results))
```

### 3. Search a Directory

```python
from copyright_extractor import CopyrightExtractor

extractor = CopyrightExtractor()

# Search all Python files
results = extractor.search_directory(".", pattern="**/*.py")

for file_path, copyrights in results.items():
    print(f"\n{file_path}:")
    for cr in copyrights:
        print(f"  Line {cr['line_number']}: {cr['statement']}")
```

### 4. Get Unique Statements

```python
from copyright_extractor import CopyrightExtractor

text = """
copyright 2023 Company A
copyright 2023 Company A
copyright 2022 Company B
"""

extractor = CopyrightExtractor()
extractor.extract_from_text(text)

# Get unique statements (removes duplicates)
unique = extractor.get_unique_statements()
print(f"Found {len(unique)} unique copyrights")
```

### 5. Detailed Information

```python
from copyright_extractor import CopyrightExtractor

extractor = CopyrightExtractor()
results = extractor.extract_from_text("copyright 2023 Test")

for result in results:
    print(f"Statement: {result['statement']}")
    print(f"Line: {result['line_number']}")
    print(f"Start Position: {result['start_pos']}")
    print(f"End Position: {result['end_pos']}")
```

## API Reference

### `CopyrightExtractor` Class

#### Methods

**`extract_from_text(text: str) -> List[Dict]`**

Extract copyright statements from text.

Returns a list of dictionaries containing:
- `statement`: The full copyright statement
- `line_number`: The line number where it was found
- `start_pos`: Starting position in the line
- `end_pos`: Ending position in the line

**`extract_from_file(file_path: Union[str, Path]) -> List[Dict]`**

Extract copyrights from a file.

Raises:
- `FileNotFoundError`: If file doesn't exist
- `IsADirectoryError`: If path is a directory

**`search_directory(directory: Union[str, Path], pattern: str = "**/*", exclude_dirs: List[str] = None) -> Dict[str, List[Dict]]`**

Search a directory for copyrights.

Parameters:
- `directory`: Directory to search
- `pattern`: Glob pattern for files (default: all files)
- `exclude_dirs`: List of directories to exclude (default: .git, __pycache__, etc.)

Returns:
- Dictionary mapping file paths to their copyright statements

**`get_unique_statements() -> List[str]`**

Get unique copyright statements from last extraction.

**`format_results(results: List[Dict] = None) -> str`**

Format results as a readable string.

### Convenience Functions

**`extract_copyright(text: str) -> List[str]`**

Extract copyrights from text, returns list of statements only.

**`extract_copyright_from_file(file_path: Union[str, Path]) -> List[str]`**

Extract copyrights from file, returns list of statements only.

## Running the Demo

```bash
python demo.py
```

This will run comprehensive demonstrations of all features.

## Running Tests

```bash
# Install pytest if you don't have it
pip install pytest

# Run all tests
pytest tests/test_copyright_extractor.py -v

# Run specific test
pytest tests/test_copyright_extractor.py::TestCopyrightExtractor::test_lowercase_copyright -v
```

## Test Coverage

The test suite includes comprehensive tests for:

- ✅ Lowercase copyright
- ✅ Uppercase COPYRIGHT
- ✅ Mixed case (CopyRight, copyRight, etc.)
- ✅ Unicode © symbol
- ✅ (c) and (C) notations
- ✅ Year ranges (2020-2023)
- ✅ Multiple years (2020, 2021, 2022)
- ✅ No year
- ✅ Line number tracking
- ✅ Multiple copyrights in one text
- ✅ File operations
- ✅ Directory searching
- ✅ UTF-8 encoding
- ✅ Code comments
- ✅ Edge cases

## Examples

### Example 1: Extract from Python Source

```python
from copyright_extractor import extract_copyright_from_file

copyrights = extract_copyright_from_file("myproject.py")
for copyright in copyrights:
    print(copyright)
```

### Example 2: Batch Process Multiple Files

```python
from copyright_extractor import CopyrightExtractor
from pathlib import Path

extractor = CopyrightExtractor()

for py_file in Path(".").glob("**/*.py"):
    results = extractor.extract_from_file(py_file)
    if results:
        print(f"\n{py_file}:")
        for r in results:
            print(f"  {r['statement']}")
```

### Example 3: Find All Unique Copyrights in a Project

```python
from copyright_extractor import CopyrightExtractor

extractor = CopyrightExtractor()
all_copyrights = set()

results = extractor.search_directory(".", pattern="**/*.py")
for file_path, copyrights in results.items():
    for cr in copyrights:
        all_copyrights.add(cr['statement'])

print(f"Found {len(all_copyrights)} unique copyrights:")
for cr in sorted(all_copyrights):
    print(f"  - {cr}")
```

## Real-World Use Cases

1. **License Auditing**: Scan your codebase to inventory all copyright statements
2. **Compliance**: Verify that all files have appropriate copyright notices
3. **Migration**: Update copyright years across multiple files
4. **Documentation**: Generate a list of copyright holders for your project
5. **Legal Review**: Extract all copyright information for legal team review

## Notes

- The extractor is case-insensitive for the word "copyright"
- It handles multiple formats of year specification
- Binary files are automatically skipped when searching directories
- UTF-8 encoding is used for file reading with error handling
- The regex pattern is optimized for accuracy and performance

## License

This module is provided as-is for copyright extraction purposes.

## Support

For issues or questions, please refer to the test files for usage examples or examine the source code documentation.

## Version

Current version: 1.0.0

## Author

Created for comprehensive copyright extraction needs.
