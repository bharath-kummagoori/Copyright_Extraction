#!/usr/bin/env python3
"""
Copyright and License Detection Module
Core detection logic without GUI dependencies
"""

import re
from typing import List, Set
from pathlib import Path


# ==================== COPYRIGHT & LICENSE DETECTION ====================

class CopyrightLicenseDetector:
    """Detects copyright and license information in text."""

    # Copyright patterns - case insensitive, multiple formats
    COPYRIGHT_PATTERNS = [
        re.compile(r'copyright\s*(?:\(c\)|\©|\xA9|©)?\s*(?:\d{4}[-–,\s]*)+', re.IGNORECASE),
        re.compile(r'(?:\(c\)|\©|\xA9|©)\s*(?:\d{4}[-–,\s]*)+', re.IGNORECASE),
        re.compile(r'copr\.\s*(?:\d{4}[-–,\s]*)+', re.IGNORECASE),
        re.compile(r'copyright(?:\s+\(c\)|\s+©|\s+\xA9)?\s+', re.IGNORECASE),
        re.compile(r'SPDX-FileCopyrightText:\s*(.+)', re.IGNORECASE),
    ]

    # License patterns with SPDX identifiers
    LICENSE_PATTERNS = {
        'MIT': [
            re.compile(r'MIT\s+Licen[cs]e', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*MIT', re.IGNORECASE),
            re.compile(r'Permission is hereby granted, free of charge', re.IGNORECASE),
        ],
        'Apache-2.0': [
            re.compile(r'Apache\s+Licen[cs]e[,\s]+Version\s+2\.0', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*Apache-2\.0', re.IGNORECASE),
            re.compile(r'Licensed under the Apache License', re.IGNORECASE),
        ],
        'GPL-2.0': [
            re.compile(r'GNU\s+General\s+Public\s+Licen[cs]e[,\s]+[Vv]ersion\s+2', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*GPL-2\.0', re.IGNORECASE),
            re.compile(r'GPL\s*v?2', re.IGNORECASE),
        ],
        'GPL-3.0': [
            re.compile(r'GNU\s+General\s+Public\s+Licen[cs]e[,\s]+[Vv]ersion\s+3', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*GPL-3\.0', re.IGNORECASE),
            re.compile(r'GPL\s*v?3', re.IGNORECASE),
        ],
        'LGPL-2.1': [
            re.compile(r'GNU\s+Lesser\s+General\s+Public\s+Licen[cs]e[,\s]+[Vv]ersion\s+2\.1', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*LGPL-2\.1', re.IGNORECASE),
        ],
        'LGPL-3.0': [
            re.compile(r'GNU\s+Lesser\s+General\s+Public\s+Licen[cs]e[,\s]+[Vv]ersion\s+3', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*LGPL-3\.0', re.IGNORECASE),
        ],
        'BSD-2-Clause': [
            re.compile(r'BSD\s+2-Clause', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*BSD-2-Clause', re.IGNORECASE),
            re.compile(r'Redistribution and use in source and binary forms.*2\s+clause', re.IGNORECASE | re.DOTALL),
        ],
        'BSD-3-Clause': [
            re.compile(r'BSD\s+3-Clause', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*BSD-3-Clause', re.IGNORECASE),
            re.compile(r'Redistribution and use in source and binary forms.*3\s+clause', re.IGNORECASE | re.DOTALL),
        ],
        'ISC': [
            re.compile(r'ISC\s+Licen[cs]e', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*ISC', re.IGNORECASE),
            re.compile(r'Permission to use, copy, modify.*ISC', re.IGNORECASE | re.DOTALL),
        ],
        'MPL-2.0': [
            re.compile(r'Mozilla\s+Public\s+Licen[cs]e[,\s]+[Vv]ersion\s+2\.0', re.IGNORECASE),
            re.compile(r'SPDX-License-Identifier:\s*MPL-2\.0', re.IGNORECASE),
        ],
    }

    # Junk patterns to filter out
    JUNK_PATTERNS = [
        re.compile(r'Copyright\s+\(C\)\s+YEAR', re.IGNORECASE),  # Templates with YEAR placeholder
        re.compile(r'Copyright\s+\(C\)\s+<year>\s+<name of author>', re.IGNORECASE),
        re.compile(r'Copyright.*put your company.*here', re.IGNORECASE),
        re.compile(r'Copyright.*YOUR NAME.*YOUR EMAIL', re.IGNORECASE),
        re.compile(r'^[\s\*\#\-\/]*$'),  # Only whitespace and comment chars
    ]

    @staticmethod
    def detect_copyrights(text: str) -> List[str]:
        """
        Detect copyright notices in text.

        Args:
            text: The text to scan

        Returns:
            List of copyright strings found
        """
        copyrights = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            # Check if line contains copyright
            for pattern in CopyrightLicenseDetector.COPYRIGHT_PATTERNS:
                if pattern.search(line):
                    # Extract copyright statement (current line + possibly next lines)
                    copyright_text = line.strip()

                    # Check if we need to merge with next lines
                    # (for multi-line copyright statements)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # If next line looks like continuation (no copyright keyword)
                        if next_line and not any(p.search(next_line) for p in CopyrightLicenseDetector.COPYRIGHT_PATTERNS):
                            # Check if ends with incomplete year, comma, or "by"
                            if re.search(r'\d{1,3}$|,$|\bby$', copyright_text, re.IGNORECASE):
                                copyright_text += ' ' + next_line

                    # Clean the text
                    copyright_text = CopyrightLicenseDetector._clean_copyright(copyright_text)

                    # Validate and add
                    if copyright_text and not CopyrightLicenseDetector._is_junk(copyright_text):
                        if copyright_text not in copyrights:
                            copyrights.append(copyright_text)
                    break

        return copyrights

    @staticmethod
    def detect_licenses(text: str) -> Set[str]:
        """
        Detect license types in text.

        Args:
            text: The text to scan

        Returns:
            Set of license identifiers found
        """
        licenses = set()

        for license_name, patterns in CopyrightLicenseDetector.LICENSE_PATTERNS.items():
            for pattern in patterns:
                if pattern.search(text):
                    licenses.add(license_name)
                    break

        return licenses

    @staticmethod
    def _clean_copyright(text: str) -> str:
        """Clean copyright text by removing artifacts."""
        # Remove comment characters
        text = re.sub(r'^[\s\*\#\-\/]+', '', text)
        text = re.sub(r'[\s\*\#\-\/]+$', '', text)

        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove common prefixes/suffixes
        text = re.sub(r'^\s*[\*\#\-\/]+\s*', '', text)
        text = re.sub(r'\s*\*+\/\s*$', '', text)

        return text.strip()

    @staticmethod
    def _is_junk(text: str) -> bool:
        """Check if copyright text is junk/template."""
        if len(text) < 10:
            return True

        for pattern in CopyrightLicenseDetector.JUNK_PATTERNS:
            if pattern.search(text):
                return True

        return False


# Supported text file extensions
TEXT_EXTENSIONS = {
    # Source code
    '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.js', '.ts', '.jsx', '.tsx',
    '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.m', '.mm',
    '.sh', '.bash', '.zsh', '.pl', '.pm', '.lua', '.r',

    # Web
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml', '.xsl', '.xsd',
    '.svg', '.vue', '.jsp', '.asp', '.aspx',

    # Config & Data
    '.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.properties',
    '.gradle', '.maven', '.pom',

    # Documentation
    '.txt', '.md', '.rst', '.adoc', '.tex',

    # Build & Package
    '.makefile', '.cmake', '.mk', '.am', '.ac',

    # License files (no extension)
    '', '.license', '.notice', '.copying'
}

# Files to always check (case-insensitive)
IMPORTANT_FILENAMES = {
    'license', 'license.txt', 'license.md',
    'copying', 'copying.txt', 'copying.md',
    'notice', 'notice.txt', 'notice.md',
    'copyright', 'copyright.txt', 'copyright.md',
    'readme', 'readme.txt', 'readme.md',
    'authors', 'contributors'
}


def should_process_file(filepath: str) -> tuple:
    """
    Check if file should be processed.

    Returns:
        (should_process, reason)
    """
    path = Path(filepath)
    filename_lower = path.name.lower()

    # Check if important file (LICENSE, README, etc.)
    if filename_lower in IMPORTANT_FILENAMES:
        return True, "Important file"

    # Check extension
    ext = path.suffix.lower()
    if ext not in TEXT_EXTENSIONS:
        return False, f"Unsupported extension: {ext}"

    return True, "OK"
