#!/usr/bin/env python3
"""
Test the mkdocs build process
"""

import subprocess
import sys
from pathlib import Path

class BuildTester:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.test_log = []
        
    def log(self, message: str):
        """Log test messages"""
        print(message)
        self.test_log.append(message)
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        
        self.log("Checking dependencies...")
        
        try:
            # Check if mkdocs is available
            result = subprocess.run(['python3', '-c', 'import mkdocs'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log("✅ MkDocs is available")
            else:
                self.log("❌ MkDocs not found - install with: pip install -r requirements.txt")
                return False
        except Exception as e:
            self.log(f"❌ Error checking MkDocs: {e}")
            return False
        
        return True
    
    def validate_config(self):
        """Validate mkdocs.yml configuration"""
        
        self.log("Validating mkdocs.yml configuration...")
        
        config_file = self.project_dir / "mkdocs.yml"
        
        if not config_file.exists():
            self.log("❌ mkdocs.yml not found")
            return False
        
        try:
            # Try to parse the config
            result = subprocess.run(['python3', '-c', '''
import yaml
with open("mkdocs.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    print("Config loaded successfully")
'''], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode == 0:
                self.log("✅ mkdocs.yml is valid YAML")
            else:
                self.log(f"❌ mkdocs.yml validation failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error validating config: {e}")
            return False
        
        return True
    
    def check_required_files(self):
        """Check if required files exist"""
        
        self.log("Checking required files...")
        
        required_files = [
            "mkdocs.yml",
            "docs/index.md",
            "docs/zh/index.md",
            "docs/en/index.md", 
            "docs/ja/index.md",
            "docs/stylesheets/extra.css",
            "requirements.txt"
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if full_path.exists():
                self.log(f"✅ Found: {file_path}")
            else:
                missing_files.append(file_path)
                self.log(f"❌ Missing: {file_path}")
        
        if missing_files:
            self.log(f"❌ {len(missing_files)} required files are missing")
            return False
        
        self.log("✅ All required files found")
        return True
    
    def test_dry_build(self):
        """Test a dry build without actually building"""
        
        self.log("Testing configuration...")
        
        try:
            # Test mkdocs config
            result = subprocess.run(['python3', '-c', '''
import sys
sys.path.insert(0, ".")
try:
    from mkdocs.config import load_config
    config = load_config()
    print(f"Site name: {config.get('site_name', 'Unknown')}")
    print(f"Theme: {config.get('theme', {}).get('name', 'Unknown')}")
    print(f"Plugins: {len(config.get('plugins', []))}")
    print("Configuration test passed")
except Exception as e:
    print(f"Configuration test failed: {e}")
    sys.exit(1)
'''], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode == 0:
                self.log("✅ Configuration test passed")
                self.log(result.stdout)
            else:
                self.log(f"❌ Configuration test failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error testing configuration: {e}")
            return False
        
        return True
    
    def generate_test_report(self):
        """Generate test report"""
        
        report_file = self.project_dir / "build-test-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Build Test Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Test Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.test_log:
                f.write(f"{log_entry}\n")
            
            f.write("\nNext Steps:\n")
            f.write("-" * 30 + "\n")
            f.write("1. Install dependencies: pip install -r requirements.txt\n")
            f.write("2. Test build: mkdocs build\n")
            f.write("3. Start dev server: mkdocs serve\n")
            f.write("4. View site at: http://127.0.0.1:8000\n")
        
        self.log(f"Test report saved to: {report_file}")
    
    def run_tests(self):
        """Run all build tests"""
        
        self.log("Starting build tests...")
        
        try:
            # Run tests
            tests_passed = 0
            total_tests = 4
            
            if self.check_dependencies():
                tests_passed += 1
            
            if self.validate_config():
                tests_passed += 1
            
            if self.check_required_files():
                tests_passed += 1
            
            if self.test_dry_build():
                tests_passed += 1
            
            # Generate report
            self.generate_test_report()
            
            self.log(f"✅ Build tests completed: {tests_passed}/{total_tests} passed")
            
            if tests_passed == total_tests:
                self.log("🎉 All tests passed! Your documentation is ready to build.")
            else:
                self.log("⚠️  Some tests failed. Please check the issues above.")
            
            return tests_passed == total_tests
            
        except Exception as e:
            self.log(f"❌ Build tests failed: {str(e)}")
            return False

def main():
    """Main function"""
    
    project_dir = "."
    
    tester = BuildTester(project_dir)
    success = tester.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()