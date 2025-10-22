# Copyright & License Extraction Tool

**Single-file, complete solution for extracting copyright and license information from source code.**

## 🚀 Quick Start

```bash
# Install dependency
pip install xlsxwriter

# Run the tool
python copyright_extraction_tool.py
```

That's it! Just run one file.

## ✨ Phase 1 Features (All Included)

1. **✅ Case-Insensitive Copyright Detection**
   - Supports: `Copyright`, `copyright`, `COPYRIGHT`
   - Symbols: `©`, `(c)`, `(C)`, `Copr.`
   - SPDX format: `SPDX-FileCopyrightText:`

2. **✅ Smart File Filtering**
   - Only processes text files (50+ extensions)
   - Skips binaries, images, archives
   - Auto-detects LICENSE, README files
   - Ignores build folders (node_modules, .git, etc.)

3. **✅ Progress Bar + Cancel Button**
   - Real-time progress updates
   - Shows current file being scanned
   - Cancel anytime

4. **✅ Error Handling + Logging**
   - Detailed log files
   - Multiple encoding support
   - Graceful error recovery

5. **✅ License Detection**
   - MIT, Apache, GPL, LGPL, BSD, ISC, MPL
   - SPDX identifiers
   - Pattern matching

## 📖 How to Use

1. **Run the tool:**
   ```bash
   python copyright_extraction_tool.py
   ```

2. **In the GUI:**
   - Click "Browse" next to **Output Directory** - select where to save Excel file
   - Click "Browse" next to **Source Directory** - select code to scan
   - Click **"Start Scan"**
   - Wait for completion (watch progress bar)

3. **Results:**
   - Excel file: `copyright_extraction_YYYYMMDD_HHMMSS.xlsx`
   - Log file: `copyright_extraction_YYYYMMDD_HHMMSS.log`
   - Both saved in output directory

## 📊 Output Format

Excel file with 4 columns:

| Column | Description |
|--------|-------------|
| File/Folder Path | Relative path from source directory |
| Folder Name | Top-level folder name |
| Copyrights | All copyright notices (one per line) |
| Licenses | Detected license types (comma-separated) |

## 🎯 Supported File Types

**Source Code:** `.py`, `.java`, `.c`, `.cpp`, `.h`, `.js`, `.ts`, `.php`, `.rb`, `.go`, `.rs`, `.swift`, etc.

**Web:** `.html`, `.css`, `.xml`, `.svg`, `.vue`, `.jsp`

**Config:** `.json`, `.yaml`, `.ini`, `.conf`, `.toml`

**Docs:** `.txt`, `.md`, `.rst`

**Special:** `LICENSE`, `COPYING`, `NOTICE`, `README` (no extension)

## 🔍 Detection Examples

### Copyrights
```
✅ Copyright 2023 John Doe
✅ copyright (c) 2020-2023 ACME Corp
✅ © 2023 Example Inc.
✅ (C) 2023 Developer
✅ Copr. 2023 Company
✅ SPDX-FileCopyrightText: 2023 Org
```

### Licenses
```
✅ MIT License
✅ Apache License, Version 2.0
✅ GNU General Public License v3
✅ BSD 3-Clause
✅ SPDX-License-Identifier: MIT
```

## ⚙️ Configuration

Edit these constants in `copyright_extraction_tool.py`:

```python
# Max file size (default 10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Directories to skip
SKIP_DIRECTORIES = {
    '.git', 'node_modules', '__pycache__', 'build'
}

# Add more file extensions
TEXT_EXTENSIONS = {
    '.py', '.java', '.c', ...
}
```

## 🐛 Troubleshooting

**"No module named 'xlsxwriter'"**
```bash
pip install xlsxwriter
```

**"No module named 'tkinter'" (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**UI freezes / Not responding**
- This is normal during scan startup
- UI becomes responsive once progress bar starts
- Use "Cancel" button if needed

## 📝 Files

- **`copyright_extraction_tool.py`** - Main file (single file, ~700 lines)
- **`test_phase1_improvements.py`** - Test suite (optional)
- **`requirements.txt`** - Just `xlsxwriter`

## 🎓 Comparison with Original

| Feature | Original | New (Phase 1) |
|---------|----------|---------------|
| Copyright Detection | "Copyright" only | ©, (c), case-insensitive |
| License Detection | ❌ | ✅ 8+ types |
| File Filtering | All files | Text only |
| Progress | ❌ | ✅ Real-time |
| Cancel | ❌ | ✅ |
| Logging | Print statements | Full logs |
| Multi-threaded | ❌ | ✅ |

## 📄 License

GPLv3

## 🙏 Credits

Improved version with Phase 1 features by Claude Code
