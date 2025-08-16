#!/usr/bin/env python3
"""
Content validation script for migrated files
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

class ContentValidator:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.issues = []
        self.languages = ["zh", "en", "ja"]
    
    def validate_all_content(self) -> Dict[str, List[str]]:
        """Validate all content in the docs directory"""
        
        results = {
            "broken_links": [],
            "missing_images": [],
            "syntax_issues": [],
            "encoding_issues": []
        }
        
        for lang in self.languages:
            lang_dir = self.docs_dir / lang
            if lang_dir.exists():
                self._validate_language_content(lang_dir, results)
        
        return results
    
    def _validate_language_content(self, lang_dir: Path, results: Dict[str, List[str]]):
        """Validate content for a specific language"""
        
        for md_file in lang_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for broken internal links
                broken_links = self._check_internal_links(content, md_file)
                results["broken_links"].extend(broken_links)
                
                # Check for missing images
                missing_images = self._check_image_references(content, md_file)
                results["missing_images"].extend(missing_images)
                
                # Check for syntax issues
                syntax_issues = self._check_markdown_syntax(content, md_file)
                results["syntax_issues"].extend(syntax_issues)
                
            except UnicodeDecodeError:
                results["encoding_issues"].append(str(md_file))
            except Exception as e:
                results["syntax_issues"].append(f"{md_file}: {str(e)}")
    
    def _check_internal_links(self, content: str, file_path: Path) -> List[str]:
        """Check for broken internal links"""
        
        issues = []
        
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # Skip external links
            if link_url.startswith(('http://', 'https://', 'mailto:')):
                continue
            
            # Skip anchor links
            if link_url.startswith('#'):
                continue
            
            # Check if internal link exists
            if link_url.endswith('.md'):
                # Resolve relative path
                if link_url.startswith('../'):
                    target_path = file_path.parent.parent / link_url[3:]
                elif link_url.startswith('./'):
                    target_path = file_path.parent / link_url[2:]
                else:
                    target_path = file_path.parent / link_url
                
                if not target_path.exists():
                    issues.append(f"{file_path}: Broken link to {link_url}")
        
        return issues
    
    def _check_image_references(self, content: str, file_path: Path) -> List[str]:
        """Check for missing image references"""
        
        issues = []
        
        # Find all image references
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, content)
        
        for alt_text, image_url in images:
            # Skip external images
            if image_url.startswith(('http://', 'https://')):
                continue
            
            # Check if image file exists
            if image_url.startswith('../'):
                target_path = file_path.parent.parent / image_url[3:]
            elif image_url.startswith('./'):
                target_path = file_path.parent / image_url[2:]
            else:
                target_path = file_path.parent / image_url
            
            if not target_path.exists():
                issues.append(f"{file_path}: Missing image {image_url}")
        
        return issues
    
    def _check_markdown_syntax(self, content: str, file_path: Path) -> List[str]:
        """Check for basic markdown syntax issues"""
        
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for unmatched brackets
            if line.count('[') != line.count(']'):
                issues.append(f"{file_path}:{i}: Unmatched square brackets")
            
            if line.count('(') != line.count(')'):
                issues.append(f"{file_path}:{i}: Unmatched parentheses")
            
            # Check for malformed links
            if '[' in line and ']' in line and '(' in line and ')' in line:
                # Basic check for malformed markdown links
                link_pattern = r'\[[^\]]*\]\([^)]*\)'
                if not re.search(link_pattern, line) and '[' in line and '](' in line:
                    issues.append(f"{file_path}:{i}: Possibly malformed link")
        
        return issues
    
    def generate_validation_report(self, results: Dict[str, List[str]], output_file: str):
        """Generate a validation report"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Content Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            total_issues = sum(len(issues) for issues in results.values())
            f.write(f"Total issues found: {total_issues}\n\n")
            
            for category, issues in results.items():
                f.write(f"{category.replace('_', ' ').title()}: {len(issues)} issues\n")
                f.write("-" * 30 + "\n")
                
                for issue in issues:
                    f.write(f"  • {issue}\n")
                
                f.write("\n")
        
        print(f"Validation report saved to: {output_file}")

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    if not Path(docs_dir).exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return
    
    validator = ContentValidator(docs_dir)
    results = validator.validate_all_content()
    
    # Print summary
    total_issues = sum(len(issues) for issues in results.values())
    print(f"Content validation complete. Found {total_issues} issues:")
    
    for category, issues in results.items():
        print(f"  {category.replace('_', ' ').title()}: {len(issues)}")
    
    # Generate detailed report
    validator.generate_validation_report(results, "content-validation-report.txt")

if __name__ == "__main__":
    main()