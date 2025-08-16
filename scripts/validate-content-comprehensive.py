#!/usr/bin/env python3
"""
Comprehensive content validation for FlutterX documentation
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple
import json

class ContentValidator:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.validation_results = {
            'markdown_issues': [],
            'link_issues': [],
            'image_issues': [],
            'structure_issues': [],
            'language_issues': [],
            'seo_issues': []
        }
        self.stats = {
            'total_files': 0,
            'total_words': 0,
            'total_images': 0,
            'total_links': 0
        }
        
    def log(self, message: str):
        """Log validation messages"""
        print(message)
    
    def validate_markdown_syntax(self):
        """Validate markdown syntax in all files"""
        
        self.log("Validating markdown syntax...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            self.stats['total_files'] += 1
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count words
                word_count = len(content.split())
                self.stats['total_words'] += word_count
                
                # Check for common markdown issues
                issues = self._check_markdown_issues(content, md_file)
                self.validation_results['markdown_issues'].extend(issues)
                
            except Exception as e:
                self.validation_results['markdown_issues'].append({
                    'file': str(md_file),
                    'issue': f"File read error: {str(e)}",
                    'severity': 'error'
                })
    
    def _check_markdown_issues(self, content: str, file_path: Path) -> List[Dict]:
        """Check for markdown syntax issues"""
        
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for unmatched brackets
            if line.count('[') != line.count(']'):
                issues.append({
                    'file': str(file_path),
                    'line': i,
                    'issue': 'Unmatched square brackets',
                    'severity': 'warning',
                    'content': line.strip()
                })
            
            # Check for unmatched parentheses in links
            if '[' in line and ']' in line:
                if line.count('(') != line.count(')'):
                    issues.append({
                        'file': str(file_path),
                        'line': i,
                        'issue': 'Unmatched parentheses in link',
                        'severity': 'warning',
                        'content': line.strip()
                    })
            
            # Check for malformed headers
            if line.startswith('#'):
                if not line.startswith('# ') and len(line) > 1:
                    if not re.match(r'^#+\s+', line):
                        issues.append({
                            'file': str(file_path),
                            'line': i,
                            'issue': 'Malformed header (missing space after #)',
                            'severity': 'warning',
                            'content': line.strip()
                        })
            
            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append({
                    'file': str(file_path),
                    'line': i,
                    'issue': 'Trailing whitespace',
                    'severity': 'info',
                    'content': repr(line)
                })
        
        # Check for missing title (h1)
        if not re.search(r'^#\s+', content, re.MULTILINE):
            issues.append({
                'file': str(file_path),
                'issue': 'Missing main title (h1)',
                'severity': 'warning'
            })
        
        return issues
    
    def validate_links_and_images(self):
        """Validate all links and images"""
        
        self.log("Validating links and images...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Validate links
                link_issues = self._validate_links(content, md_file)
                self.validation_results['link_issues'].extend(link_issues)
                
                # Validate images
                image_issues = self._validate_images(content, md_file)
                self.validation_results['image_issues'].extend(image_issues)
                
            except Exception as e:
                self.validation_results['link_issues'].append({
                    'file': str(md_file),
                    'issue': f"File processing error: {str(e)}",
                    'severity': 'error'
                })
    
    def _validate_links(self, content: str, file_path: Path) -> List[Dict]:
        """Validate links in content"""
        
        issues = []
        
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            self.stats['total_links'] += 1
            
            # Skip external links
            if link_url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
            
            # Skip anchors
            if link_url.startswith('#'):
                continue
            
            # Validate internal links
            if not self._validate_internal_link(link_url, file_path):
                issues.append({
                    'file': str(file_path),
                    'issue': f'Broken internal link: {link_url}',
                    'severity': 'error',
                    'link_text': link_text,
                    'link_url': link_url
                })
        
        return issues
    
    def _validate_images(self, content: str, file_path: Path) -> List[Dict]:
        """Validate images in content"""
        
        issues = []
        
        # Find all image references
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, content)
        
        for alt_text, image_url in images:
            self.stats['total_images'] += 1
            
            # Skip external images
            if image_url.startswith(('http://', 'https://')):
                continue
            
            # Validate internal images
            if not self._validate_internal_image(image_url, file_path):
                issues.append({
                    'file': str(file_path),
                    'issue': f'Missing image: {image_url}',
                    'severity': 'error',
                    'alt_text': alt_text,
                    'image_url': image_url
                })
            
            # Check for missing alt text
            if not alt_text.strip():
                issues.append({
                    'file': str(file_path),
                    'issue': f'Missing alt text for image: {image_url}',
                    'severity': 'warning',
                    'image_url': image_url
                })
        
        return issues
    
    def _validate_internal_link(self, link_url: str, current_file: Path) -> bool:
        """Validate internal link exists"""
        
        # Remove fragment
        if '#' in link_url:
            link_url = link_url.split('#')[0]
        
        if not link_url:
            return True  # Pure anchor link
        
        # Resolve path
        if link_url.startswith('../'):
            target_path = (current_file.parent / link_url).resolve()
        elif link_url.startswith('/'):
            target_path = self.docs_dir / link_url.lstrip('/')
        else:
            target_path = current_file.parent / link_url
        
        return target_path.exists()
    
    def _validate_internal_image(self, image_url: str, current_file: Path) -> bool:
        """Validate internal image exists"""
        
        # Resolve path
        if image_url.startswith('../'):
            target_path = (current_file.parent / image_url).resolve()
        elif image_url.startswith('/'):
            target_path = self.docs_dir / image_url.lstrip('/')
        else:
            target_path = current_file.parent / image_url
        
        return target_path.exists()
    
    def validate_structure(self):
        """Validate documentation structure"""
        
        self.log("Validating documentation structure...")
        
        # Check for required files
        required_files = [
            'index.md',
            'zh/index.md',
            'en/index.md',
            'ja/index.md'
        ]
        
        for required_file in required_files:
            file_path = self.docs_dir / required_file
            if not file_path.exists():
                self.validation_results['structure_issues'].append({
                    'issue': f'Missing required file: {required_file}',
                    'severity': 'error'
                })
        
        # Check for empty directories
        for dir_path in self.docs_dir.rglob('*'):
            if dir_path.is_dir():
                if not any(dir_path.iterdir()):
                    self.validation_results['structure_issues'].append({
                        'issue': f'Empty directory: {dir_path.relative_to(self.docs_dir)}',
                        'severity': 'warning'
                    })
    
    def validate_language_consistency(self):
        """Validate consistency across languages"""
        
        self.log("Validating language consistency...")
        
        languages = ['zh', 'en', 'ja']
        
        # Get file structure for each language
        lang_files = {}
        for lang in languages:
            lang_dir = self.docs_dir / lang
            if lang_dir.exists():
                lang_files[lang] = set(
                    str(f.relative_to(lang_dir)) 
                    for f in lang_dir.rglob("*.md")
                )
        
        # Check for missing translations
        if len(lang_files) > 1:
            all_files = set()
            for files in lang_files.values():
                all_files.update(files)
            
            for lang, files in lang_files.items():
                missing_files = all_files - files
                for missing_file in missing_files:
                    self.validation_results['language_issues'].append({
                        'issue': f'Missing translation in {lang}: {missing_file}',
                        'severity': 'warning',
                        'language': lang,
                        'file': missing_file
                    })
    
    def validate_seo_elements(self):
        """Validate SEO elements"""
        
        self.log("Validating SEO elements...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for title
                if not re.search(r'^#\s+.+', content, re.MULTILINE):
                    self.validation_results['seo_issues'].append({
                        'file': str(md_file),
                        'issue': 'Missing main heading (important for SEO)',
                        'severity': 'warning'
                    })
                
                # Check content length
                word_count = len(content.split())
                if word_count < 50:
                    self.validation_results['seo_issues'].append({
                        'file': str(md_file),
                        'issue': f'Very short content ({word_count} words)',
                        'severity': 'info'
                    })
                
            except Exception as e:
                continue
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        
        # Calculate summary
        total_issues = sum(len(issues) for issues in self.validation_results.values())
        error_count = sum(1 for issues in self.validation_results.values() 
                         for issue in issues if issue.get('severity') == 'error')
        warning_count = sum(1 for issues in self.validation_results.values() 
                           for issue in issues if issue.get('severity') == 'warning')
        
        # Generate text report
        report_file = Path("comprehensive-validation-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Comprehensive Content Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write("Summary:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total files: {self.stats['total_files']}\n")
            f.write(f"Total words: {self.stats['total_words']:,}\n")
            f.write(f"Total images: {self.stats['total_images']}\n")
            f.write(f"Total links: {self.stats['total_links']}\n")
            f.write(f"Total issues: {total_issues}\n")
            f.write(f"Errors: {error_count}\n")
            f.write(f"Warnings: {warning_count}\n\n")
            
            # Detailed issues
            for category, issues in self.validation_results.items():
                if issues:
                    f.write(f"{category.replace('_', ' ').title()} ({len(issues)}):\n")
                    f.write("-" * 30 + "\n")
                    
                    for issue in issues:
                        severity = issue.get('severity', 'info').upper()
                        f.write(f"[{severity}] ")
                        
                        if 'file' in issue:
                            f.write(f"{issue['file']}: ")
                        
                        if 'line' in issue:
                            f.write(f"Line {issue['line']}: ")
                        
                        f.write(f"{issue['issue']}\n")
                        
                        if 'content' in issue:
                            f.write(f"  Content: {issue['content']}\n")
                    
                    f.write("\n")
        
        # Generate JSON report
        json_report_file = Path("validation-report.json")
        
        report_data = {
            'summary': {
                'total_files': self.stats['total_files'],
                'total_words': self.stats['total_words'],
                'total_images': self.stats['total_images'],
                'total_links': self.stats['total_links'],
                'total_issues': total_issues,
                'error_count': error_count,
                'warning_count': warning_count
            },
            'issues': self.validation_results
        }
        
        with open(json_report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"Validation reports saved:")
        self.log(f"  Text report: {report_file}")
        self.log(f"  JSON report: {json_report_file}")
        
        return total_issues, error_count, warning_count
    
    def run_validation(self) -> bool:
        """Run comprehensive validation"""
        
        self.log("Starting comprehensive content validation...")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return False
        
        try:
            # Run all validations
            self.validate_markdown_syntax()
            self.validate_links_and_images()
            self.validate_structure()
            self.validate_language_consistency()
            self.validate_seo_elements()
            
            # Generate report
            total_issues, error_count, warning_count = self.generate_validation_report()
            
            # Print summary
            self.log(f"\nValidation Summary:")
            self.log(f"  Files processed: {self.stats['total_files']}")
            self.log(f"  Total issues: {total_issues}")
            self.log(f"  Errors: {error_count}")
            self.log(f"  Warnings: {warning_count}")
            
            if error_count == 0:
                self.log("✅ No critical errors found!")
                return True
            else:
                self.log(f"❌ Found {error_count} critical errors")
                return False
            
        except Exception as e:
            self.log(f"❌ Validation failed: {str(e)}")
            return False

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive content validation")
    parser.add_argument("--docs-dir", default="docs", help="Documentation directory")
    
    args = parser.parse_args()
    
    validator = ContentValidator(args.docs_dir)
    success = validator.run_validation()
    
    import sys
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()