#!/usr/bin/env python3
"""
Copyright & License Extraction Tool - Phase 1 Complete
Single unified file with all improvements

Phase 1 Features:
✅ Case-insensitive copyright matching (©, (c), Copyright, etc.)
✅ Smart file extension filtering (text files only)
✅ Progress bar with cancel button
✅ Comprehensive error handling and logging
✅ License detection (MIT, GPL, Apache, BSD, etc.)

Usage:
    python copyright_extraction_tool.py

Author: Improved by Claude Code
Version: 2.0
"""

import re
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List, Tuple, Optional
import threading
import xlsxwriter
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ==================== CONFIGURATION ====================

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

# Directories to skip
SKIP_DIRECTORIES = {
    '.git', '.svn', '.hg', '.bzr',
    'node_modules', '__pycache__', '.pytest_cache',
    'build', 'dist', 'target', 'bin', 'obj',
    '.idea', '.vscode', '.vs',
    'vendor', 'deps', 'bower_components'
}

# Maximum file size to process (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


# ==================== LOGGING SETUP ====================

def setup_logging(output_dir: str) -> logging.Logger:
    """Setup logging configuration."""
    log_file = os.path.join(output_dir, f"copyright_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('CopyrightExtractor')
    logger.info("=" * 80)
    logger.info("Copyright Extraction Tool - Session Started")
    logger.info("=" * 80)

    return logger


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


# ==================== FILE SCANNER ====================

class FileScanner:
    """Scans files for copyright and license information."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.detector = CopyrightLicenseDetector()
        self.cancelled = False

    def should_process_file(self, filepath: str) -> Tuple[bool, str]:
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

        # Check file size
        try:
            if os.path.getsize(filepath) > MAX_FILE_SIZE:
                return False, f"File too large (>{MAX_FILE_SIZE/1024/1024}MB)"
        except OSError as e:
            return False, f"Cannot access file: {e}"

        return True, "OK"

    def scan_file(self, filepath: str) -> Optional[Dict]:
        """
        Scan a single file for copyright and license info.

        Returns:
            Dict with keys: filepath, folder_name, copyrights, licenses
            or None if file cannot be processed
        """
        try:
            # Read file with multiple encoding attempts
            content = None
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    self.logger.warning(f"Error reading {filepath}: {e}")
                    return None

            if content is None:
                self.logger.warning(f"Could not decode {filepath}")
                return None

            # Detect copyrights and licenses
            copyrights = self.detector.detect_copyrights(content)
            licenses = self.detector.detect_licenses(content)

            # Only return if we found something
            if copyrights or licenses:
                return {
                    'filepath': filepath,
                    'copyrights': copyrights,
                    'licenses': licenses
                }

            return None

        except Exception as e:
            self.logger.error(f"Error scanning {filepath}: {e}", exc_info=True)
            return None

    def scan_directory(self, root_path: str, progress_callback=None) -> List[Dict]:
        """
        Scan directory recursively.

        Args:
            root_path: Root directory to scan
            progress_callback: Function to call with progress updates
                             (current_file, files_processed, total_files)

        Returns:
            List of results (each result is a dict from scan_file)
        """
        results = []

        # First pass: count files
        self.logger.info(f"Counting files in {root_path}...")
        all_files = []

        for root, dirs, files in os.walk(root_path):
            # Remove skip directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]

            for filename in files:
                filepath = os.path.join(root, filename)
                should_process, reason = self.should_process_file(filepath)

                if should_process:
                    all_files.append(filepath)

        total_files = len(all_files)
        self.logger.info(f"Found {total_files} text files to process")

        # Second pass: process files
        files_processed = 0
        files_with_copyright = 0

        for filepath in all_files:
            if self.cancelled:
                self.logger.info("Scan cancelled by user")
                break

            files_processed += 1

            # Update progress
            if progress_callback:
                progress_callback(filepath, files_processed, total_files)

            # Scan file
            result = self.scan_file(filepath)
            if result:
                results.append(result)
                files_with_copyright += 1

            if files_processed % 100 == 0:
                self.logger.info(f"Processed {files_processed}/{total_files} files, found {files_with_copyright} with copyright/license")

        self.logger.info("=" * 80)
        self.logger.info(f"Scan complete!")
        self.logger.info(f"  Files processed: {files_processed}")
        self.logger.info(f"  Files with copyright/license: {files_with_copyright}")
        self.logger.info(f"  Files without: {files_processed - files_with_copyright}")
        self.logger.info("=" * 80)

        return results

    def cancel(self):
        """Cancel ongoing scan."""
        self.cancelled = True


# ==================== EXCEL EXPORT ====================

def export_to_excel(results: List[Dict], output_path: str, root_path: str, logger: logging.Logger):
    """Export results to Excel file."""
    logger.info(f"Exporting results to {output_path}")

    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet("Copyright Extraction")

    # Formats
    bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
    wrap = workbook.add_format({'text_wrap': True, 'valign': 'top'})

    # Headers
    worksheet.write('A1', 'File/Folder Path', bold)
    worksheet.write('B1', 'Folder Name', bold)
    worksheet.write('C1', 'Copyrights', bold)
    worksheet.write('D1', 'Licenses', bold)
    worksheet.autofilter('A1:D1')

    # Set column widths
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 60)
    worksheet.set_column('D:D', 30)

    row = 1
    for result in results:
        filepath = result['filepath']

        # Get relative path and folder name
        rel_path = os.path.relpath(filepath, root_path)
        folder_name = Path(rel_path).parts[0] if Path(rel_path).parts else ""

        # Join copyrights and licenses
        copyrights_text = '\n'.join(result['copyrights'])
        licenses_text = ', '.join(sorted(result['licenses']))

        worksheet.write(row, 0, rel_path)
        worksheet.write(row, 1, folder_name)
        worksheet.write(row, 2, copyrights_text, wrap)
        worksheet.write(row, 3, licenses_text, wrap)

        row += 1

    workbook.close()
    logger.info(f"Exported {row - 1} entries to Excel")


# ==================== GUI APPLICATION ====================

class CopyrightExtractionGUI:
    """GUI for copyright extraction."""

    def __init__(self, win):
        self.window = win
        self.logger = None
        self.scanner = None
        self.scan_thread = None

        # Variables
        self.output_path = StringVar()
        self.source_path = StringVar()
        self.is_scanning = False

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build the user interface."""
        # Title
        title = Label(
            self.window,
            text="COPYRIGHT & LICENSE EXTRACTION TOOL",
            font=('Arial', 14, 'bold'),
            bg="light blue",
            fg="navy"
        )
        title.pack(pady=10)

        # Version info
        version = Label(
            self.window,
            text="Phase 1 Complete - v2.0 | All features in single file",
            font=('Arial', 9),
            bg="light blue",
            fg="gray"
        )
        version.pack()

        # Main frame
        main_frame = Frame(self.window, bg="light blue")
        main_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

        # Output path
        Label(
            main_frame,
            text="Output Directory:",
            font=('Arial', 10),
            bg="light blue"
        ).grid(row=0, column=0, sticky=W, pady=5)

        Entry(
            main_frame,
            textvariable=self.output_path,
            width=50,
            font=('Arial', 9)
        ).grid(row=0, column=1, padx=5, pady=5)

        Button(
            main_frame,
            text="Browse",
            command=self._browse_output,
            width=10
        ).grid(row=0, column=2, padx=5, pady=5)

        # Source path
        Label(
            main_frame,
            text="Source Directory:",
            font=('Arial', 10),
            bg="light blue"
        ).grid(row=1, column=0, sticky=W, pady=5)

        Entry(
            main_frame,
            textvariable=self.source_path,
            width=50,
            font=('Arial', 9)
        ).grid(row=1, column=1, padx=5, pady=5)

        Button(
            main_frame,
            text="Browse",
            command=self._browse_source,
            width=10
        ).grid(row=1, column=2, padx=5, pady=5)

        # Progress frame
        progress_frame = Frame(self.window, bg="light blue")
        progress_frame.pack(padx=20, pady=10, fill=X)

        # Progress bar
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=500
        )
        self.progress.pack(pady=5)

        # Status label
        self.status_label = Label(
            progress_frame,
            text="Ready to scan...",
            font=('Arial', 9),
            bg="light blue",
            fg="blue"
        )
        self.status_label.pack(pady=5)

        # Buttons frame
        button_frame = Frame(self.window, bg="light blue")
        button_frame.pack(pady=10)

        self.scan_button = Button(
            button_frame,
            text="Start Scan",
            command=self._start_scan,
            width=12,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=('Arial', 10, 'bold')
        )
        self.scan_button.pack(side=LEFT, padx=5)

        self.cancel_button = Button(
            button_frame,
            text="Cancel",
            command=self._cancel_scan,
            width=12,
            height=2,
            bg="#f44336",
            fg="white",
            font=('Arial', 10, 'bold'),
            state=DISABLED
        )
        self.cancel_button.pack(side=LEFT, padx=5)

        Button(
            button_frame,
            text="Clear",
            command=self._clear_all,
            width=12,
            height=2,
            bg="#2196F3",
            fg="white",
            font=('Arial', 10, 'bold')
        ).pack(side=LEFT, padx=5)

        # Results text area
        results_frame = Frame(self.window, bg="light blue")
        results_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

        Label(
            results_frame,
            text="Results:",
            font=('Arial', 10, 'bold'),
            bg="light blue"
        ).pack(anchor=W)

        # Scrollbar
        scrollbar = Scrollbar(results_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.results_text = Text(
            results_frame,
            height=10,
            width=80,
            bg="white",
            fg="black",
            font=('Courier', 9),
            yscrollcommand=scrollbar.set
        )
        self.results_text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)

    def _browse_output(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_path.set(directory)

    def _browse_source(self):
        """Browse for source directory."""
        directory = filedialog.askdirectory(title="Select Source Directory to Scan")
        if directory:
            self.source_path.set(directory)

    def _clear_all(self):
        """Clear all fields."""
        self.output_path.set("")
        self.source_path.set("")
        self.results_text.delete(1.0, END)
        self.status_label.config(text="Ready to scan...", fg="blue")
        self.progress['value'] = 0

    def _validate_inputs(self) -> bool:
        """Validate user inputs."""
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output directory")
            return False

        if not self.source_path.get():
            messagebox.showerror("Error", "Please select a source directory to scan")
            return False

        if not os.path.isdir(self.output_path.get()):
            messagebox.showerror("Error", "Output directory does not exist")
            return False

        if not os.path.isdir(self.source_path.get()):
            messagebox.showerror("Error", "Source directory does not exist")
            return False

        return True

    def _start_scan(self):
        """Start the scanning process."""
        if not self._validate_inputs():
            return

        if self.is_scanning:
            messagebox.showwarning("Warning", "Scan already in progress")
            return

        # Setup
        self.is_scanning = True
        self.scan_button.config(state=DISABLED)
        self.cancel_button.config(state=NORMAL)
        self.results_text.delete(1.0, END)
        self.progress['value'] = 0

        # Setup logging
        self.logger = setup_logging(self.output_path.get())
        self.scanner = FileScanner(self.logger)

        # Start scan in separate thread
        self.scan_thread = threading.Thread(target=self._run_scan, daemon=True)
        self.scan_thread.start()

    def _run_scan(self):
        """Run the scan (called in separate thread)."""
        try:
            source_dir = self.source_path.get()
            output_dir = self.output_path.get()

            self._update_status("Scanning files...", "blue")

            # Scan directory
            results = self.scanner.scan_directory(
                source_dir,
                progress_callback=self._update_progress
            )

            if self.scanner.cancelled:
                self._update_status("Scan cancelled", "orange")
                self._append_result("\n❌ Scan was cancelled by user\n")
            else:
                # Export to Excel
                self._update_status("Exporting to Excel...", "blue")
                output_file = os.path.join(output_dir, f"copyright_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                export_to_excel(results, output_file, source_dir, self.logger)

                # Show success
                self._update_status("Scan completed successfully!", "green")
                self._append_result(f"\n✅ Scan Complete!\n")
                self._append_result(f"   Files processed: {len(results)}\n")
                self._append_result(f"   Output file: {output_file}\n")

                messagebox.showinfo(
                    "Success",
                    f"Copyright extraction completed!\n\n"
                    f"Files with copyright/license: {len(results)}\n"
                    f"Output: {output_file}"
                )

        except Exception as e:
            self.logger.error(f"Scan failed: {e}", exc_info=True)
            self._update_status(f"Error: {str(e)}", "red")
            self._append_result(f"\n❌ Error: {str(e)}\n")
            messagebox.showerror("Error", f"Scan failed:\n{str(e)}")

        finally:
            # Reset UI
            self.is_scanning = False
            self.window.after(0, self._reset_buttons)

    def _cancel_scan(self):
        """Cancel ongoing scan."""
        if self.scanner:
            self.scanner.cancel()
            self.cancel_button.config(state=DISABLED)
            self._update_status("Cancelling...", "orange")

    def _reset_buttons(self):
        """Reset button states (must be called from main thread)."""
        self.scan_button.config(state=NORMAL)
        self.cancel_button.config(state=DISABLED)
        self.progress['value'] = 100

    def _update_progress(self, current_file: str, processed: int, total: int):
        """Update progress bar and status (called from worker thread)."""
        progress_percent = (processed / total * 100) if total > 0 else 0

        # Update UI in main thread
        self.window.after(0, lambda: self.progress.config(value=progress_percent))
        self.window.after(0, lambda: self.status_label.config(
            text=f"Processing: {processed}/{total} - {Path(current_file).name}",
            fg="blue"
        ))

    def _update_status(self, message: str, color: str = "black"):
        """Update status label (thread-safe)."""
        self.window.after(0, lambda: self.status_label.config(text=message, fg=color))

    def _append_result(self, text: str):
        """Append text to results area (thread-safe)."""
        self.window.after(0, lambda: self.results_text.insert(END, text))
        self.window.after(0, lambda: self.results_text.see(END))


# ==================== MAIN ====================

def main():
    """Main entry point."""
    print("=" * 80)
    print("COPYRIGHT & LICENSE EXTRACTION TOOL - Phase 1 Complete")
    print("=" * 80)
    print("\nStarting GUI...")
    print("\nPhase 1 Features:")
    print("  ✅ Case-insensitive copyright matching")
    print("  ✅ Smart file extension filtering")
    print("  ✅ Progress bar with cancel button")
    print("  ✅ Comprehensive error handling & logging")
    print("  ✅ License detection (MIT, GPL, Apache, BSD, etc.)")
    print("\n" + "=" * 80 + "\n")

    window = tk.Tk()
    window.title('Copyright & License Extraction Tool v2.0')
    window.geometry("900x700")
    window.configure(background='light blue')

    app = CopyrightExtractionGUI(window)

    window.mainloop()


if __name__ == "__main__":
    main()
