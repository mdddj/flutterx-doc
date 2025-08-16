#!/usr/bin/env python3
"""
Generate comprehensive test summary for FlutterX migration
"""

import json
import sys
from pathlib import Path
import time

class TestSummaryGenerator:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.test_reports = []
        
    def collect_test_reports(self):
        """Collect all test reports"""
        
        report_files = [
            "content-migration-test-report.json",
            "multilanguage-test-report.json",
            "framework-test-report.json"
        ]
        
        for report_file in report_files:
            report_path = self.project_dir / report_file
            if report_path.exists():
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                        self.test_reports.append(report_data)
                except Exception as e:
                    print(f"Error reading {report_file}: {e}")
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        
        self.collect_test_reports()
        
        # Calculate overall statistics
        total_suites = 0
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        suite_results = []
        
        for report in self.test_reports:
            for suite in report.get('suites', []):
                total_suites += 1
                suite_summary = suite.get('summary', {})
                suite_name = suite_summary.get('suite_name', 'Unknown Suite')
                suite_tests = suite_summary.get('total_tests', 0)
                suite_passed = suite_summary.get('passed', 0)
                suite_failed = suite_summary.get('failed', 0)
                
                total_tests += suite_tests
                total_passed += suite_passed
                total_failed += suite_failed
                
                suite_results.append({
                    'name': suite_name,
                    'tests': suite_tests,
                    'passed': suite_passed,
                    'failed': suite_failed,
                    'success_rate': (suite_passed / suite_tests * 100) if suite_tests > 0 else 0
                })
        
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Generate summary report
        summary = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall': {
                'suites': total_suites,
                'tests': total_tests,
                'passed': total_passed,
                'failed': total_failed,
                'success_rate': overall_success_rate
            },
            'suites': suite_results
        }
        
        return summary
    
    def print_summary(self, summary):
        """Print test summary to console"""
        
        print("🎯 FlutterX Migration Test Summary")
        print("=" * 50)
        print(f"Generated: {summary['timestamp']}")
        print()
        
        overall = summary['overall']
        print("📊 Overall Results:")
        print(f"   Test suites: {overall['suites']}")
        print(f"   Total tests: {overall['tests']}")
        print(f"   Passed: {overall['passed']}")
        print(f"   Failed: {overall['failed']}")
        print(f"   Success rate: {overall['success_rate']:.1f}%")
        print()
        
        print("📋 Suite Details:")
        for suite in summary['suites']:
            status = "✅" if suite['failed'] == 0 else "❌"
            print(f"   {status} {suite['name']}: {suite['passed']}/{suite['tests']} ({suite['success_rate']:.1f}%)")
        
        print()
        
        # Overall assessment
        if overall['success_rate'] == 100:
            print("🎉 EXCELLENT! All tests passed. Migration is production-ready.")
        elif overall['success_rate'] >= 90:
            print("✅ GOOD! Most tests passed. Minor issues to address.")
        elif overall['success_rate'] >= 80:
            print("⚠️  ACCEPTABLE. Some issues need attention before deployment.")
        else:
            print("❌ NEEDS WORK. Significant issues require fixing.")
    
    def save_summary(self, summary):
        """Save summary to file"""
        
        # Save JSON summary
        json_file = self.project_dir / "test-summary.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        text_file = self.project_dir / "test-summary.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("FlutterX Migration Test Summary\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {summary['timestamp']}\n\n")
            
            overall = summary['overall']
            f.write("Overall Results:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Test suites: {overall['suites']}\n")
            f.write(f"Total tests: {overall['tests']}\n")
            f.write(f"Passed: {overall['passed']}\n")
            f.write(f"Failed: {overall['failed']}\n")
            f.write(f"Success rate: {overall['success_rate']:.1f}%\n\n")
            
            f.write("Suite Details:\n")
            f.write("-" * 20 + "\n")
            for suite in summary['suites']:
                status = "PASS" if suite['failed'] == 0 else "FAIL"
                f.write(f"{suite['name']}: {status} ({suite['passed']}/{suite['tests']} - {suite['success_rate']:.1f}%)\n")
            
            f.write("\nRecommendations:\n")
            f.write("-" * 20 + "\n")
            
            if overall['success_rate'] == 100:
                f.write("✅ All tests passed! Your migration is production-ready.\n")
                f.write("   - Proceed with deployment\n")
                f.write("   - Set up monitoring and CI/CD\n")
            elif overall['success_rate'] >= 90:
                f.write("✅ Most tests passed with minor issues.\n")
                f.write("   - Review failed tests\n")
                f.write("   - Fix minor issues\n")
                f.write("   - Re-run tests before deployment\n")
            elif overall['success_rate'] >= 80:
                f.write("⚠️  Acceptable results but needs attention.\n")
                f.write("   - Address failed tests\n")
                f.write("   - Validate critical functionality\n")
                f.write("   - Consider staged deployment\n")
            else:
                f.write("❌ Significant issues detected.\n")
                f.write("   - Review all failed tests\n")
                f.write("   - Fix critical issues\n")
                f.write("   - Re-run complete test suite\n")
                f.write("   - Do not deploy until issues resolved\n")
        
        print(f"📄 Summary saved to: {json_file} and {text_file}")
    
    def run(self):
        """Run summary generation"""
        
        summary = self.generate_summary()
        self.print_summary(summary)
        self.save_summary(summary)
        
        # Return success status
        return summary['overall']['success_rate'] >= 80

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate test summary")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    args = parser.parse_args()
    
    generator = TestSummaryGenerator(args.project_dir)
    success = generator.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()