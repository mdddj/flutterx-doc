#!/usr/bin/env python3
"""
Test framework for FlutterX documentation migration
"""

import unittest
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import json
import time

class TestResult:
    def __init__(self, name: str, passed: bool, message: str = "", details: Dict = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = time.time()

class TestSuite:
    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.results = []
        self.setup_done = False
        
    def add_test(self, test_func, name: str = None):
        """Add a test function to the suite"""
        test_name = name or test_func.__name__
        self.tests.append((test_name, test_func))
    
    def setup(self):
        """Override this method for suite setup"""
        pass
    
    def teardown(self):
        """Override this method for suite teardown"""
        pass
    
    def run_tests(self) -> List[TestResult]:
        """Run all tests in the suite"""
        
        print(f"Running test suite: {self.name}")
        
        # Setup
        if not self.setup_done:
            try:
                self.setup()
                self.setup_done = True
            except Exception as e:
                print(f"Setup failed: {e}")
                return []
        
        # Run tests
        for test_name, test_func in self.tests:
            try:
                print(f"  Running: {test_name}")
                result = test_func()
                
                if isinstance(result, TestResult):
                    self.results.append(result)
                elif isinstance(result, bool):
                    self.results.append(TestResult(test_name, result))
                else:
                    self.results.append(TestResult(test_name, True, str(result)))
                    
            except Exception as e:
                self.results.append(TestResult(test_name, False, str(e)))
        
        # Teardown
        try:
            self.teardown()
        except Exception as e:
            print(f"Teardown failed: {e}")
        
        return self.results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        return {
            'suite_name': self.name,
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / total * 100) if total > 0 else 0
        }

class TestRunner:
    def __init__(self):
        self.suites = []
        self.results = []
        
    def add_suite(self, suite: TestSuite):
        """Add a test suite"""
        self.suites.append(suite)
    
    def run_all_suites(self) -> Dict[str, Any]:
        """Run all test suites"""
        
        print("=" * 50)
        print("FlutterX Documentation Test Runner")
        print("=" * 50)
        
        suite_results = []
        
        for suite in self.suites:
            results = suite.run_tests()
            summary = suite.get_summary()
            
            suite_results.append({
                'suite': suite,
                'results': results,
                'summary': summary
            })
            
            # Print suite summary
            print(f"\n{suite.name}: {summary['passed']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
        
        # Overall summary
        total_tests = sum(sr['summary']['total_tests'] for sr in suite_results)
        total_passed = sum(sr['summary']['passed'] for sr in suite_results)
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        overall_summary = {
            'total_suites': len(self.suites),
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_tests - total_passed,
            'overall_success_rate': overall_success_rate,
            'suite_results': suite_results
        }
        
        print("\n" + "=" * 50)
        print(f"Overall Results: {total_passed}/{total_tests} passed ({overall_success_rate:.1f}%)")
        print("=" * 50)
        
        return overall_summary
    
    def generate_report(self, results: Dict[str, Any], output_file: str = "test-report.json"):
        """Generate detailed test report"""
        
        # Convert results to serializable format
        serializable_results = {
            'summary': {
                'total_suites': results['total_suites'],
                'total_tests': results['total_tests'],
                'total_passed': results['total_passed'],
                'total_failed': results['total_failed'],
                'overall_success_rate': results['overall_success_rate'],
                'timestamp': time.time()
            },
            'suites': []
        }
        
        for suite_result in results['suite_results']:
            suite_data = {
                'name': suite_result['summary']['suite_name'],
                'summary': suite_result['summary'],
                'tests': []
            }
            
            for test_result in suite_result['results']:
                test_data = {
                    'name': test_result.name,
                    'passed': test_result.passed,
                    'message': test_result.message,
                    'details': test_result.details,
                    'timestamp': test_result.timestamp
                }
                suite_data['tests'].append(test_data)
            
            serializable_results['suites'].append(suite_data)
        
        # Write JSON report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed test report saved to: {output_file}")
        
        # Write text report
        text_report_file = output_file.replace('.json', '.txt')
        
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write("FlutterX Documentation Test Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Overall summary
            f.write("Overall Summary:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total suites: {results['total_suites']}\n")
            f.write(f"Total tests: {results['total_tests']}\n")
            f.write(f"Passed: {results['total_passed']}\n")
            f.write(f"Failed: {results['total_failed']}\n")
            f.write(f"Success rate: {results['overall_success_rate']:.1f}%\n\n")
            
            # Suite details
            for suite_result in results['suite_results']:
                suite_summary = suite_result['summary']
                f.write(f"Suite: {suite_summary['suite_name']}\n")
                f.write("-" * 30 + "\n")
                f.write(f"Tests: {suite_summary['total_tests']}\n")
                f.write(f"Passed: {suite_summary['passed']}\n")
                f.write(f"Failed: {suite_summary['failed']}\n")
                f.write(f"Success rate: {suite_summary['success_rate']:.1f}%\n\n")
                
                # Test details
                for test_result in suite_result['results']:
                    status = "✅ PASS" if test_result.passed else "❌ FAIL"
                    f.write(f"  {status} {test_result.name}\n")
                    
                    if test_result.message:
                        f.write(f"    Message: {test_result.message}\n")
                    
                    if test_result.details:
                        f.write(f"    Details: {test_result.details}\n")
                
                f.write("\n")
        
        print(f"Text test report saved to: {text_report_file}")

# Utility functions for common test patterns
def assert_file_exists(file_path: str, message: str = "") -> TestResult:
    """Assert that a file exists"""
    path = Path(file_path)
    exists = path.exists()
    
    if not message:
        message = f"File {'exists' if exists else 'does not exist'}: {file_path}"
    
    return TestResult(f"file_exists_{path.name}", exists, message)

def assert_directory_exists(dir_path: str, message: str = "") -> TestResult:
    """Assert that a directory exists"""
    path = Path(dir_path)
    exists = path.exists() and path.is_dir()
    
    if not message:
        message = f"Directory {'exists' if exists else 'does not exist'}: {dir_path}"
    
    return TestResult(f"dir_exists_{path.name}", exists, message)

def assert_file_contains(file_path: str, content: str, message: str = "") -> TestResult:
    """Assert that a file contains specific content"""
    try:
        path = Path(file_path)
        if not path.exists():
            return TestResult(f"file_contains_{path.name}", False, f"File does not exist: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        contains = content in file_content
        
        if not message:
            message = f"File {'contains' if contains else 'does not contain'} expected content"
        
        return TestResult(f"file_contains_{path.name}", contains, message)
        
    except Exception as e:
        return TestResult(f"file_contains_{Path(file_path).name}", False, str(e))

def count_files_with_extension(directory: str, extension: str) -> int:
    """Count files with specific extension in directory"""
    path = Path(directory)
    if not path.exists():
        return 0
    
    return len(list(path.rglob(f"*{extension}")))