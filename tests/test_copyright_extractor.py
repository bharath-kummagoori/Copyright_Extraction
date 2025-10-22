#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the copyright_extractor module.
"""

import pytest
from pathlib import Path
import tempfile
import os

from copyright_extractor import (
    CopyrightExtractor,
    extract_copyright,
    extract_copyright_from_file
)


class TestCopyrightExtractor:
    """Test suite for CopyrightExtractor class."""

    def test_lowercase_copyright(self):
        """Test extraction of lowercase 'copyright'."""
        text = "copyright 2023 John Doe"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "copyright 2023 john doe" in results[0]['statement'].lower()
        assert results[0]['line_number'] == 1

    def test_uppercase_copyright(self):
        """Test extraction of uppercase 'COPYRIGHT'."""
        text = "COPYRIGHT 2023 ACME CORPORATION"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "copyright 2023 acme corporation" in results[0]['statement'].lower()

    def test_mixed_case_copyright(self):
        """Test extraction of mixed case variations."""
        text = """
        CopyRight 2021 Example Inc
        copyRight 2022 Test Corp
        CopyRIGHT 2023 Another
        """
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 3
        for result in results:
            assert 'copyright' in result['statement'].lower()

    def test_unicode_copyright_symbol(self):
        """Test extraction with © symbol."""
        text = "© 2023 Unicode Corp"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "©" in results[0]['statement']
        assert "2023" in results[0]['statement']

    def test_lowercase_c_in_parentheses(self):
        """Test extraction of (c) notation."""
        text = "(c) 2023 Test Company"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "(c)" in results[0]['statement']

    def test_uppercase_c_in_parentheses(self):
        """Test extraction of (C) notation."""
        text = "(C) 2023 Big Corp"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "(C)" in results[0]['statement']

    def test_year_ranges(self):
        """Test extraction with year ranges."""
        text = """
        copyright 2020-2023 Company A
        © 2018-2022 Company B
        (c) 2015-2020 Company C
        """
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 3
        assert any("2020-2023" in r['statement'] for r in results)
        assert any("2018-2022" in r['statement'] for r in results)

    def test_multiple_years(self):
        """Test extraction with multiple years."""
        text = "copyright 2020, 2021, 2022 Company"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "2020" in results[0]['statement']

    def test_no_year(self):
        """Test extraction without year."""
        text = "copyright by John Doe"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "copyright" in results[0]['statement'].lower()

    def test_multiple_copyrights(self):
        """Test extraction of multiple copyright statements."""
        text = """
        copyright 2023 Company A
        Some other text here
        COPYRIGHT 2022 Company B
        More text
        © 2021 Company C
        (c) 2020 Company D
        """
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 4

    def test_line_numbers(self):
        """Test that line numbers are correctly tracked."""
        text = """Line 1
