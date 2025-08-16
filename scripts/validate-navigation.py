#!/usr/bin/env python3
"""
Validate navigation structure in mkdocs.yml
"""

import re
from pathlib import Path
from typing import List, Dict, Set

class NavigationValidator:
    def __init__(self, mkdocs_config_path: str, docs_dir: str):
        self.mkdocs_config_path = Path(mkdocs_config_path)
        self.docs_dir = Path(docs_dir)
        self.issues = []
        self.stats = {
            'total_nav_items': 0,
            'valid_links': 0,
            'broken_links': 0,
            'missing_files': 0
        }
    
    def log(self, message: str):
        """Log validation messages"""
        print(message)
        self.issues.append(message)
    
    def extract_navigation_links(self) -> List[str]:
        """Extract all navigation links from mkdocs.yml"""
        
        self.log("Extracting navigation links from mkdocs.yml...")
        
        with open(self.mkdocs_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the nav section
        nav_match = re.search(r'nav:\s*\n(.*?)(?=\n\w|\n#|\Z)', content, re.DOTALL)
        if not nav_match:
            self.log("⚠️  No navigation section found in mkdocs.yml")
            return []
        
        nav_content = nav_match.group(1)
        
        # Extract all .md file references
        md_links = re.findall(r':\s*([^:\n]+\.md)', nav_content)
        
        self.log(f"✅ Found {len(md_links)} navigation links")
        return md_links
    
    def validate_navigation_files(self, nav_links: List[str]) -> Dict[str, List[str]]:
        """Validate that all navigation files exist"""
        
        self.log("Validating navigation file references...")
        
        results = {
            'valid_files': [],
            'missing_files': [],
            'broken_links': []
        }
        
        for link in nav_links:
            self.stats['total_nav_items'] += 1
            
            # Clean up the link
            clean_link = link.strip()
            
            # Resolve file path
            file_path = self.docs_dir / clean_link
            
            if file_path.exists():
                results['valid_files'].append(clean_link)
                self.stats['valid_links'] += 1
            else:
                results['missing_files'].append(clean_link)
                results['broken_links'].append(f"Missing file: {clean_link} -> {file_path}")
                self.stats['broken_links'] += 1
                self.stats['missing_files'] += 1
        
        return results
    
    def find_orphaned_files(self, nav_links: List[str]) -> List[str]:
        """Find markdown files that are not referenced in navigation"""
        
        self.log("Finding orphaned markdown files...")
        
        # Get all markdown files in docs directory
        all_md_files = set()
        for md_file in self.docs_dir.rglob("*.md"):
            relative_path = md_file.relative_to(self.docs_dir)
            all_md_files.add(str(relative_path))
        
        # Get navigation files
        nav_files = set(link.strip() for link in nav_links)
        
        # Find orphaned files
        orphaned = all_md_files - nav_files
        
        self.log(f"Found {len(orphaned)} orphaned files")
        return list(orphaned)
    
    def validate_navigation_structure(self) -> Dict[str, List[str]]:
        """Validate the overall navigation structure"""
        
        self.log("Validating navigation structure...")
        
        with open(self.mkdocs_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for duplicate nav sections
        nav_sections = re.findall(r'^nav:', content, re.MULTILINE)
        if len(nav_sections) > 1:
            issues.append(f"Found {len(nav_sections)} nav sections - should be only 1")
        
        # Check for proper YAML indentation
        nav_match = re.search(r'nav:\s*\n(.*?)(?=\n\w|\n#|\Z)', content, re.DOTALL)
        if nav_match:
            nav_content = nav_match.group(1)
            lines = nav_content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith('  '):
                    if not line.startswith('#'):  # Ignore comments
                        issues.append(f"Line {i}: Improper indentation - '{line.strip()}'")
        
        return {'structure_issues': issues}
    
    def print_validation_summary(self, file_results: Dict[str, List[str]], orphaned_files: List[str], structure_results: Dict[str, List[str]]):
        """Print validation summary"""
        
        print("\nNavigation Validation Summary")
        print("=" * 40)
        print(f"Total navigation items: {self.stats['total_nav_items']}")
        print(f"Valid file references: {self.stats['valid_links']}")
        print(f"Broken file references: {self.stats['broken_links']}")
        print(f"Orphaned files: {len(orphaned_files)}")
        print()
        
        if file_results['missing_files']:
            print(f"❌ Missing Files ({len(file_results['missing_files'])}):")
            for missing_file in file_results['missing_files'][:10]:
                print(f"  • {missing_file}")
            if len(file_results['missing_files']) > 10:
                print(f"  ... and {len(file_results['missing_files']) - 10} more")
            print()
        
        if orphaned_files:
            print(f"📁 Orphaned Files ({len(orphaned_files)}):")
            for orphaned_file in orphaned_files[:10]:
                print(f"  • {orphaned_file}")
            if len(orphaned_files) > 10:
                print(f"  ... and {len(orphaned_files) - 10} more")
            print()
        
        if structure_results['structure_issues']:
            print(f"⚠️  Structure Issues ({len(structure_results['structure_issues'])}):")
            for issue in structure_results['structure_issues']:
                print(f"  • {issue}")
            print()
        
        if (self.stats['broken_links'] == 0 and 
            len(orphaned_files) == 0 and 
            len(structure_results['structure_issues']) == 0):
            print("✅ Navigation structure is valid!")
        else:
            total_issues = (self.stats['broken_links'] + 
                          len(orphaned_files) + 
                          len(structure_results['structure_issues']))
            print(f"⚠️  Found {total_issues} issues that need attention")
    
    def generate_validation_report(self, file_results: Dict[str, List[str]], orphaned_files: List[str], structure_results: Dict[str, List[str]]):
        """Generate detailed validation report"""
        
        report_file = Path("navigation-validation-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Navigation Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write("Summary:\n")
            f.write(f"  Total navigation items: {self.stats['total_nav_items']}\n")
            f.write(f"  Valid file references: {self.stats['valid_links']}\n")
            f.write(f"  Broken file references: {self.stats['broken_links']}\n")
            f.write(f"  Orphaned files: {len(orphaned_files)}\n\n")
            
            # Missing files
            if file_results['missing_files']:
                f.write(f"Missing Files ({len(file_results['missing_files'])}):\n")
                f.write("-" * 30 + "\n")
                for missing_file in file_results['missing_files']:
                    f.write(f"{missing_file}\n")
                f.write("\n")
            
            # Orphaned files
            if orphaned_files:
                f.write(f"Orphaned Files ({len(orphaned_files)}):\n")
                f.write("-" * 30 + "\n")
                for orphaned_file in orphaned_files:
                    f.write(f"{orphaned_file}\n")
                f.write("\n")
            
            # Structure issues
            if structure_results['structure_issues']:
                f.write(f"Structure Issues ({len(structure_results['structure_issues'])}):\n")
                f.write("-" * 30 + "\n")
                for issue in structure_results['structure_issues']:
                    f.write(f"{issue}\n")
                f.write("\n")
            
            # Valid files (sample)
            if file_results['valid_files']:
                f.write(f"Valid Files (sample of {min(20, len(file_results['valid_files']))}):\n")
                f.write("-" * 30 + "\n")
                for valid_file in file_results['valid_files'][:20]:
                    f.write(f"{valid_file}\n")
                f.write("\n")
        
        self.log(f"Validation report saved to: {report_file}")
    
    def run_validation(self):
        """Run complete navigation validation"""
        
        if not self.mkdocs_config_path.exists():
            self.log(f"❌ MkDocs config not found: {self.mkdocs_config_path}")
            return
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            # Extract navigation links
            nav_links = self.extract_navigation_links()
            
            # Validate file references
            file_results = self.validate_navigation_files(nav_links)
            
            # Find orphaned files
            orphaned_files = self.find_orphaned_files(nav_links)
            
            # Validate structure
            structure_results = self.validate_navigation_structure()
            
            # Print summary
            self.print_validation_summary(file_results, orphaned_files, structure_results)
            
            # Generate report
            self.generate_validation_report(file_results, orphaned_files, structure_results)
            
        except Exception as e:
            self.log(f"❌ Navigation validation failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    mkdocs_config = "mkdocs.yml"
    docs_dir = "docs"
    
    validator = NavigationValidator(mkdocs_config, docs_dir)
    validator.run_validation()

if __name__ == "__main__":
    main()