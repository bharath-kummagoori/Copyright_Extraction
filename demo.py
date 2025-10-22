#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for Copyright Extractor

This script demonstrates how to use the copyright_extractor module
to extract copyright statements in various formats.
"""

from copyright_extractor import CopyrightExtractor, extract_copyright
from pathlib import Path


def demo_basic_usage():
    """Demonstrate basic usage of the copyright extractor."""
    print("=" * 80)
    print("DEMO: Basic Usage - All Copyright Variations")
    print("=" * 80)

    # Sample text with all copyright variations
    sample_text = """
    This is a sample document with various copyright formats.

    copyright 2023 John Doe - Lowercase format
    COPYRIGHT 2020-2023 Jane Smith - Uppercase format
    CopyRight 2022 ACME Corp - Mixed case format
    © 2021 Example Inc. - Unicode symbol
    (c) 2019 Test Company - Lowercase (c) format
    (C) 2018-2020 Another Corp - Uppercase (C) format

    All of the above should be detected!

    Some additional examples:
    copyright 2023 Company A, Inc.
    Copyright 2020, 2021, 2022 Company B
    © 2023 Company C & Associates
    (c) Multiple Year Corp 2015-2023

    This line has no copyright and should be ignored.
    """

    # Create extractor instance
    extractor = CopyrightExtractor()

    # Extract copyrights
    results = extractor.extract_from_text(sample_text)

    # Display formatted results
    print(extractor.format_results(results))
    print()


def demo_simple_function():
    """Demonstrate the simple extract_copyright function."""
    print("=" * 80)
    print("DEMO: Simple Function Usage")
    print("=" * 80)

    text = """
    copyright 2023 Simple Example
    © 2022 Another Example
    (C) 2021 Third Example
    """

    # Use the convenience function
    statements = extract_copyright(text)

    print(f"Found {len(statements)} copyright statement(s):")
    for idx, stmt in enumerate(statements, 1):
        print(f"{idx}. {stmt}")
    print()


def demo_file_extraction():
    """Demonstrate extracting copyrights from a file."""
    print("=" * 80)
    print("DEMO: File Extraction")
    print("=" * 80)

    # Check if CE.py exists
    ce_file = Path("CE.py")
    if ce_file.exists():
        extractor = CopyrightExtractor()
        results = extractor.extract_from_file(ce_file)

        if results:
            print(f"Extracting copyrights from {ce_file}:")
            print(extractor.format_results(results))
        else:
            print(f"No copyrights found in {ce_file}")
    else:
        print(f"File {ce_file} not found. Skipping file extraction demo.")
    print()


def demo_unique_statements():
    """Demonstrate getting unique copyright statements."""
    print("=" * 80)
    print("DEMO: Unique Statements (removes duplicates)")
    print("=" * 80)

    text = """
    copyright 2023 Company A
    copyright 2023 Company A
    COPYRIGHT 2023 COMPANY A
    copyright 2022 Company B
    © 2022 Company B
    copyright 2022 Company B
    """

    extractor = CopyrightExtractor()
    extractor.extract_from_text(text)

    unique = extractor.get_unique_statements()

    print(f"Found {len(unique)} unique copyright statement(s):")
    for idx, stmt in enumerate(unique, 1):
        print(f"{idx}. {stmt}")
    print()


def demo_directory_search():
    """Demonstrate searching a directory for copyrights."""
    print("=" * 80)
    print("DEMO: Directory Search")
    print("=" * 80)

    current_dir = Path(".")

    extractor = CopyrightExtractor()

    # Search for Python files
    print(f"Searching for copyrights in Python files in {current_dir.absolute()}...")
    results = extractor.search_directory(current_dir, pattern="*.py")

    if results:
        print(f"\nFound copyrights in {len(results)} file(s):\n")
        for file_path, copyrights in results.items():
            print(f"📄 {file_path}:")
            for copyright_info in copyrights:
                print(f"   Line {copyright_info['line_number']}: {copyright_info['statement']}")
            print()
    else:
        print("No copyrights found in Python files.")
    print()


def demo_detailed_info():
    """Demonstrate accessing detailed information about copyrights."""
    print("=" * 80)
    print("DEMO: Detailed Copyright Information")
    print("=" * 80)

    text = """Line 1: No copyright here
Line 2: copyright 2023 First Corp
Line 3: Still no copyright
Line 4: © 2022 Second Corp
Line 5: More text
Line 6: (c) 2021 Third Corp"""

    extractor = CopyrightExtractor()
    results = extractor.extract_from_text(text)

    print(f"Found {len(results)} copyright(s) with detailed information:\n")
    for idx, info in enumerate(results, 1):
        print(f"{idx}. Copyright Statement: {info['statement']}")
        print(f"   Line Number: {info['line_number']}")
        print(f"   Position: {info['start_pos']} - {info['end_pos']}")
        print()


def demo_code_comments():
    """Demonstrate extracting copyrights from code comments."""
    print("=" * 80)
    print("DEMO: Copyrights in Code Comments")
    print("=" * 80)

    code_sample = """
    # Python comment - copyright 2023 Python Dev

    def my_function():
        '''
        Docstring here
        © 2022 DocString Author
        '''
        pass

    // JavaScript comment - Copyright 2021 JS Dev

    /*
     * C-style comment
     * (c) 2020 C Developer
     */
    """

    extractor = CopyrightExtractor()
    results = extractor.extract_from_text(code_sample)

    print(extractor.format_results(results))
    print()


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "COPYRIGHT EXTRACTOR DEMO" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    demos = [
        demo_basic_usage,
        demo_simple_function,
        demo_file_extraction,
        demo_unique_statements,
        demo_detailed_info,
        demo_code_comments,
        demo_directory_search,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"Error in {demo.__name__}: {e}\n")

    print("=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nSupported copyright formats:")
    print("  ✓ copyright (lowercase)")
    print("  ✓ COPYRIGHT (uppercase)")
    print("  ✓ CopyRight, copyRight (mixed case)")
    print("  ✓ © (Unicode copyright symbol)")
    print("  ✓ (c) or (C) (ASCII alternatives)")
    print("\nFor more information, see the documentation in copyright_extractor.py")
    print()


if __name__ == "__main__":
    main()
