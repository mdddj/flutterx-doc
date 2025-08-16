#!/usr/bin/env python3
"""
Advanced link validation for built documentation
"""

import re
import requests
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
import time
import json

class LinkValidator:
    def __init__(self, site_dir: str, base_url: str = "http://localhost:8000"):
        self.site_dir = Path(site_dir)
        self.base_url = base_url.rstrip('/')
        self.validation_results = {
            'internal_links': [],
            'external_links': [],
            'images': [],
            'anchors': []
        }
        self.stats = {
            'total_internal_links': 0,
            'total_external_links': 0,
            'total_images': 0,
            'total_anchors': 0,
            'broken_internal': 0,
            'broken_external': 0,
            'broken_images': 0,
            'broken_anchors': 0
        }
        
    def log(self, message: str):
        """Log validation messages"""
        print(message)
    
    def validate_internal_links(self):
        """Validate internal links in HTML files"""
        
        self.log("Validating internal links...")
        
        for html_file in self.site_dir.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all internal links
                link_pattern = r'href=["\']([^"\']+)["\']'
                links = re.findall(link_pattern, content)
                
                for link in links:
                    if self._is_internal_link(link):
                        self.stats['total_internal_links'] += 1
                        
                        if not self._validate_internal_link(link, html_file):
                            self.stats['broken_internal'] += 1
                            self.validation_results['internal_links'].append({
                                'file': str(html_file.relative_to(self.site_dir)),
                                'link': link,
                                'status': 'broken'
                            })
                
            except Exception as e:
                self.log(f"Error processing {html_file}: {e}")
    
    def validate_external_links(self, check_external: bool = False):
        """Validate external links (optional)"""
        
        if not check_external:
            self.log("Skipping external link validation (use --check-external to enable)")
            return
        
        self.log("Validating external links...")
        
        external_links = set()
        
        for html_file in self.site_dir.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all external links
                link_pattern = r'href=["\']([^"\']+)["\']'
                links = re.findall(link_pattern, content)
                
                for link in links:
                    if self._is_external_link(link):
                        external_links.add(link)
                
            except Exception as e:
                self.log(f"Error processing {html_file}: {e}")
        
        # Check each unique external link
        for link in external_links:
            self.stats['total_external_links'] += 1
            
            if not self._validate_external_link(link):
                self.stats['broken_external'] += 1
                self.validation_results['external_links'].append({
                    'link': link,
                    'status': 'broken'
                })
            
            # Rate limiting
            time.sleep(0.1)
    
    def validate_images(self):
        """Validate image links"""
        
        self.log("Validating image links...")
        
        for html_file in self.site_dir.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all image sources
                img_pattern = r'src=["\']([^"\']+)["\']'
                images = re.findall(img_pattern, content)
                
                for img_src in images:
                    self.stats['total_images'] += 1
                    
                    if not self._validate_image(img_src, html_file):
                        self.stats['broken_images'] += 1
                        self.validation_results['images'].append({
                            'file': str(html_file.relative_to(self.site_dir)),
                            'image': img_src,
                            'status': 'broken'
                        })
                
            except Exception as e:
                self.log(f"Error processing {html_file}: {e}")
    
    def validate_anchors(self):
        """Validate anchor links"""
        
        self.log("Validating anchor links...")
        
        # First, collect all available anchors
        available_anchors = {}
        
        for html_file in self.site_dir.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all anchors (id attributes)
                anchor_pattern = r'id=["\']([^"\']+)["\']'
                anchors = re.findall(anchor_pattern, content)
                
                file_key = str(html_file.relative_to(self.site_dir))
                available_anchors[file_key] = set(anchors)
                
            except Exception as e:
                self.log(f"Error processing {html_file}: {e}")
        
        # Now validate anchor links
        for html_file in self.site_dir.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all anchor links
                anchor_pattern = r'href=["\']([^"\']*#[^"\']+)["\']'
                anchor_links = re.findall(anchor_pattern, content)
                
                for link in anchor_links:
                    self.stats['total_anchors'] += 1
                    
                    if not self._validate_anchor_link(link, html_file, available_anchors):
                        self.stats['broken_anchors'] += 1
                        self.validation_results['anchors'].append({
                            'file': str(html_file.relative_to(self.site_dir)),
                            'link': link,
                            'status': 'broken'
                        })
                
            except Exception as e:
                self.log(f"Error processing {html_file}: {e}")
    
    def _is_internal_link(self, link: str) -> bool:
        """Check if link is internal"""
        return not link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#'))
    
    def _is_external_link(self, link: str) -> bool:
        """Check if link is external"""
        return link.startswith(('http://', 'https://'))
    
    def _validate_internal_link(self, link: str, current_file: Path) -> bool:
        """Validate internal link exists"""
        
        # Remove anchor part
        if '#' in link:
            link = link.split('#')[0]
        
        if not link:  # Pure anchor link
            return True
        
        # Resolve relative path
        if link.startswith('/'):
            target_path = self.site_dir / link.lstrip('/')
        else:
            target_path = current_file.parent / link
        
        # Add .html if no extension
        if not target_path.suffix:
            target_path = target_path.with_suffix('.html')
        
        return target_path.exists()
    
    def _validate_external_link(self, link: str) -> bool:
        """Validate external link is accessible"""
        
        try:
            response = requests.head(link, timeout=10, allow_redirects=True)
            return response.status_code < 400
        except Exception:
            try:
                # Try GET if HEAD fails
                response = requests.get(link, timeout=10, allow_redirects=True)
                return response.status_code < 400
            except Exception:
                return False
    
    def _validate_image(self, img_src: str, current_file: Path) -> bool:
        """Validate image exists"""
        
        # Skip external images
        if img_src.startswith(('http://', 'https://')):
            return True  # Assume external images are valid
        
        # Resolve relative path
        if img_src.startswith('/'):
            target_path = self.site_dir / img_src.lstrip('/')
        else:
            target_path = current_file.parent / img_src
        
        return target_path.exists()
    
    def _validate_anchor_link(self, link: str, current_file: Path, available_anchors: Dict) -> bool:
        """Validate anchor link exists"""
        
        if '#' not in link:
            return True
        
        # Split file and anchor
        if link.startswith('#'):
            # Same page anchor
            file_key = str(current_file.relative_to(self.site_dir))
            anchor = link[1:]
        else:
            file_part, anchor = link.split('#', 1)
            
            # Resolve file path
            if file_part.startswith('/'):
                target_file = self.site_dir / file_part.lstrip('/')
            else:
                target_file = current_file.parent / file_part
            
            if not target_file.suffix:
                target_file = target_file.with_suffix('.html')
            
            file_key = str(target_file.relative_to(self.site_dir))
        
        # Check if anchor exists in target file
        return file_key in available_anchors and anchor in available_anchors[file_key]
    
    def generate_validation_report(self):
        """Generate link validation report"""
        
        total_issues = (self.stats['broken_internal'] + 
                       self.stats['broken_external'] + 
                       self.stats['broken_images'] + 
                       self.stats['broken_anchors'])
        
        # Text report
        report_file = Path("link-validation-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Link Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write("Summary:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Internal links: {self.stats['total_internal_links']} ({self.stats['broken_internal']} broken)\n")
            f.write(f"External links: {self.stats['total_external_links']} ({self.stats['broken_external']} broken)\n")
            f.write(f"Images: {self.stats['total_images']} ({self.stats['broken_images']} broken)\n")
            f.write(f"Anchors: {self.stats['total_anchors']} ({self.stats['broken_anchors']} broken)\n")
            f.write(f"Total issues: {total_issues}\n\n")
            
            # Detailed issues
            for category, issues in self.validation_results.items():
                if issues:
                    f.write(f"{category.replace('_', ' ').title()} Issues ({len(issues)}):\n")
                    f.write("-" * 30 + "\n")
                    
                    for issue in issues:
                        if 'file' in issue:
                            f.write(f"File: {issue['file']}\n")
                        
                        if 'link' in issue:
                            f.write(f"Link: {issue['link']}\n")
                        elif 'image' in issue:
                            f.write(f"Image: {issue['image']}\n")
                        
                        f.write(f"Status: {issue['status']}\n")
                        f.write("\n")
        
        # JSON report
        json_report_file = Path("link-validation-report.json")
        
        report_data = {
            'summary': self.stats,
            'issues': self.validation_results
        }
        
        with open(json_report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"Link validation reports saved:")
        self.log(f"  Text report: {report_file}")
        self.log(f"  JSON report: {json_report_file}")
        
        return total_issues
    
    def run_validation(self, check_external: bool = False) -> bool:
        """Run complete link validation"""
        
        self.log("Starting link validation...")
        
        if not self.site_dir.exists():
            self.log(f"❌ Site directory not found: {self.site_dir}")
            return False
        
        try:
            # Run validations
            self.validate_internal_links()
            self.validate_external_links(check_external)
            self.validate_images()
            self.validate_anchors()
            
            # Generate report
            total_issues = self.generate_validation_report()
            
            # Print summary
            self.log(f"\nLink Validation Summary:")
            self.log(f"  Internal links: {self.stats['total_internal_links']} ({self.stats['broken_internal']} broken)")
            self.log(f"  External links: {self.stats['total_external_links']} ({self.stats['broken_external']} broken)")
            self.log(f"  Images: {self.stats['total_images']} ({self.stats['broken_images']} broken)")
            self.log(f"  Anchors: {self.stats['total_anchors']} ({self.stats['broken_anchors']} broken)")
            
            if total_issues == 0:
                self.log("✅ No broken links found!")
                return True
            else:
                self.log(f"❌ Found {total_issues} broken links")
                return False
            
        except Exception as e:
            self.log(f"❌ Link validation failed: {str(e)}")
            return False

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate links in built documentation")
    parser.add_argument("--site-dir", default="site", help="Built site directory")
    parser.add_argument("--check-external", action="store_true", help="Check external links (slow)")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for the site")
    
    args = parser.parse_args()
    
    validator = LinkValidator(args.site_dir, args.base_url)
    success = validator.run_validation(args.check_external)
    
    import sys
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()