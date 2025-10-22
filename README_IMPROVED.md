# Copyright & License Extraction Tool - Phase 1 Improved

An improved GUI tool for extracting copyright and license information from source code directories.

## 🎯 Phase 1 Improvements

### ✅ What's New

1. **Case-Insensitive Matching**
   - Detects `Copyright`, `copyright`, `COPYRIGHT`
   - Supports copyright symbols: `©`, `(c)`, `(C)`
   - Recognizes `Copr.` abbreviation
   - Handles SPDX format: `SPDX-FileCopyrightText:`

2. **Smart File Extension Filtering**
   - Only processes text-based files (source code, configs, docs)
   - Skips binary files (executables, images, archives)
   - Always checks important files (LICENSE, README, COPYING)
   - Configurable file size limit (10MB by default)
   - Auto-skips common directories (node_modules, .git, build, etc.)

3. **Progress Bar with Cancel Button**
   - Real-time progress updates
   - Shows current file being processed
   - Cancel button to stop scan at any time
   - Multi-threaded scanning (GUI stays responsive)

4. **Comprehensive Error Handling & Logging**
   - Detailed log files with timestamps
   - Categorized errors (encoding, access denied, etc.)
   - Multiple encoding attempts (UTF-8, Latin-1, CP1252)
   - Graceful failure handling
   - Session summary statistics

5. **License Detection**
   - Detects common licenses: MIT, Apache, GPL, LGPL, BSD, ISC, MPL
   - SPDX identifier recognition
   - License text pattern matching
   - Exports licenses alongside copyrights

## 📋 Requirements

```bash
pip install -r requirements_improved.txt
```

## 🚀 Usage

### GUI Mode

```bash
python copyright_extraction_improved.py
```

1. Click "Browse" to select **Output Directory** (where Excel file will be saved)
2. Click "Browse" to select **Source Directory** (code to scan)
3. Click "Start Scan"
4. Monitor progress in real-time
5. Click "Cancel" if needed
6. Results saved to timestamped Excel file

### Output Format

Excel file with columns:
- **File/Folder Path**: Relative path from source directory
- **Folder Name**: Top-level folder name
- **Copyrights**: All copyright notices found (one per line)
- **Licenses**: Detected license types (comma-separated)

## 📊 Supported File Types

### Source Code
`.py`, `.java`, `.c`, `.cpp`, `.h`, `.js`, `.ts`, `.php`, `.rb`, `.go`, `.rs`, `.swift`, `.kt`, `.scala`, etc.

### Web Files
`.html`, `.css`, `.xml`, `.svg`, `.vue`, `.jsp`, `.asp`

### Configuration
`.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.conf`, `.properties`

### Documentation
`.txt`, `.md`, `.rst`, `.adoc`, `.tex`

### Special Files
`LICENSE`, `COPYING`, `NOTICE`, `README`, `AUTHORS` (no extension required)

## 🔍 Detection Examples

### Copyrights Detected ✅
```
Copyright 2023 John Doe
Copyright (C) 2020-2023 ACME Corp
© 2023 Example Inc.
(c) 2023 Developer Name
Copr. 2023 Company
SPDX-FileCopyrightText: 2023 Organization
```

### Licenses Detected ✅
```
MIT License
Apache License, Version 2.0
GNU General Public License, Version 2.0
GNU General Public License, Version 3.0
BSD 2-Clause License
BSD 3-Clause License
ISC License
Mozilla Public License, Version 2.0
SPDX-License-Identifier: MIT
```

## 📁 Directory Structure

```
Copyright_Extraction/
├── copyright_extraction_improved.py    # Main improved tool
├── README_IMPROVED.md                  # This file
├── requirements_improved.txt           # Dependencies
└── logs/                               # Auto-generated logs
    └── copyright_extraction_YYYYMMDD_HHMMSS.log
```

## 🎨 GUI Features

- **Modern Interface**: Clean, intuitive design
- **Browse Buttons**: Easy directory selection
- **Progress Bar**: Visual feedback during scan
- **Real-time Status**: Shows current file being processed
- **Results Panel**: Scrollable results area with summary
- **Cancel Support**: Stop scan at any time
- **Thread-safe**: Non-blocking UI during scan

## 📝 Logging

Each scan creates a detailed log file:
- Timestamp for each operation
- Files processed count
- Errors with stack traces
- Session summary statistics
- Saved to output directory

Example log:
```
2023-10-22 14:30:15 - INFO - Counting files in /path/to/source...
2023-10-22 14:30:16 - INFO - Found 1523 text files to process
2023-10-22 14:30:45 - INFO - Processed 100/1523 files, found 45 with copyright/license
2023-10-22 14:31:30 - WARNING - Could not decode /path/to/file.bin
2023-10-22 14:35:20 - INFO - Scan complete!
2023-10-22 14:35:20 - INFO -   Files processed: 1523
2023-10-22 14:35:20 - INFO -   Files with copyright/license: 456
```

## 🛡️ Error Handling

The tool gracefully handles:
- **Encoding Issues**: Tries multiple encodings (UTF-8, Latin-1, CP1252)
- **Access Denied**: Logs and continues
- **Binary Files**: Automatically skipped
- **Large Files**: Size limit prevents memory issues
- **Corrupted Files**: Caught and logged
- **Network Drives**: Supported with timeout handling

## 🔧 Configuration

Edit these constants in the code to customize:

```python
# File size limit (default 10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Directories to skip
SKIP_DIRECTORIES = {
    '.git', 'node_modules', '__pycache__', 'build', 'dist'
}

# Add more file extensions
TEXT_EXTENSIONS = {
    '.py', '.java', '.c', '.cpp', '.js', ...
}
```

## 📈 Performance

- **Multi-threaded**: Scanning doesn't block UI
- **Smart Filtering**: Only processes text files
- **Memory Efficient**: Streams large files
- **Progress Updates**: Every file (throttled for performance)
- **Typical Speed**: 100-500 files/second (depends on file size and content)

## 🐛 Known Limitations

1. **Archives**: Does not extract `.zip`, `.tar`, `.jar` files (Phase 2 feature)
2. **PDF Files**: Not supported yet (Phase 2 feature)
3. **Office Docs**: `.docx`, `.xlsx` not supported (Phase 2 feature)
4. **Binary Metadata**: Does not read metadata from executables (Phase 2 feature)

## 🆚 Comparison: Old vs New

| Feature | Old Version | New Version |
|---------|-------------|-------------|
| Copyright Detection | "Copyright" only | Case-insensitive, ©, (c), Copr. |
| License Detection | ❌ None | ✅ 8+ license types |
| File Filtering | ❌ Processes all files | ✅ Text files only |
| Progress Bar | ❌ No feedback | ✅ Real-time progress |
| Cancel Button | ❌ No | ✅ Yes |
| Error Handling | Basic try/except | Comprehensive logging |
| Logging | Print statements | Detailed log files |
| UI Responsiveness | Freezes during scan | Multi-threaded |
| Multi-line Copyright | Buggy (index issue) | Fixed |
| Encoding Support | UTF-8 only | 4 encodings |

## 🔜 Coming in Phase 2

- Archive extraction (.zip, .tar, .jar)
- PDF parsing
- Office document support
- Multi-threading for parallel file processing
- SBOM generation (SPDX format)
- Comparison reports
- CLI mode for automation
- Advanced deduplication

## 📞 Support

For issues or questions, refer to the main project README.

## 📄 License

This tool is licensed under GPLv3.
