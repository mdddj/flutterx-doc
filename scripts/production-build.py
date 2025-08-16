#!/usr/bin/env python3
"""
Production build optimization for FlutterX documentation
"""

import subprocess
import sys
import os
import time
import shutil
import gzip
from pathlib import Path
import json
import hashlib

class ProductionBuilder:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.build_stats = {
            'start_time': time.time(),
            'files_processed': 0,
            'size_before': 0,
            'size_after': 0,
            'optimizations': []
        }
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def clean_and_build(self) -> bool:
        """Clean and build the site"""
        
        self.log("Starting production build...")
        
        # Clean previous build
        site_dir = self.project_dir / "site"
        if site_dir.exists():
            shutil.rmtree(site_dir)
            self.log("Cleaned previous build")
        
        # Build with strict mode
        try:
            result = subprocess.run(
                ["mkdocs", "build", "--config-file", "mkdocs.yml", "--strict"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Site built successfully")
                return True
            else:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Build error: {e}", "ERROR")
            return False
    
    def calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        
        total_size = 0
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
    def minify_html_files(self) -> bool:
        """Minify HTML files"""
        
        self.log("Minifying HTML files...")
        
        site_dir = self.project_dir / "site"
        html_files = list(site_dir.rglob("*.html"))
        
        minified_count = 0
        size_saved = 0
        
        for html_file in html_files:
            try:
                original_size = html_file.stat().st_size
                
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Advanced HTML minification
                minified_content = self.minify_html_content(content)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(minified_content)
                
                new_size = html_file.stat().st_size
                size_saved += original_size - new_size
                minified_count += 1
                
            except Exception as e:
                self.log(f"Error minifying {html_file}: {e}", "WARNING")
        
        self.log(f"Minified {minified_count} HTML files, saved {size_saved / 1024:.1f} KB")
        self.build_stats['optimizations'].append(f"HTML minification: {size_saved / 1024:.1f} KB saved")
        
        return True
    
    def minify_html_content(self, content: str) -> str:
        """Advanced HTML minification"""
        
        import re
        
        # Remove HTML comments (but preserve IE conditionals)
        content = re.sub(r'<!--(?!\[if).*?-->', '', content, flags=re.DOTALL)
        
        # Remove extra whitespace between tags
        content = re.sub(r'>\s+<', '><', content)
        
        # Remove leading/trailing whitespace from lines
        lines = content.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        # Join lines and remove extra spaces
        content = ' '.join(lines)
        
        # Remove spaces around certain characters
        content = re.sub(r'\s*([<>{}();,])\s*', r'\1', content)
        
        return content
    
    def minify_css_files(self) -> bool:
        """Minify CSS files"""
        
        self.log("Minifying CSS files...")
        
        site_dir = self.project_dir / "site"
        css_files = list(site_dir.rglob("*.css"))
        
        minified_count = 0
        size_saved = 0
        
        for css_file in css_files:
            try:
                original_size = css_file.stat().st_size
                
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Advanced CSS minification
                minified_content = self.minify_css_content(content)
                
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(minified_content)
                
                new_size = css_file.stat().st_size
                size_saved += original_size - new_size
                minified_count += 1
                
            except Exception as e:
                self.log(f"Error minifying {css_file}: {e}", "WARNING")
        
        self.log(f"Minified {minified_count} CSS files, saved {size_saved / 1024:.1f} KB")
        self.build_stats['optimizations'].append(f"CSS minification: {size_saved / 1024:.1f} KB saved")
        
        return True
    
    def minify_css_content(self, content: str) -> str:
        """Advanced CSS minification"""
        
        import re
        
        # Remove comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove spaces around certain characters
        content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', content)
        
        # Remove trailing semicolons before closing braces
        content = re.sub(r';\s*}', '}', content)
        
        # Remove leading/trailing whitespace
        content = content.strip()
        
        return content
    
    def minify_js_files(self) -> bool:
        """Minify JavaScript files"""
        
        self.log("Minifying JavaScript files...")
        
        site_dir = self.project_dir / "site"
        js_files = list(site_dir.rglob("*.js"))
        
        minified_count = 0
        size_saved = 0
        
        for js_file in js_files:
            try:
                original_size = js_file.stat().st_size
                
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic JS minification (for more advanced, use external tools)
                minified_content = self.minify_js_content(content)
                
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(minified_content)
                
                new_size = js_file.stat().st_size
                size_saved += original_size - new_size
                minified_count += 1
                
            except Exception as e:
                self.log(f"Error minifying {js_file}: {e}", "WARNING")
        
        self.log(f"Minified {minified_count} JS files, saved {size_saved / 1024:.1f} KB")
        self.build_stats['optimizations'].append(f"JS minification: {size_saved / 1024:.1f} KB saved")
        
        return True
    
    def minify_js_content(self, content: str) -> str:
        """Basic JavaScript minification"""
        
        import re
        
        # Remove single-line comments (but be careful with URLs)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove spaces around certain characters
        content = re.sub(r'\s*([{}();,=+\-*/<>!&|])\s*', r'\1', content)
        
        return content.strip()
    
    def optimize_images(self) -> bool:
        """Optimize image files"""
        
        self.log("Optimizing images...")
        
        site_dir = self.project_dir / "site"
        
        # Find image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(site_dir.rglob(f"*{ext}"))
        
        optimized_count = 0
        size_saved = 0
        
        for image_file in image_files:
            try:
                original_size = image_file.stat().st_size
                
                # Basic optimization - remove metadata for JPEG files
                if image_file.suffix.lower() in ['.jpg', '.jpeg']:
                    self.optimize_jpeg(image_file)
                
                # For SVG files, minify the XML
                elif image_file.suffix.lower() == '.svg':
                    self.optimize_svg(image_file)
                
                new_size = image_file.stat().st_size
                if new_size < original_size:
                    size_saved += original_size - new_size
                    optimized_count += 1
                
            except Exception as e:
                self.log(f"Error optimizing {image_file}: {e}", "WARNING")
        
        if optimized_count > 0:
            self.log(f"Optimized {optimized_count} images, saved {size_saved / 1024:.1f} KB")
            self.build_stats['optimizations'].append(f"Image optimization: {size_saved / 1024:.1f} KB saved")
        
        return True
    
    def optimize_jpeg(self, image_file: Path):
        """Basic JPEG optimization"""
        # This is a placeholder - in production, you'd use PIL or similar
        pass
    
    def optimize_svg(self, svg_file: Path):
        """Optimize SVG files"""
        
        try:
            with open(svg_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic SVG optimization
            import re
            
            # Remove comments
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'>\s+<', '><', content)
            
            with open(svg_file, 'w', encoding='utf-8') as f:
                f.write(content.strip())
                
        except Exception:
            pass  # Ignore errors for SVG optimization
    
    def create_gzip_files(self) -> bool:
        """Create gzip versions of text files"""
        
        self.log("Creating gzip compressed files...")
        
        site_dir = self.project_dir / "site"
        
        # File types to compress
        compress_extensions = ['.html', '.css', '.js', '.json', '.xml', '.txt']
        
        compressed_count = 0
        total_original_size = 0
        total_compressed_size = 0
        
        for ext in compress_extensions:
            files = list(site_dir.rglob(f"*{ext}"))
            
            for file_path in files:
                try:
                    original_size = file_path.stat().st_size
                    
                    # Skip very small files
                    if original_size < 1024:  # Less than 1KB
                        continue
                    
                    # Create gzip version
                    gz_path = file_path.with_suffix(file_path.suffix + '.gz')
                    
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(gz_path, 'wb') as f_out:
                            f_out.write(f_in.read())
                    
                    compressed_size = gz_path.stat().st_size
                    
                    # Only keep if compression is worthwhile (>10% reduction)
                    if compressed_size < original_size * 0.9:
                        total_original_size += original_size
                        total_compressed_size += compressed_size
                        compressed_count += 1
                    else:
                        gz_path.unlink()  # Remove if not worth it
                        
                except Exception as e:
                    self.log(f"Error compressing {file_path}: {e}", "WARNING")
        
        if compressed_count > 0:
            size_saved = total_original_size - total_compressed_size
            self.log(f"Created {compressed_count} gzip files, potential savings: {size_saved / 1024:.1f} KB")
            self.build_stats['optimizations'].append(f"Gzip compression: {compressed_count} files")
        
        return True
    
    def generate_file_hashes(self) -> bool:
        """Generate file hashes for cache busting"""
        
        self.log("Generating file hashes...")
        
        site_dir = self.project_dir / "site"
        
        # Files to hash
        hash_extensions = ['.css', '.js']
        hash_map = {}
        
        for ext in hash_extensions:
            files = list(site_dir.rglob(f"*{ext}"))
            
            for file_path in files:
                try:
                    # Calculate hash
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()[:8]
                    
                    # Create new filename with hash
                    stem = file_path.stem
                    suffix = file_path.suffix
                    new_name = f"{stem}.{file_hash}{suffix}"
                    new_path = file_path.parent / new_name
                    
                    # Rename file
                    file_path.rename(new_path)
                    
                    # Store mapping for updating references
                    relative_old = file_path.relative_to(site_dir)
                    relative_new = new_path.relative_to(site_dir)
                    hash_map[str(relative_old)] = str(relative_new)
                    
                except Exception as e:
                    self.log(f"Error hashing {file_path}: {e}", "WARNING")
        
        # Update references in HTML files
        if hash_map:
            self.update_file_references(hash_map)
            self.log(f"Generated hashes for {len(hash_map)} files")
        
        return True
    
    def update_file_references(self, hash_map: dict):
        """Update file references in HTML files"""
        
        site_dir = self.project_dir / "site"
        html_files = list(site_dir.rglob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update references
                for old_path, new_path in hash_map.items():
                    content = content.replace(old_path, new_path)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                self.log(f"Error updating references in {html_file}: {e}", "WARNING")
    
    def generate_build_manifest(self) -> bool:
        """Generate build manifest"""
        
        self.log("Generating build manifest...")
        
        site_dir = self.project_dir / "site"
        
        manifest = {
            'build_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'build_duration': time.time() - self.build_stats['start_time'],
            'optimizations': self.build_stats['optimizations'],
            'files': []
        }
        
        # Collect file information
        for file_path in site_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(site_dir)
                file_info = {
                    'path': str(relative_path),
                    'size': file_path.stat().st_size,
                    'type': file_path.suffix.lower()
                }
                manifest['files'].append(file_info)
        
        # Save manifest
        manifest_file = site_dir / 'build-manifest.json'
        try:
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
        except Exception as e:
            self.log(f"Error saving manifest: {e}", "WARNING")
        
        return True
    
    def run_production_build(self) -> bool:
        """Run complete production build"""
        
        self.log("🚀 Starting production build process...")
        
        # Record initial size
        site_dir = self.project_dir / "site"
        
        # Build steps
        steps = [
            ("Clean and build site", self.clean_and_build),
            ("Minify HTML files", self.minify_html_files),
            ("Minify CSS files", self.minify_css_files),
            ("Minify JavaScript files", self.minify_js_files),
            ("Optimize images", self.optimize_images),
            ("Create gzip files", self.create_gzip_files),
            ("Generate file hashes", self.generate_file_hashes),
            ("Generate build manifest", self.generate_build_manifest)
        ]
        
        success = True
        
        for step_name, step_func in steps:
            self.log(f"Step: {step_name}")
            
            if not step_func():
                self.log(f"Step failed: {step_name}", "ERROR")
                success = False
                break
        
        # Calculate final statistics
        if success and site_dir.exists():
            final_size = self.calculate_directory_size(site_dir)
            build_time = time.time() - self.build_stats['start_time']
            
            self.log("✅ Production build completed!")
            self.log(f"Build time: {build_time:.2f} seconds")
            self.log(f"Final site size: {final_size / 1024 / 1024:.2f} MB")
            
            if self.build_stats['optimizations']:
                self.log("Optimizations applied:")
                for opt in self.build_stats['optimizations']:
                    self.log(f"  - {opt}")
        
        return success

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="FlutterX Production Build")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--no-minify", action="store_true", help="Skip minification")
    parser.add_argument("--no-gzip", action="store_true", help="Skip gzip compression")
    parser.add_argument("--no-hash", action="store_true", help="Skip file hashing")
    
    args = parser.parse_args()
    
    builder = ProductionBuilder(args.project_dir)
    
    # Override steps based on arguments
    if args.no_minify:
        builder.minify_html_files = lambda: True
        builder.minify_css_files = lambda: True
        builder.minify_js_files = lambda: True
    
    if args.no_gzip:
        builder.create_gzip_files = lambda: True
    
    if args.no_hash:
        builder.generate_file_hashes = lambda: True
    
    success = builder.run_production_build()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()