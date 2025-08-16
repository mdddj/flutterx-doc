#!/usr/bin/env python3
"""
Comprehensive build script for FlutterX documentation
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional

class SiteBuilder:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.build_log = []
        self.site_dir = self.project_dir / "site"
        self.venv_dir = self.project_dir / "venv"
        
    def log(self, message: str, level: str = "INFO"):
        """Log build messages"""
        formatted_message = f"[{level}] {message}"
        print(formatted_message)
        self.build_log.append(formatted_message)
    
    def setup_virtual_environment(self) -> bool:
        """Set up Python virtual environment"""
        
        self.log("Setting up virtual environment...")
        
        try:
            if not self.venv_dir.exists():
                self.log("Creating virtual environment...")
                result = subprocess.run([
                    sys.executable, "-m", "venv", str(self.venv_dir)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    self.log(f"Failed to create virtual environment: {result.stderr}", "ERROR")
                    return False
                
                self.log("✅ Virtual environment created")
            else:
                self.log("✅ Virtual environment already exists")
            
            return True
            
        except Exception as e:
            self.log(f"Error setting up virtual environment: {e}", "ERROR")
            return False
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        
        self.log("Installing dependencies...")
        
        try:
            # Determine pip path
            if os.name == 'nt':  # Windows
                pip_path = self.venv_dir / "Scripts" / "pip"
            else:  # Unix-like
                pip_path = self.venv_dir / "bin" / "pip"
            
            # Install requirements
            requirements_file = self.project_dir / "requirements.txt"
            
            if not requirements_file.exists():
                self.log("requirements.txt not found", "ERROR")
                return False
            
            result = subprocess.run([
                str(pip_path), "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log(f"Failed to install dependencies: {result.stderr}", "ERROR")
                return False
            
            self.log("✅ Dependencies installed successfully")
            return True
            
        except Exception as e:
            self.log(f"Error installing dependencies: {e}", "ERROR")
            return False
    
    def validate_configuration(self) -> bool:
        """Validate mkdocs configuration"""
        
        self.log("Validating configuration...")
        
        try:
            # Determine python path
            if os.name == 'nt':  # Windows
                python_path = self.venv_dir / "Scripts" / "python"
            else:  # Unix-like
                python_path = self.venv_dir / "bin" / "python"
            
            # Test configuration
            result = subprocess.run([
                str(python_path), "-c", """
import sys
import os
sys.path.insert(0, '.')
try:
    from mkdocs.config import load_config
    config = load_config()
    print(f"Site: {config.get('site_name', 'Unknown')}")
    print(f"Theme: {config.get('theme', {}).get('name', 'Unknown')}")
    print("Configuration is valid")
except Exception as e:
    print(f"Configuration error: {e}")
    sys.exit(1)
