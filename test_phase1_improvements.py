#!/usr/bin/env python3
"""
Test script for Phase 1 improvements
Validates copyright and license detection
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from copyright_detector import CopyrightLicenseDetector, should_process_file


def test_copyright_detection():
    """Test copyright detection patterns."""
    print("=" * 80)
    print("TESTING COPYRIGHT DETECTION")
    print("=" * 80)

    test_cases = [
        # (input_text, expected_to_find)
        ("Copyright 2023 John Doe", True),
        ("copyright 2023 john doe", True),  # lowercase
        ("COPYRIGHT 2023 ACME CORP", True),  # uppercase
        ("© 2023 Example Inc.", True),  # copyright symbol
        ("(c) 2023 Developer", True),  # (c) notation
        ("(C) 2023 Company", True),  # (C) notation
        ("Copr. 2023 Organization", True),  # abbreviation
        ("Copyright (C) 2020-2023 Multi Year", True),  # range
        ("SPDX-FileCopyrightText: 2023 SPDX Format", True),  # SPDX
        ("This is just text without copyright", False),  # no copyright
        ("Copyright (C) YEAR NAME", False),  # template (junk)
    ]

    detector = CopyrightLicenseDetector()
    passed = 0
    failed = 0

    for i, (text, should_find) in enumerate(test_cases, 1):
        copyrights = detector.detect_copyrights(text)
        found = len(copyrights) > 0

        status = "✅ PASS" if found == should_find else "❌ FAIL"
        if found == should_find:
            passed += 1
        else:
            failed += 1

        print(f"\nTest {i}: {status}")
        print(f"  Input: {text[:60]}")
        print(f"  Expected to find: {should_find}")
        print(f"  Actually found: {found}")
        if copyrights:
            print(f"  Detected: {copyrights[0]}")

    print(f"\n{'=' * 80}")
    print(f"Copyright Detection: {passed}/{passed + failed} tests passed")
    print(f"{'=' * 80}\n")

    return failed == 0


def test_license_detection():
    """Test license detection patterns."""
    print("=" * 80)
    print("TESTING LICENSE DETECTION")
    print("=" * 80)

    test_cases = [
        # (input_text, expected_licenses)
        ("Licensed under the MIT License", {"MIT"}),
        ("This code uses the Apache License, Version 2.0", {"Apache-2.0"}),
        ("SPDX-License-Identifier: MIT", {"MIT"}),
        ("SPDX-License-Identifier: Apache-2.0", {"Apache-2.0"}),
        ("GNU General Public License, Version 2", {"GPL-2.0"}),
        ("GNU General Public License, Version 3", {"GPL-3.0"}),
        ("GPL v2", {"GPL-2.0"}),
        ("GPLv3", {"GPL-3.0"}),
        ("BSD 2-Clause License", {"BSD-2-Clause"}),
        ("BSD 3-Clause License", {"BSD-3-Clause"}),
        ("ISC License", {"ISC"}),
        ("Mozilla Public License, Version 2.0", {"MPL-2.0"}),
        ("This is just text without license info", set()),
    ]

    detector = CopyrightLicenseDetector()
    passed = 0
    failed = 0

    for i, (text, expected_licenses) in enumerate(test_cases, 1):
        detected_licenses = detector.detect_licenses(text)

        status = "✅ PASS" if detected_licenses == expected_licenses else "❌ FAIL"
        if detected_licenses == expected_licenses:
            passed += 1
        else:
            failed += 1

        print(f"\nTest {i}: {status}")
        print(f"  Input: {text[:60]}")
        print(f"  Expected: {expected_licenses}")
        print(f"  Detected: {detected_licenses}")

    print(f"\n{'=' * 80}")
    print(f"License Detection: {passed}/{passed + failed} tests passed")
    print(f"{'=' * 80}\n")

    return failed == 0


def test_multiline_copyright():
    """Test multi-line copyright detection."""
    print("=" * 80)
    print("TESTING MULTI-LINE COPYRIGHT")
    print("=" * 80)

    test_text = """
    /*
     * Copyright (C) 2023
     * John Doe and Jane Smith
     */

    // Copyright 2020-
    // 2023 ACME Corporation

    /* Copyright (c) 2023 by
       The Development Team */
    """

    detector = CopyrightLicenseDetector()
    copyrights = detector.detect_copyrights(test_text)

    print(f"\nInput text has multi-line copyrights")
    print(f"Detected {len(copyrights)} copyright(s):\n")

    for i, copyright in enumerate(copyrights, 1):
        print(f"  {i}. {copyright}")

    print(f"\n{'=' * 80}")
    success = len(copyrights) >= 3
    print(f"Multi-line Detection: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"{'=' * 80}\n")

    return success


def test_junk_filtering():
    """Test that junk/template text is filtered out."""
    print("=" * 80)
    print("TESTING JUNK FILTERING")
    print("=" * 80)

    junk_texts = [
        "Copyright (C) YEAR COPYRIGHT HOLDER",
        "Copyright (C) <year> <name of author>",
        "Copyright YOUR NAME YOUR EMAIL",
        "/* * * */",  # Only comment characters
    ]

    detector = CopyrightLicenseDetector()
    passed = 0
    failed = 0

    for i, text in enumerate(junk_texts, 1):
        copyrights = detector.detect_copyrights(text)

        status = "✅ PASS" if len(copyrights) == 0 else "❌ FAIL"
        if len(copyrights) == 0:
            passed += 1
        else:
            failed += 1

        print(f"\nTest {i}: {status}")
        print(f"  Junk text: {text}")
        print(f"  Should filter out: Yes")
        print(f"  Actually filtered: {len(copyrights) == 0}")

    print(f"\n{'=' * 80}")
    print(f"Junk Filtering: {passed}/{passed + failed} tests passed")
    print(f"{'=' * 80}\n")

    return failed == 0


def test_file_extensions():
    """Test file extension filtering."""
    print("=" * 80)
    print("TESTING FILE EXTENSION FILTERING")
    print("=" * 80)

    test_files = [
        # (filename, should_process)
        ("test.py", True),
        ("test.java", True),
        ("test.c", True),
        ("test.js", True),
        ("test.txt", True),
        ("README.md", True),
        ("LICENSE", True),  # Important file
        ("test.exe", False),  # Binary
        ("test.jpg", False),  # Image
        ("test.zip", False),  # Archive
        ("test.pdf", False),  # Not supported yet
    ]

    passed = 0
    failed = 0

    for filename, expected in test_files:
        # Create temp file path (doesn't need to exist)
        filepath = f"/tmp/{filename}"
        should_process_result, reason = should_process_file(filepath)

        status = "✅ PASS" if should_process_result == expected else "❌ FAIL"
        if should_process_result == expected:
            passed += 1
        else:
            failed += 1

        print(f"\n{status} {filename}")
        print(f"  Expected: {'Process' if expected else 'Skip'}")
        print(f"  Result: {'Process' if should_process_result else 'Skip'}")
        print(f"  Reason: {reason}")

    print(f"\n{'=' * 80}")
    print(f"File Extension Filtering: {passed}/{passed + failed} tests passed")
    print(f"{'=' * 80}\n")

    return failed == 0


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "PHASE 1 IMPROVEMENTS - VALIDATION TESTS" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    results = []

    # Run tests
    results.append(("Copyright Detection", test_copyright_detection()))
    results.append(("License Detection", test_license_detection()))
    results.append(("Multi-line Copyright", test_multiline_copyright()))
    results.append(("Junk Filtering", test_junk_filtering()))
    results.append(("File Extension Filtering", test_file_extensions()))

    # Summary
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 32 + "TEST SUMMARY" + " " * 34 + "║")
    print("╠" + "═" * 78 + "╣")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"║  {test_name:<50} {status:>25} ║")

    print("╠" + "═" * 78 + "╣")
    print(f"║  TOTAL: {total_passed}/{total_tests} test suites passed" + " " * (78 - 30 - len(str(total_passed)) - len(str(total_tests))) + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    if total_passed == total_tests:
        print("🎉 All Phase 1 improvements are working correctly!\n")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
