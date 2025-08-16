#!/usr/bin/env python3
"""
Build automation script for FlutterX documentation
"""

import subprocess
import sys
import os
import time
import shutil
from pathlib import Path
import json

class BuildAutomation:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.build_config = {
            'clean_build': True,
            'run_tests': True,
            'optimize_assets': True,
            'generate_sitemap': True,
            'validate_links': True,
            'compress_output': False
        }
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def load_build_config(self):
        """Load build configuration from file"""
        
        config_file = self.project_dir / "build-config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.build_config.update(user_config)
                    self.log("Loaded custom build configuration")
            except Exception as e:
                self.log(f"Error loading build config: {e}", "WARNING")
    
    def save_build_config(self):
        """Save current build configuration"""
        
        config_file = self.project_dir / "build-config.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.build_config, f, indent=2)
                self.log("Saved build configuration")
        except Exception as e:
            self.log(f"Error saving build config: {e}", "WARNING")
    
    def clean_build_directory(self) -> bool:
        """Clean the build directory"""
        
        if not self.build_config['clean_build']:
            return True
        
        self.log("Cleaning build directory...")
        
        site_dir = self.project_dir / "site"
        if site_dir.exists():
            try:
                shutil.rmtree(site_dir)
                self.log("Build directory cleaned")
                return True
            except Exception as e:
                self.log(f"Error cleaning build directory: {e}", "ERROR")
                return False
        
        return True
    
    def run_pre_build_tests(self) -> bool:
        """Run tests before building"""
        
        if not self.build_config['run_tests']:
            return True
        
        self.log("Running pre-build tests...")
        
        try:
            # Run content migration tests
            result = subprocess.run(
                [sys.executable, "tests/test_content_migration.py"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log("Pre-build tests failed", "ERROR")
                return False
            
            self.log("Pre-build tests passed")
            return True
            
        except Exception as e:
            self.log(f"Error running tests: {e}", "ERROR")
            return False
    
    def build_site(self) -> bool:
        """Build the static site"""
        
        self.log("Building static site...")
        
        try:
            # Build with mkdocs
            result = subprocess.run(
                ["mkdocs", "build", "--config-file", "mkdocs.yml", "--strict"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Site built successfully")
                
                # Show build statistics
                site_dir = self.project_dir / "site"
                if site_dir.exists():
                    total_files = len(list(site_dir.rglob("*")))
                    html_files = len(list(site_dir.rglob("*.html")))
                    css_files = len(list(site_dir.rglob("*.css")))
                    js_files = len(list(site_dir.rglob("*.js")))
                    image_files = len(list(site_dir.rglob("*.png"))) + len(list(site_dir.rglob("*.jpg"))) + len(list(site_dir.rglob("*.gif")))
                    
                    self.log(f"Build statistics:")
                    self.log(f"  Total files: {total_files}")
                    self.log(f"  HTML files: {html_files}")
                    self.log(f"  CSS files: {css_files}")
                    self.log(f"  JS files: {js_files}")
                    self.log(f"  Image files: {image_files}")
                
                return True
            else:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Build error: {e}", "ERROR")
            return False
    
    def optimize_assets(self) -> bool:
        """Optimize assets in the built site"""
        
        if not self.build_config['optimize_assets']:
            return True
        
        self.log("Optimizing assets...")
        
        site_dir = self.project_dir / "site"
        if not site_dir.exists():
            self.log("Site directory not found", "ERROR")
            return False
        
        try:
            # Optimize CSS files (basic minification)
            css_files = list(site_dir.rglob("*.css"))
            for css_file in css_files:
                self.minify_css(css_file)
            
            if css_files:
                self.log(f"Optimized {len(css_files)} CSS files")
            
            # Optimize HTML files (basic minification)
            html_files = list(site_dir.rglob("*.html"))
            for html_file in html_files:
                self.minify_html(html_file)
            
            if html_files:
                self.log(f"Optimized {len(html_files)} HTML files")
            
            return True
            
        except Exception as e:
            self.log(f"Asset optimization error: {e}", "ERROR")
            return False
    
    def minify_css(self, css_file: Path):
        """Basic CSS minification"""
        
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic minification - remove comments and extra whitespace
            import re
            
            # Remove comments
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r';\s*}', '}', content)
            content = re.sub(r'{\s*', '{', content)
            content = re.sub(r'}\s*', '}', content)
            content = re.sub(r':\s*', ':', content)
            content = re.sub(r';\s*', ';', content)
            
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(content.strip())
                
        except Exception as e:
            self.log(f"Error minifying {css_file}: {e}", "WARNING")
    
    def minify_html(self, html_file: Path):
        """Basic HTML minification"""
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic minification - remove extra whitespace between tags
            import re
            
            # Remove extra whitespace between tags
            content = re.sub(r'>\s+<', '><', content)
            
            # Remove leading/trailing whitespace from lines
            lines = content.split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            content = '\n'.join(lines)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.log(f"Error minifying {html_file}: {e}", "WARNING")
    
    def generate_sitemap(self) -> bool:
        """Generate sitemap.xml"""
        
        if not self.build_config['generate_sitemap']:
            return True
        
        self.log("Generating sitemap...")
        
        site_dir = self.project_dir / "site"
        if not site_dir.exists():
            return False
        
        try:
            # Get all HTML files
            html_files = list(site_dir.rglob("*.html"))
            
            # Generate sitemap content
            sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
            sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
            
            base_url = "https://flutterx.com"  # Update with actual domain
            
            for html_file in html_files:
                # Get relative path from site directory
                rel_path = html_file.relative_to(site_dir)
                
                # Convert to URL path
                url_path = str(rel_path).replace('\\', '/')
                if url_path.endswith('index.html'):
                    url_path = url_path[:-10]  # Remove index.html
                elif url_path.endswith('.html'):
                    url_path = url_path[:-5]   # Remove .html
                
                full_url = f"{base_url}/{url_path}".rstrip('/')
                if not full_url.endswith('/') and url_path != '':
                    full_url += '/'
                
                sitemap_content.append('  <url>')
                sitemap_content.append(f'    <loc>{full_url}</loc>')
                sitemap_content.append(f'    <lastmod>{time.strftime("%Y-%m-%d")}</lastmod>')
                sitemap_content.append('    <changefreq>weekly</changefreq>')
                sitemap_content.append('    <priority>0.8</priority>')
                sitemap_content.append('  </url>')
            
            sitemap_content.append('</urlset>')
            
            # Write sitemap
            sitemap_file = site_dir / "sitemap.xml"
            with open(sitemap_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sitemap_content))
            
            self.log(f"Generated sitemap with {len(html_files)} URLs")
            return True
            
        except Exception as e:
            self.log(f"Sitemap generation error: {e}", "ERROR")
            return False
    
    def validate_build(self) -> bool:
        """Validate the built site"""
        
        if not self.build_config['validate_links']:
            return True
        
        self.log("Validating build...")
        
        try:
            # Run link validation
            result = subprocess.run(
                [sys.executable, "scripts/validate-links.py", "--site-dir", "site"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Build validation passed")
                return True
            else:
                self.log("Build validation failed", "WARNING")
                # Don't fail the build for validation issues
                return True
                
        except Exception as e:
            self.log(f"Validation error: {e}", "WARNING")
            return True
    
    def compress_output(self) -> bool:
        """Compress build output"""
        
        if not self.build_config['compress_output']:
            return True
        
        self.log("Compressing build output...")
        
        site_dir = self.project_dir / "site"
        if not site_dir.exists():
            return False
        
        try:
            # Create compressed archive
            archive_name = f"flutterx-docs-{time.strftime('%Y%m%d-%H%M%S')}"
            archive_path = self.project_dir / f"{archive_name}.tar.gz"
            
            import tarfile
            
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(site_dir, arcname="site")
            
            self.log(f"Created compressed archive: {archive_path}")
            return True
            
        except Exception as e:
            self.log(f"Compression error: {e}", "ERROR")
            return False
    
    def generate_build_report(self, success: bool, start_time: float):
        """Generate build report"""
        
        end_time = time.time()
        build_time = end_time - start_time
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'success': success,
            'build_time': build_time,
            'config': self.build_config
        }
        
        # Add site statistics if build was successful
        if success:
            site_dir = self.project_dir / "site"
            if site_dir.exists():
                total_size = sum(f.stat().st_size for f in site_dir.rglob('*') if f.is_file())
                report['site_size_mb'] = total_size / (1024 * 1024)
                report['total_files'] = len(list(site_dir.rglob('*')))
        
        # Save report
        report_file = self.project_dir / "build-report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            self.log(f"Error saving build report: {e}", "WARNING")
        
        # Print summary
        self.log(f"Build completed in {build_time:.2f} seconds")
        if success:
            self.log("✅ Build successful!")
            if 'site_size_mb' in report:
                self.log(f"Site size: {report['site_size_mb']:.2f} MB")
                self.log(f"Total files: {report['total_files']}")
        else:
            self.log("❌ Build failed!")
    
    def run_build(self) -> bool:
        """Run the complete build process"""
        
        start_time = time.time()
        self.log("Starting automated build process...")
        
        # Load configuration
        self.load_build_config()
        
        # Build steps
        steps = [
            ("Clean build directory", self.clean_build_directory),
            ("Run pre-build tests", self.run_pre_build_tests),
            ("Build site", self.build_site),
            ("Optimize assets", self.optimize_assets),
            ("Generate sitemap", self.generate_sitemap),
            ("Validate build", self.validate_build),
            ("Compress output", self.compress_output)
        ]
        
        success = True
        
        for step_name, step_func in steps:
            self.log(f"Step: {step_name}")
            
            if not step_func():
                self.log(f"Step failed: {step_name}", "ERROR")
                success = False
                break
        
        # Generate build report
        self.generate_build_report(success, start_time)
        
        return success

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="FlutterX Documentation Build Automation")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--config", help="Build configuration file")
    parser.add_argument("--no-tests", action="store_true", help="Skip pre-build tests")
    parser.add_argument("--no-optimize", action="store_true", help="Skip asset optimization")
    parser.add_argument("--compress", action="store_true", help="Compress build output")
    
    args = parser.parse_args()
    
    builder = BuildAutomation(args.project_dir)
    
    # Override config based on arguments
    if args.no_tests:
        builder.build_config['run_tests'] = False
    if args.no_optimize:
        builder.build_config['optimize_assets'] = False
    if args.compress:
        builder.build_config['compress_output'] = True
    
    # Load custom config if provided
    if args.config:
        config_file = Path(args.config)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                    builder.build_config.update(custom_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                sys.exit(1)
    
    # Run build
    success = builder.run_build()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()