copyright 2023 on line 2
Line 3
© 2022 on line 4"""
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 2
        assert results[0]['line_number'] == 2
        assert results[1]['line_number'] == 4

    def test_empty_text(self):
        """Test with empty text."""
        text = ""
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 0

    def test_no_copyright(self):
        """Test with text containing no copyright."""
        text = "This is just some regular text without any copyright notices."
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 0

    def test_copyright_with_special_characters(self):
        """Test copyright with special characters in company name."""
        text = "Copyright 2023 ABC, Inc. & Co."
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1
        assert "ABC, Inc. & Co." in results[0]['statement']

    def test_get_unique_statements(self):
        """Test getting unique statements."""
        text = """
        copyright 2023 Company A
        copyright 2023 Company A
        copyright 2022 Company B
        """
        extractor = CopyrightExtractor()
        extractor.extract_from_text(text)
        unique = extractor.get_unique_statements()

        assert len(unique) == 2

    def test_format_results(self):
        """Test formatting of results."""
        text = "copyright 2023 Test"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)
        formatted = extractor.format_results(results)

        assert "Found 1 copyright statement(s)" in formatted
        assert "copyright 2023 Test" in formatted

    def test_format_results_empty(self):
        """Test formatting with no results."""
        extractor = CopyrightExtractor()
        formatted = extractor.format_results([])

        assert "No copyright statements found" in formatted


class TestFileOperations:
    """Test file-related operations."""

    def test_extract_from_file(self, tmp_path):
        """Test extracting copyright from a file."""
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("copyright 2023 File Test\n© 2022 Another")

        extractor = CopyrightExtractor()
        results = extractor.extract_from_file(test_file)

        assert len(results) == 2

    def test_extract_from_nonexistent_file(self):
        """Test with non-existent file."""
        extractor = CopyrightExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.extract_from_file("/nonexistent/file.txt")

    def test_extract_from_directory(self, tmp_path):
        """Test that extracting from a directory raises an error."""
        extractor = CopyrightExtractor()
        with pytest.raises(IsADirectoryError):
            extractor.extract_from_file(tmp_path)

    def test_search_directory(self, tmp_path):
        """Test searching a directory for copyrights."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file1.write_text("copyright 2023 File 1")

        file2 = tmp_path / "file2.txt"
        file2.write_text("© 2022 File 2")

        file3 = tmp_path / "no_copyright.txt"
        file3.write_text("This file has no copyright")

        extractor = CopyrightExtractor()
        results = extractor.search_directory(tmp_path)

        # Should find copyrights in 2 files
        assert len(results) == 2

    def test_search_directory_with_subdirectories(self, tmp_path):
        """Test searching directory with subdirectories."""
        # Create subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        # Create files in different locations
        (tmp_path / "root.txt").write_text("copyright 2023 Root")
        (subdir / "sub.txt").write_text("© 2022 Sub")

        extractor = CopyrightExtractor()
        results = extractor.search_directory(tmp_path, pattern="**/*.txt")

        assert len(results) == 2

    def test_search_directory_excludes_git(self, tmp_path):
        """Test that .git directories are excluded."""
        # Create .git directory
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("copyright 2023 Git Config")

        # Create normal file
        (tmp_path / "normal.txt").write_text("copyright 2023 Normal")

        extractor = CopyrightExtractor()
        results = extractor.search_directory(tmp_path)

        # Should only find the normal file
        assert len(results) == 1
        assert "normal.txt" in str(list(results.keys())[0])


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_extract_copyright_function(self):
        """Test the convenience extract_copyright function."""
        text = "copyright 2023 Test\n© 2022 Another"
        statements = extract_copyright(text)

        assert len(statements) == 2
        assert isinstance(statements[0], str)

    def test_extract_copyright_from_file_function(self, tmp_path):
        """Test the convenience extract_copyright_from_file function."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("copyright 2023 File")

        statements = extract_copyright_from_file(test_file)

        assert len(statements) == 1
        assert "copyright 2023 File" in statements[0]


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_copyright_at_line_start(self):
        """Test copyright at the beginning of a line."""
        text = "copyright 2023 Start of line"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1

    def test_copyright_with_extra_whitespace(self):
        """Test copyright with extra whitespace."""
        text = "copyright    2023    Lots of spaces"
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 1

    def test_copyright_in_code_comment(self):
        """Test copyright in typical code comment formats."""
        text = """
        # copyright 2023 Python comment
        // copyright 2022 C++ comment
        /* copyright 2021 C comment */
        """
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 3

    def test_all_variations_together(self):
        """Test all copyright variations in one text."""
        text = """
        copyright 2023 Lowercase
        COPYRIGHT 2023 Uppercase
        CopyRight 2023 Mixed case
        © 2023 Unicode symbol
        (c) 2023 Lowercase parentheses
        (C) 2023 Uppercase parentheses
        """
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        assert len(results) == 6

    def test_multiline_copyright_statement(self):
        """Test that each line is treated separately."""
        text = """copyright 2023 Company
        All rights reserved."""
        extractor = CopyrightExtractor()
        results = extractor.extract_from_text(text)

        # Should find 1 copyright (second line doesn't have copyright keyword)
        assert len(results) == 1

    def test_utf8_encoding(self, tmp_path):
        """Test with UTF-8 encoded file containing © symbol."""
        test_file = tmp_path / "utf8.txt"
        test_file.write_text("© 2023 UTF-8 Test", encoding='utf-8')

        extractor = CopyrightExtractor()
        results = extractor.extract_from_file(test_file)

        assert len(results) == 1
        assert "©" in results[0]['statement']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
