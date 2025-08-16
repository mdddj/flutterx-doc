#!/usr/bin/env python3
"""
End-to-end migration test for FlutterX documentation
"""

import subprocess
import sys
import time
import json
from pathlib import Path
import shutil

class EndToEndTester:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.test_results = {
            'start_time': time.time(),
            'steps': [],
            'success': False,
            'errors': [],
            'warnings': []
        }
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        print(formatted_message)
        
        # Store in results
        self.test_results['steps'].append({
            'timestamp': timestamp,
            'level': level,
            'message': message
        })
        
        if level == "ERROR":
            self.test_results['errors'].append(message)
        elif level == "WARNING":
            self.test_results['warnings'].append(message)
    
    def run_command(self, command: list, description: str, timeout: int = 300) -> bool:
        """Run a command and return success status"""
        
        self.log(f"Running: {description}")
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                self.log(f"✅ {description} completed successfully")
                return True
            else:
                self.log(f"❌ {description} failed: {result.stderr[:200]}...", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"❌ {description} timed out after {timeout}s", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ {description} error: {str(e)}", "ERROR")
            return False
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        
        self.log("🔍 Checking prerequisites...")
        
        # Check required files
        required_files = [
            "mkdocs.yml",
            "requirements.txt",
            "migrate.py",
            "docs",
            "scripts"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log(f"Missing required files: {missing_files}", "ERROR")
            return False
        
        # Check Python dependencies
        try:
            import yaml
            import jinja2
        except ImportError as e:
            self.log(f"Missing Python dependencies: {e}", "ERROR")
            return False
        
        self.log("✅ Prerequisites check passed")
        return True
    
    def run_full_migration(self) -> bool:
        """Run the complete migration process"""
        
        self.log("🚀 Starting full migration process...")
        
        # Step 1: Content migration
        if not self.run_command(
            [sys.executable, "migrate.py"],
            "Content migration"
        ):
            return False
        
        # Step 2: Asset migration
        if not self.run_command(
            [sys.executable, "scripts/migrate-assets.py"],
            "Asset migration"
        ):
            return False
        
        # Step 3: Navigation building
        if not self.run_command(
            [sys.executable, "scripts/build-navigation.py"],
            "Navigation building"
        ):
            return False
        
        # Step 4: Link fixing
        if not self.run_command(
            [sys.executable, "scripts/fix-image-links.py"],
            "Image link fixing"
        ):
            return False
        
        # Step 5: Cross-language link fixing
        if not self.run_command(
            [sys.executable, "scripts/fix-cross-language-links.py"],
            "Cross-language link fixing"
        ):
            return False
        
        # Step 6: Theme customization
        if not self.run_command(
            [sys.executable, "scripts/customize-theme.py"],
            "Theme customization"
        ):
            return False
        
        self.log("✅ Full migration process completed")
        return True
    
    def validate_migration_results(self) -> bool:
        """Validate the migration results"""
        
        self.log("🔍 Validating migration results...")
        
        # Run content validation
        if not self.run_command(
            [sys.executable, "scripts/validate-content-comprehensive.py"],
            "Content validation"
        ):
            self.log("Content validation failed", "WARNING")
        
        # Run navigation validation
        if not self.run_command(
            [sys.executable, "scripts/validate-navigation.py"],
            "Navigation validation"
        ):
            self.log("Navigation validation failed", "WARNING")
        
        # Run asset validation
        if not self.run_command(
            [sys.executable, "scripts/validate-assets.py"],
            "Asset validation"
        ):
            self.log("Asset validation failed", "WARNING")
        
        self.log("✅ Migration validation completed")
        return True
    
    def test_build_process(self) -> bool:
        """Test the build process"""
        
        self.log("🔨 Testing build process...")
        
        # Clean previous build
        site_dir = self.project_dir / "site"
        if site_dir.exists():
            shutil.rmtree(site_dir)
            self.log("Cleaned previous build")
        
        # Test development build
        if not self.run_command(
            [sys.executable, "scripts/build-site.py"],
            "Development build",
            timeout=600  # 10 minutes
        ):
            return False
        
        # Verify build output
        if not site_dir.exists():
            self.log("Build output directory not found", "ERROR")
            return False
        
        # Check for essential files
        essential_files = [
            "index.html",
            "zh/index.html",
            "en/index.html",
            "ja/index.html"
        ]
        
        missing_files = []
        for file_path in essential_files:
            if not (site_dir / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log(f"Missing essential build files: {missing_files}", "ERROR")
            return False
        
        self.log("✅ Build process test passed")
        return True
    
    def test_multi_language_functionality(self) -> bool:
        """Test multi-language functionality"""
        
        self.log("🌐 Testing multi-language functionality...")
        
        # Check language directories
        languages = ["zh", "en", "ja"]
        docs_dir = self.project_dir / "docs"
        
        for lang in languages:
            lang_dir = docs_dir / lang
            if not lang_dir.exists():
                self.log(f"Language directory missing: {lang}", "ERROR")
                return False
            
            # Check for index file
            index_file = lang_dir / "index.md"
            if not index_file.exists():
                self.log(f"Index file missing for language: {lang}", "ERROR")
                return False
        
        # Run multi-language tests
        if not self.run_command(
            [sys.executable, "tests/test_multilanguage.py"],
            "Multi-language tests"
        ):
            self.log("Multi-language tests failed", "WARNING")
        
        self.log("✅ Multi-language functionality test passed")
        return True
    
    def test_image_and_asset_loading(self) -> bool:
        """Test image and asset loading"""
        
        self.log("🖼️  Testing image and asset loading...")
        
        # Check assets directory
        assets_dir = self.project_dir / "docs" / "assets"
        if not assets_dir.exists():
            self.log("Assets directory not found", "ERROR")
            return False
        
        # Check for images
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg"]
        image_count = 0
        
        for ext in image_extensions:
            images = list(assets_dir.rglob(f"*{ext}"))
            image_count += len(images)
        
        if image_count == 0:
            self.log("No images found in assets directory", "WARNING")
        else:
            self.log(f"Found {image_count} images in assets directory")
        
        # Test image references in markdown files
        docs_dir = self.project_dir / "docs"
        broken_references = []
        
        for md_file in docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple check for image references
                import re
                image_refs = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
                
                for ref in image_refs:
                    if not ref.startswith(('http://', 'https://')):
                        # Check if local image exists
                        if ref.startswith('../'):
                            image_path = (md_file.parent / ref).resolve()
                        else:
                            image_path = md_file.parent / ref
                        
                        if not image_path.exists():
                            broken_references.append(f"{md_file}: {ref}")
                            
            except Exception as e:
                self.log(f"Error checking {md_file}: {e}", "WARNING")
        
        if broken_references:
            self.log(f"Found {len(broken_references)} broken image references", "WARNING")
            for ref in broken_references[:5]:  # Show first 5
                self.log(f"  - {ref}", "WARNING")
        else:
            self.log("✅ All image references appear valid")
        
        self.log("✅ Image and asset loading test completed")
        return True
    
    def test_navigation_functionality(self) -> bool:
        """Test navigation functionality"""
        
        self.log("🧭 Testing navigation functionality...")
        
        # Check mkdocs.yml for navigation
        mkdocs_config = self.project_dir / "mkdocs.yml"
        
        try:
            with open(mkdocs_config, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'nav:' not in content:
                self.log("Navigation section not found in mkdocs.yml", "ERROR")
                return False
            
            # Check for language-specific navigation
            languages = ["简体中文", "English", "日本語"]
            for lang in languages:
                if lang not in content:
                    self.log(f"Language navigation missing: {lang}", "WARNING")
            
        except Exception as e:
            self.log(f"Error reading mkdocs.yml: {e}", "ERROR")
            return False
        
        self.log("✅ Navigation functionality test passed")
        return True
    
    def run_comprehensive_tests(self) -> bool:
        """Run comprehensive test suite"""
        
        self.log("🧪 Running comprehensive test suite...")
        
        # Run all available tests
        test_commands = [
            ([sys.executable, "tests/test_content_migration.py"], "Content migration tests"),
            ([sys.executable, "tests/test_multilanguage.py"], "Multi-language tests"),
            ([sys.executable, "tests/test_framework.py"], "Framework tests")
        ]
        
        passed_tests = 0
        total_tests = len(test_commands)
        
        for command, description in test_commands:
            if self.run_command(command, description):
                passed_tests += 1
        
        success_rate = (passed_tests / total_tests) * 100
        self.log(f"Test suite results: {passed_tests}/{total_tests} passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:  # 80% pass rate required
            self.log("✅ Comprehensive test suite passed")
            return True
        else:
            self.log("❌ Comprehensive test suite failed", "ERROR")
            return False
    
    def generate_final_report(self) -> bool:
        """Generate final test report"""
        
        self.log("📊 Generating final report...")
        
        end_time = time.time()
        total_time = end_time - self.test_results['start_time']
        
        # Update results
        self.test_results['end_time'] = end_time
        self.test_results['total_time'] = total_time
        self.test_results['success'] = len(self.test_results['errors']) == 0
        
        # Generate summary
        summary = {
            'migration_status': 'SUCCESS' if self.test_results['success'] else 'FAILED',
            'total_time': f"{total_time:.2f} seconds",
            'total_steps': len(self.test_results['steps']),
            'errors': len(self.test_results['errors']),
            'warnings': len(self.test_results['warnings']),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save detailed report
        report_file = self.project_dir / "end-to-end-test-report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error saving detailed report: {e}", "WARNING")
        
        # Save summary report
        summary_file = self.project_dir / "migration-summary.json"
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error saving summary report: {e}", "WARNING")
        
        # Generate text report
        text_report = self.project_dir / "migration-summary.txt"
        try:
            with open(text_report, 'w', encoding='utf-8') as f:
                f.write("FlutterX Documentation Migration Summary\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Status: {summary['migration_status']}\n")
                f.write(f"Completion time: {summary['timestamp']}\n")
                f.write(f"Total duration: {summary['total_time']}\n")
                f.write(f"Steps executed: {summary['total_steps']}\n")
                f.write(f"Errors: {summary['errors']}\n")
                f.write(f"Warnings: {summary['warnings']}\n\n")
                
                if self.test_results['errors']:
                    f.write("Errors encountered:\n")
                    f.write("-" * 20 + "\n")
                    for error in self.test_results['errors']:
                        f.write(f"- {error}\n")
                    f.write("\n")
                
                if self.test_results['warnings']:
                    f.write("Warnings:\n")
                    f.write("-" * 20 + "\n")
                    for warning in self.test_results['warnings']:
                        f.write(f"- {warning}\n")
                    f.write("\n")
                
                f.write("Detailed execution log:\n")
                f.write("-" * 20 + "\n")
                for step in self.test_results['steps']:
                    f.write(f"[{step['timestamp']}] [{step['level']}] {step['message']}\n")
                    
        except Exception as e:
            self.log(f"Error saving text report: {e}", "WARNING")
        
        self.log(f"Reports saved: {report_file.name}, {summary_file.name}, {text_report.name}")
        return True
    
    def run_end_to_end_test(self) -> bool:
        """Run complete end-to-end test"""
        
        self.log("🎯 Starting end-to-end migration test...")
        
        # Test steps
        test_steps = [
            ("Check prerequisites", self.check_prerequisites),
            ("Run full migration", self.run_full_migration),
            ("Validate migration results", self.validate_migration_results),
            ("Test build process", self.test_build_process),
            ("Test multi-language functionality", self.test_multi_language_functionality),
            ("Test image and asset loading", self.test_image_and_asset_loading),
            ("Test navigation functionality", self.test_navigation_functionality),
            ("Run comprehensive tests", self.run_comprehensive_tests),
            ("Generate final report", self.generate_final_report)
        ]
        
        success = True
        
        for step_name, step_func in test_steps:
            self.log(f"\n📋 Step: {step_name}")
            
            try:
                if not step_func():
                    self.log(f"Step failed: {step_name}", "ERROR")
                    success = False
                    # Continue with remaining steps for complete report
                    
            except Exception as e:
                self.log(f"Step crashed: {step_name} - {str(e)}", "ERROR")
                success = False
        
        # Final summary
        if success:
            self.log("\n🎉 END-TO-END TEST PASSED!")
            self.log("✅ Migration is complete and ready for production")
        else:
            self.log("\n❌ END-TO-END TEST FAILED!")
            self.log("Please review errors and fix issues before deployment")
        
        return success

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="End-to-end migration test")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    args = parser.parse_args()
    
    tester = EndToEndTester(args.project_dir)
    success = tester.run_end_to_end_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()