#!/usr/bin/env python3
"""
Validate asset references in markdown files
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

class AssetValidator:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.issues = []
        self.stats = {
            'total_files': 0,
            'files_with_images': 0,
            'total_image_refs': 0,
            'broken_refs': 0,
            'valid_refs': 0
        }
    
    def validate_all_assets(self) -> Dict[str, List[str]]:
        """Validate all asset references in markdown files"""
        
        results = {
            'broken_images': [],
            'missing_files': [],
            'valid_references': []
        }
        
        print("Validating asset references...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            self.stats['total_files'] += 1
            file_issues = self._validate_file_assets(md_file)
            
            if file_issues['broken_images']:
                results['broken_images'].extend(file_issues['broken_images'])
                self.stats['files_with_images'] += 1
            
            if file_issues['missing_files']:
                results['missing_files'].extend(file_issues['missing_files'])
            
            if file_issues['valid_references']:
                results['valid_references'].extend(file_issues['valid_references'])
        
        return results
    
    def _validate_file_assets(self, md_file: Path) -> Dict[str, List[str]]:
        """Validate asset references in a single file"""
        
        file_issues = {
            'broken_images': [],
            'missing_files': [],
            'valid_references': []
        }
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all image references
            image_refs = self._extract_image_references(content)
            
            for ref_type, alt_text, image_path in image_refs:
                self.stats['total_image_refs'] += 1
                
                # Resolve the actual file path
                actual_path = self._resolve_image_path(image_path, md_file)
                
                if actual_path and actual_path.exists():
                    file_issues['valid_references'].append(f"{md_file}: {image_path} -> {actual_path}")
                    self.stats['valid_refs'] += 1
                else:
                    file_issues['broken_images'].append(f"{md_file}: Missing image {image_path}")
                    if actual_path:
                        file_issues['missing_files'].append(str(actual_path))
                    self.stats['broken_refs'] += 1
            
        except Exception as e:
            file_issues['broken_images'].append(f"{md_file}: Error reading file - {str(e)}")
        
        return file_issues
    
    def _extract_image_references(self, content: str) -> List[Tuple[str, str, str]]:
        """Extract all image references from content"""
        
        references = []
        
        # Markdown image syntax: ![alt](path)
        md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(md_pattern, content):
            alt_text = match.group(1)
            image_path = match.group(2)
            references.append(('markdown', alt_text, image_path))
        
        # HTML img tags: <img src="path" ...>
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(html_pattern, content):
            image_path = match.group(1)
            references.append(('html', '', image_path))
        
        return references
    
    def _resolve_image_path(self, image_path: str, md_file: Path) -> Path:
        """Resolve the actual file system path for an image reference"""
        
        # Skip external URLs
        if image_path.startswith(('http://', 'https://', 'data:')):
            return None
        
        # Handle absolute paths from docs root
        if image_path.startswith('/'):
            return self.docs_dir / image_path[1:]
        
        # Handle relative paths
        if image_path.startswith('../'):
            # Relative to the markdown file
            return (md_file.parent / image_path).resolve()
        elif image_path.startswith('./'):
            # Relative to the markdown file
            return (md_file.parent / image_path[2:]).resolve()
        else:
            # Relative to the markdown file
            return (md_file.parent / image_path).resolve()
    
    def print_validation_summary(self, results: Dict[str, List[str]]):
        """Print a summary of validation results"""
        
        print("\nAsset Validation Summary")
        print("=" * 40)
        print(f"Total markdown files: {self.stats['total_files']}")
        print(f"Files with images: {self.stats['files_with_images']}")
        print(f"Total image references: {self.stats['total_image_refs']}")
        print(f"Valid references: {self.stats['valid_refs']}")
        print(f"Broken references: {self.stats['broken_refs']}")
        print()
        
        if results['broken_images']:
            print(f"❌ Found {len(results['broken_images'])} broken image references:")
            for issue in results['broken_images'][:10]:  # Show first 10
                print(f"  • {issue}")
            if len(results['broken_images']) > 10:
                print(f"  ... and {len(results['broken_images']) - 10} more")
            print()
        
        if results['missing_files']:
            unique_missing = list(set(results['missing_files']))
            print(f"📁 Missing asset files ({len(unique_missing)}):")
            for missing_file in unique_missing[:10]:  # Show first 10
                print(f"  • {missing_file}")
            if len(unique_missing) > 10:
                print(f"  ... and {len(unique_missing) - 10} more")
            print()
        
        if self.stats['broken_refs'] == 0:
            print("✅ All asset references are valid!")
        else:
            print(f"⚠️  Found {self.stats['broken_refs']} issues that need attention")
    
    def generate_validation_report(self, results: Dict[str, List[str]]):
        """Generate a detailed validation report"""
        
        report_file = self.docs_dir.parent / "asset-validation-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Asset Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write("Summary:\n")
            f.write(f"  Total markdown files: {self.stats['total_files']}\n")
            f.write(f"  Files with images: {self.stats['files_with_images']}\n")
            f.write(f"  Total image references: {self.stats['total_image_refs']}\n")
            f.write(f"  Valid references: {self.stats['valid_refs']}\n")
            f.write(f"  Broken references: {self.stats['broken_refs']}\n\n")
            
            # Broken images
            if results['broken_images']:
                f.write(f"Broken Image References ({len(results['broken_images'])}):\n")
                f.write("-" * 40 + "\n")
                for issue in results['broken_images']:
                    f.write(f"{issue}\n")
                f.write("\n")
            
            # Missing files
            if results['missing_files']:
                unique_missing = list(set(results['missing_files']))
                f.write(f"Missing Asset Files ({len(unique_missing)}):\n")
                f.write("-" * 40 + "\n")
                for missing_file in unique_missing:
                    f.write(f"{missing_file}\n")
                f.write("\n")
            
            # Valid references (sample)
            if results['valid_references']:
                f.write(f"Valid References (sample of {min(20, len(results['valid_references']))}):\n")
                f.write("-" * 40 + "\n")
                for ref in results['valid_references'][:20]:
                    f.write(f"{ref}\n")
                f.write("\n")
        
        print(f"Detailed validation report saved to: {report_file}")
    
    def run_validation(self):
        """Run the complete validation process"""
        
        if not self.docs_dir.exists():
            print(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            results = self.validate_all_assets()
            self.print_validation_summary(results)
            self.generate_validation_report(results)
            
        except Exception as e:
            print(f"❌ Asset validation failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    validator = AssetValidator(docs_dir)
    validator.run_validation()

if __name__ == "__main__":
    main()