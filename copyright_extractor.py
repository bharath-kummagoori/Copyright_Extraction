#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright Extraction Module

This module provides functionality to extract copyright statements from text
in various formats including:
- copyright (lowercase)
- COPYRIGHT (all caps)
- CopyRight, copyRight (mixed case)
- © - Unicode copyright symbol
- (c) or (C) - Common ASCII alternative
"""

import re
from pathlib import Path
from typing import List, Union, Dict


class CopyrightExtractor:
    """Extract copyright statements from text in various formats."""

    # Comprehensive regex pattern that matches all copyright variations
    # This pattern matches:
    # - © symbol followed by year (with optional range) or text
    # - (c) or (C) followed by year (with optional range) or text
    # - "copyright" (any case) followed by year or "by"
    COPYRIGHT_PATTERN = re.compile(
        r'(?:'
        # For © and (c)/(C), match year with optional range, or any content
        r'(?:©|\(c\)|\(C\))\s*(?:'
        r'(?:(?:19|20)\d{2}(?:\s*-\s*(?:19|20)\d{2})?[^\n]*)|'  # Year with optional range
        r'(?:[^\n]+)'  # Or any other content
        r')'
        r'|'
        # For the word "copyright", require either a year or "by"
        r'\bcopyright\b\s+(?:'
        r'(?:(?:19|20)\d{2}(?:\s*-\s*(?:19|20)\d{2})?)|'  # Year or year range
        r'(?:(?:19|20)\d{2}(?:\s*,\s*(?:19|20)\d{2})*)|'  # Multiple years
        r'(?:by\s+\S)|'                                     # "by" followed by non-whitespace
        r'(?:\d{4}\s+)'                                    # Year followed by space
        r')[^\n]*'
        r')',
        re.IGNORECASE | re.MULTILINE
    )

    def __init__(self):
        """Initialize the CopyrightExtractor."""
        self.results: List[Dict[str, Union[str, int]]] = []

    def extract_from_text(self, text: str) -> List[Dict[str, Union[str, int]]]:
        """
        Extract all copyright statements from the given text.

        Parameters
        ----------
        text : str
            The text to search for copyright statements.

        Returns
        -------
        List[Dict[str, Union[str, int]]]
            A list of dictionaries containing:
            - 'statement': The full copyright statement
            - 'line_number': The line number where it was found
            - 'start_pos': The starting position in the text
            - 'end_pos': The ending position in the text
        """
        results = []
        lines = text.split('\n')

        for line_num, line in enumerate(lines, start=1):
            matches = self.COPYRIGHT_PATTERN.finditer(line)
            for match in matches:
                statement = match.group().strip()
                if statement:  # Only add non-empty matches
                    results.append({
                        'statement': statement,
                        'line_number': line_num,
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })

        self.results = results
        return results

    def extract_from_file(self, file_path: Union[str, Path]) -> List[Dict[str, Union[str, int]]]:
        """
        Extract copyright statements from a file.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the file to read and extract copyrights from.

        Returns
        -------
        List[Dict[str, Union[str, int]]]
            A list of dictionaries containing copyright information.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        IsADirectoryError
            If the path is a directory.
        """
        path = Path(file_path)
        text = path.read_text(encoding='utf-8', errors='ignore')
        return self.extract_from_text(text)

    def get_unique_statements(self) -> List[str]:
        """
        Get unique copyright statements from the last extraction.

        Returns
        -------
        List[str]
            A list of unique copyright statements.
        """
        return list(set(result['statement'] for result in self.results))

    def format_results(self, results: List[Dict[str, Union[str, int]]] = None) -> str:
        """
        Format extraction results as a readable string.

        Parameters
        ----------
        results : List[Dict[str, Union[str, int]]], optional
            Results to format. If None, uses the last extraction results.

        Returns
        -------
        str
            Formatted results as a string.
        """
        if results is None:
            results = self.results

        if not results:
            return "No copyright statements found."

        output = []
        output.append(f"Found {len(results)} copyright statement(s):\n")
        output.append("=" * 80)

        for idx, result in enumerate(results, start=1):
            output.append(f"\n{idx}. Line {result['line_number']}:")
            output.append(f"   {result['statement']}")

        output.append("\n" + "=" * 80)
        return "\n".join(output)

    def search_directory(self, directory: Union[str, Path],
                        pattern: str = "**/*",
                        exclude_dirs: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Search for copyright statements in all files in a directory.

        Parameters
        ----------
        directory : Union[str, Path]
            The directory to search.
        pattern : str, optional
            Glob pattern for files to search (default: "**/*" for all files).
        exclude_dirs : List[str], optional
            List of directory names to exclude (e.g., ['.git', '__pycache__']).

        Returns
        -------
        Dict[str, List[Dict]]
            Dictionary mapping file paths to their copyright statements.
        """
        if exclude_dirs is None:
            exclude_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']

        dir_path = Path(directory)
        results = {}

        for file_path in dir_path.glob(pattern):
            # Skip directories
            if file_path.is_dir():
                continue

            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue

            # Try to read and extract (skip binary files that fail)
            try:
                copyrights = self.extract_from_file(file_path)
                if copyrights:
                    results[str(file_path)] = copyrights
            except (UnicodeDecodeError, PermissionError):
                # Skip files that can't be read as text
                continue

        return results


def extract_copyright(text: str) -> List[str]:
    """
    Convenience function to extract copyright statements from text.

    Parameters
    ----------
    text : str
        The text to search.

    Returns
    -------
    List[str]
        List of copyright statements found.
    """
    extractor = CopyrightExtractor()
    results = extractor.extract_from_text(text)
    return [result['statement'] for result in results]


def extract_copyright_from_file(file_path: Union[str, Path]) -> List[str]:
    """
    Convenience function to extract copyright statements from a file.

    Parameters
    ----------
    file_path : Union[str, Path]
        Path to the file.

    Returns
    -------
    List[str]
        List of copyright statements found.
    """
    extractor = CopyrightExtractor()
    results = extractor.extract_from_file(file_path)
    return [result['statement'] for result in results]


if __name__ == "__main__":
    # Example usage
    sample_text = """
    copyright 2023 John Doe
    COPYRIGHT 2020-2023 Jane Smith
    CopyRight 2022 ACME Corp
    © 2021 Example Inc.
    (c) 2019 Test Company
    (C) 2018-2020 Another Corp
    This file is copyrighted by Someone
    """

    extractor = CopyrightExtractor()
    results = extractor.extract_from_text(sample_text)
    print(extractor.format_results(results))
