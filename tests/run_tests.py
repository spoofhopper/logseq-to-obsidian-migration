#!/usr/bin/env python3
"""
Test runner for logseq_to_obsidian.py

This script runs all tests and provides a summary of results.
"""

import sys
import os
import subprocess
import unittest

def run_tests():
    """Run all tests and return results"""
    # Add tests directory to path
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, tests_dir)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def main():
    """Main test runner"""
    print("🧪 Running Logseq to Obsidian Migration Tool Tests")
    print("=" * 60)
    
    # Run tests
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failures}")
    print(f"💥 Errors: {errors}")
    print(f"⏭️  Skipped: {skipped}")
    
    if failures > 0:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if errors > 0:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    # Return appropriate exit code
    if failures > 0 or errors > 0:
        print(f"\n❌ Tests failed!")
        return 1
    else:
        print(f"\n✅ All tests passed!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