"""
            ], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode != 0:
                self.log(f"Configuration validation failed: {result.stderr}", "ERROR")
                return False
            
            self.log("✅ Configuration is valid")
            self.log(result.stdout)
            return True
            
        except Exception as e:
            self.log(f"Error validating configuration: {e}", "ERROR")
            return False
    
    def clean_build_directory(self):
        """Clean previous build artifacts"""
        
        self.log("Cleaning build directory...")
        
        try:
            if self.site_dir.exists():
                shutil.rmtree(self.site_dir)
                self.log("✅ Cleaned previous build")
            else:
                self.log("✅ No previous build to clean")
                
        except Exception as e:
            self.log(f"Error cleaning build directory: {e}", "WARNING")
    
    def build_site(self) -> bool:
        """Build the documentation site"""
        
        self.log("Building documentation site...")
        
        try:
            # Determine mkdocs path
            if os.name == 'nt':  # Windows
                mkdocs_path = self.venv_dir / "Scripts" / "mkdocs"
            else:  # Unix-like
                mkdocs_path = self.venv_dir / "bin" / "mkdocs"
            
            # Build the site
            result = subprocess.run([
                str(mkdocs_path), "build", "--clean", "--strict"
            ], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode != 0:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
            
            self.log("✅ Site built successfully")
            if result.stdout:
                self.log(result.stdout)
            
            return True
            
        except Exception as e:
            self.log(f"Error building site: {e}", "ERROR")
            return False
    
    def validate_build_output(self) -> bool:
        """Validate the build output"""
        
        self.log("Validating build output...")
        
        try:
            if not self.site_dir.exists():
                self.log("Site directory not found", "ERROR")
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
                full_path = self.site_dir / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
            
            if missing_files:
                self.log(f"Missing essential files: {missing_files}", "ERROR")
                return False
            
            # Check site size
            total_size = sum(f.stat().st_size for f in self.site_dir.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            
            self.log(f"✅ Build validation passed")
            self.log(f"Site size: {size_mb:.2f} MB")
            
            # Count files
            html_files = len(list(self.site_dir.rglob("*.html")))
            css_files = len(list(self.site_dir.rglob("*.css")))
            js_files = len(list(self.site_dir.rglob("*.js")))
            image_files = len(list(self.site_dir.rglob("*.png"))) + len(list(self.site_dir.rglob("*.jpg"))) + len(list(self.site_dir.rglob("*.svg")))
            
            self.log(f"Generated files: {html_files} HTML, {css_files} CSS, {js_files} JS, {image_files} images")
            
            return True
            
        except Exception as e:
            self.log(f"Error validating build output: {e}", "ERROR")
            return False
    
    def run_link_validation(self) -> bool:
        """Run link validation on built site"""
        
        self.log("Running link validation...")
        
        try:
            # Simple link validation - check for broken internal links
            broken_links = []
            
            for html_file in self.site_dir.rglob("*.html"):
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Basic check for obvious broken links
                    if 'href="404.html"' in content:
                        broken_links.append(f"{html_file}: Contains 404 links")
                    
                except Exception as e:
                    self.log(f"Error checking {html_file}: {e}", "WARNING")
            
            if broken_links:
                self.log(f"Found {len(broken_links)} potential link issues", "WARNING")
                for link in broken_links[:5]:  # Show first 5
                    self.log(f"  • {link}", "WARNING")
            else:
                self.log("✅ No obvious link issues found")
            
            return len(broken_links) == 0
            
        except Exception as e:
            self.log(f"Error running link validation: {e}", "WARNING")
            return True  # Don't fail build for link validation errors
    
    def generate_build_report(self):
        """Generate build report"""
        
        report_file = self.project_dir / "build-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Documentation Build Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Build Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.build_log:
                f.write(f"{log_entry}\n")
            
            f.write("\nBuild Summary:\n")
            f.write("-" * 30 + "\n")
            
            if self.site_dir.exists():
                total_files = len(list(self.site_dir.rglob('*')))
                f.write(f"Total files generated: {total_files}\n")
                
                total_size = sum(f.stat().st_size for f in self.site_dir.rglob('*') if f.is_file())
                size_mb = total_size / (1024 * 1024)
                f.write(f"Total site size: {size_mb:.2f} MB\n")
            
            f.write("\nNext Steps:\n")
            f.write("-" * 30 + "\n")
            f.write("1. Test the site: mkdocs serve\n")
            f.write("2. Deploy the 'site' directory to your web server\n")
            f.write("3. Set up CI/CD for automatic builds\n")
        
        self.log(f"Build report saved to: {report_file}")
    
    def run_build(self, clean: bool = True, validate: bool = True) -> bool:
        """Run the complete build process"""
        
        self.log("Starting documentation build process...")
        self.log(f"Project directory: {self.project_dir}")
        
        try:
            # Setup phase
            if not self.setup_virtual_environment():
                return False
            
            if not self.install_dependencies():
                return False
            
            if not self.validate_configuration():
                return False
            
            # Build phase
            if clean:
                self.clean_build_directory()
            
            if not self.build_site():
                return False
            
            # Validation phase
            if validate:
                if not self.validate_build_output():
                    return False
                
                self.run_link_validation()
            
            # Generate report
            self.generate_build_report()
            
            self.log("✅ Build process completed successfully!")
            self.log(f"🌐 Site generated in: {self.site_dir}")
            
            return True
            
        except Exception as e:
            self.log(f"Build process failed: {str(e)}", "ERROR")
            return False

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Build FlutterX documentation")
    parser.add_argument("--no-clean", action="store_true", help="Don't clean build directory")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    args = parser.parse_args()
    
    builder = SiteBuilder(args.project_dir)
    success = builder.run_build(
        clean=not args.no_clean,
        validate=not args.no_validate
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()