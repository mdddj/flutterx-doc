#!/usr/bin/env python3
"""
Test runner for all FlutterX documentation tests
"""

import subprocess
import sys
from pathlib import Path
import time

class TestRunner:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.test_results = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages"""
        formatted_message = f"[{level}] {message}"
        print(formatted_message)
    
    def run_test_suite(self, test_script: str, description: str) -> dict:
        """Run a test suite and return results"""
        
        self.log(f"🧪 Running: {description}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [sys.executable, test_script],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            execution_time = time.time() - start_time
            
            test_result = {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            if result.returncode == 0:
                self.log(f"✅ {description} PASSED ({execution_time:.2f}s)")
            else:
                self.log(f"❌ {description} FAILED ({execution_time:.2f}s)")
                if result.stderr:
                    self.log(f"   Error: {result.stderr[:200]}...", "ERROR")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            self.log(f"⏰ {description} TIMED OUT", "ERROR")
            return {
                'success': False,
                'execution_time': 600,
                'stdout': '',
                'stderr': 'Test timed out'
            }
        except Exception as e:
            self.log(f"💥 {description} CRASHED: {str(e)}", "ERROR")
            return {
                'success': False,
                'execution_time': 0,
                'stdout': '',
                'stderr': str(e)
            }
    
    def run_all_tests(self) -> bool:
        """Run all test suites"""
        
        self.log("🚀 Starting comprehensive test suite...")
        
        test_suites = [
            ("tests/test_migration.py", "Migration Integrity Tests"),
            ("tests/test_performance.py", "Performance Tests"),
            ("tests/test_integration.py", "Integration Tests")
        ]
        
        total_start_time = time.time()
        
        for test_script, description in test_suites:
            test_path = self.project_dir / test_script
            
            if test_path.exists():
                result = self.run_test_suite(test_script, description)
                self.test_results[description] = result
            else:
                self.log(f"⚠️  Test script not found: {test_script}", "WARNING")
                self.test_results[description] = {
                    'success': False,
                    'execution_time': 0,
                    'stdout': '',
                    'stderr': 'Test script not found'
                }
        
        total_execution_time = time.time() - total_start_time
        
        # Generate summary
        self.generate_test_summary(total_execution_time)
        
        # Calculate overall success
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        total_tests = len(self.test_results)
        
        return passed_tests == total_tests
    
    def generate_test_summary(self, total_time: float):
        """Generate comprehensive test summary"""
        
        self.log("\n📊 Test Summary")
        self.log("=" * 50)
        
        passed_tests = 0
        failed_tests = 0
        total_execution_time = 0
        
        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            execution_time = result['execution_time']
            
            self.log(f"{test_name}: {status} ({execution_time:.2f}s)")
            
            if result['success']:
                passed_tests += 1
            else:
                failed_tests += 1
            
            total_execution_time += execution_time
        
        success_rate = (passed_tests / len(self.test_results)) * 100 if self.test_results else 0
        
        self.log("\n📈 Overall Results:")
        self.log(f"   Tests passed: {passed_tests}")
        self.log(f"   Tests failed: {failed_tests}")
        self.log(f"   Success rate: {success_rate:.1f}%")
        self.log(f"   Total execution time: {total_time:.2f}s")
        
        # Generate detailed report
        self.generate_detailed_report(total_time)
        
        if success_rate == 100:
            self.log("\n🎉 ALL TESTS PASSED! Your migration is ready for production.")
        elif success_rate >= 80:
            self.log("\n✅ Most tests passed. Review failed tests before deployment.")
        else:
            self.log("\n❌ Multiple test failures. Please address issues before deployment.")
    
    def generate_detailed_report(self, total_time: float):
        """Generate detailed test report"""
        
        report_file = self.project_dir / "comprehensive-test-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Comprehensive Test Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Test execution completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total execution time: {total_time:.2f} seconds\n\n")
            
            # Summary
            passed_tests = sum(1 for result in self.test_results.values() if result['success'])
            failed_tests = len(self.test_results) - passed_tests
            success_rate = (passed_tests / len(self.test_results)) * 100 if self.test_results else 0
            
            f.write("Summary:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Tests passed: {passed_tests}\n")
            f.write(f"Tests failed: {failed_tests}\n")
            f.write(f"Success rate: {success_rate:.1f}%\n\n")
            
            # Detailed results
            f.write("Detailed Results:\n")
            f.write("-" * 30 + "\n")
            
            for test_name, result in self.test_results.items():
                f.write(f"\n{test_name}:\n")
                f.write(f"  Status: {'PASSED' if result['success'] else 'FAILED'}\n")
                f.write(f"  Execution time: {result['execution_time']:.2f}s\n")
                
                if result['stdout']:
                    f.write(f"  Output: {result['stdout'][:500]}...\n")
                
                if result['stderr']:
                    f.write(f"  Errors: {result['stderr'][:500]}...\n")
            
            # Recommendations
            f.write("\nRecommendations:\n")
            f.write("-" * 30 + "\n")
            
            if success_rate == 100:
                f.write("✅ All tests passed! Your migration is production-ready.\n")
                f.write("   - You can proceed with deployment\n")
                f.write("   - Consider setting up CI/CD for automated testing\n")
            elif success_rate >= 80:
                f.write("⚠️  Most tests passed, but some issues need attention.\n")
                f.write("   - Review failed tests and fix issues\n")
                f.write("   - Re-run tests after fixes\n")
            else:
                f.write("❌ Multiple test failures detected.\n")
                f.write("   - Review all failed tests carefully\n")
                f.write("   - Fix critical issues before deployment\n")
                f.write("   - Consider running tests individually for debugging\n")
        
        self.log(f"Detailed test report saved to: {report_file}")

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Run all FlutterX documentation tests")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    args = parser.parse_args()
    
    runner = TestRunner(args.project_dir)
    
    if args.quick:
        # Run only migration tests for quick validation
        runner.log("🏃 Running quick tests...")
        result = runner.run_test_suite("tests/test_migration.py", "Quick Migration Tests")
        success = result['success']
    else:
        success = runner.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()