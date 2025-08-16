#!/usr/bin/env python3
"""
Fix image links to point to correct asset locations
"""

import re
from pathlib import Path
from typing import Dict, List, Set

class ImageLinkFixer:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.assets_dir = self.docs_dir / "assets"
        self.fixed_files = []
        self.fix_log = []
        self.image_mappings = {}
        
    def log(self, message: str):
        """Log fix messages"""
        print(message)
        self.fix_log.append(message)
    
    def build_image_mappings(self):
        """Build mappings of image filenames to their actual locations"""
        
        self.log("Building image mappings...")
        
        # Scan all image files in assets directory
        for image_file in self.assets_dir.rglob("*"):
            if image_file.is_file() and image_file.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}:
                filename = image_file.name
                relative_path = image_file.relative_to(self.docs_dir)
                
                # Map filename to relative path from docs root
                self.image_mappings[filename] = str(relative_path)
        
        self.log(f"✅ Built mappings for {len(self.image_mappings)} images")
    
    def fix_all_image_links(self):
        """Fix image links in all markdown files"""
        
        self.log("Fixing image links in all markdown files...")
        
        # Build image mappings first
        self.build_image_mappings()
        
        for md_file in self.docs_dir.rglob("*.md"):
            if self.fix_file_image_links(md_file):
                self.fixed_files.append(md_file)
        
        self.log(f"✅ Fixed image links in {len(self.fixed_files)} files")
    
    def fix_file_image_links(self, md_file: Path) -> bool:
        """Fix image links in a single file"""
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix image links
            content = self._fix_image_references(content, md_file)
            
            # Only write if content changed
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes = self._count_changes(original_content, content)
                self.log(f"✅ Fixed {md_file} ({changes} image link changes)")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error fixing {md_file}: {str(e)}")
            return False
    
    def _fix_image_references(self, content: str, md_file: Path) -> str:
        """Fix image references in content"""
        
        def replace_image(match):
            alt_text = match.group(1)
            image_url = match.group(2)
            
            # Skip external images
            if image_url.startswith(('http://', 'https://')):
                return match.group(0)
            
            # Try to fix the image URL
            fixed_url = self._fix_image_url(image_url, md_file)
            if fixed_url != image_url:
                return f"![{alt_text}]({fixed_url})"
            
            return match.group(0)
        
        # Fix markdown image syntax
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
        
        # Fix HTML img tags
        def replace_html_img(match):
            full_tag = match.group(0)
            src_url = match.group(1)
            
            # Skip external images
            if src_url.startswith(('http://', 'https://')):
                return full_tag
            
            # Try to fix the image URL
            fixed_url = self._fix_image_url(src_url, md_file)
            if fixed_url != src_url:
                return full_tag.replace(f'src="{src_url}"', f'src="{fixed_url}"')
            
            return full_tag
        
        content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', replace_html_img, content)
        
        return content
    
    def _fix_image_url(self, image_url: str, md_file: Path) -> str:
        """Fix a single image URL"""
        
        # Extract filename from URL
        filename = Path(image_url).name
        
        # Check if we have a mapping for this filename
        if filename in self.image_mappings:
            correct_path = self.image_mappings[filename]
            
            # Calculate relative path from current file to the image
            relative_path = md_file.relative_to(self.docs_dir)
            depth = len(relative_path.parts) - 1
            
            # Build correct relative path
            if depth > 0:
                prefix = '../' * depth
                return prefix + correct_path
            else:
                return correct_path
        
        # If no direct mapping, try to fix common path issues
        return self._fix_common_path_issues(image_url, md_file)
    
    def _fix_common_path_issues(self, image_url: str, md_file: Path) -> str:
        """Fix common path issues in image URLs"""
        
        # Calculate correct assets prefix
        relative_path = md_file.relative_to(self.docs_dir)
        depth = len(relative_path.parts) - 1
        assets_prefix = '../' * depth + 'assets/'
        
        # Common fixes
        fixes = [
            # Fix subdirectory references that are now flattened
            (r'assets/images/[^/]+/([^/]+)$', rf'{assets_prefix}images/\1'),
            (r'\.\.\/assets/images/[^/]+/([^/]+)$', rf'{assets_prefix}images/\1'),
            (r'\.\.\/\.\.\/assets/images/[^/]+/([^/]+)$', rf'{assets_prefix}images/\1'),
            
            # Fix gif references
            (r'assets/gif/([^/]+)$', rf'{assets_prefix}gif/\1'),
            (r'\.\.\/assets/gif/([^/]+)$', rf'{assets_prefix}gif/\1'),
            (r'\.\.\/\.\.\/assets/gif/([^/]+)$', rf'{assets_prefix}gif/\1'),
            
            # Fix videos references (now in gif directory)
            (r'assets/videos/([^/]+)$', rf'{assets_prefix}gif/\1'),
            (r'\.\.\/assets/videos/([^/]+)$', rf'{assets_prefix}gif/\1'),
            (r'\.\.\/\.\.\/assets/videos/([^/]+)$', rf'{assets_prefix}gif/\1'),
        ]
        
        for pattern, replacement in fixes:
            if re.search(pattern, image_url):
                return re.sub(pattern, replacement, image_url)
        
        # If no specific fix, try to normalize the path
        if 'assets/' in image_url:
            # Extract the part after assets/
            assets_part = image_url.split('assets/', 1)[1]
            return assets_prefix + assets_part
        
        return image_url
    
    def _count_changes(self, original: str, updated: str) -> int:
        """Count the number of changes made"""
        
        original_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', original)
        updated_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', updated)
        
        changes = 0
        for orig_img, upd_img in zip(original_images, updated_images):
            if orig_img[1] != upd_img[1]:  # Compare URLs
                changes += 1
        
        return changes
    
    def validate_fixed_images(self):
        """Validate that fixed image links are correct"""
        
        self.log("Validating fixed image links...")
        
        validation_issues = []
        valid_images = 0
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all image references
                images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
                
                for alt_text, image_url in images:
                    if not image_url.startswith(('http://', 'https://')):
                        # Check if internal image exists
                        if self._validate_image_link(image_url, md_file):
                            valid_images += 1
                        else:
                            validation_issues.append(f"{md_file}: Missing image {image_url}")
                
            except Exception as e:
                validation_issues.append(f"{md_file}: Error reading file - {str(e)}")
        
        self.log(f"✅ Validated {valid_images} image links")
        
        if validation_issues:
            self.log(f"⚠️  Found {len(validation_issues)} image validation issues")
            for issue in validation_issues[:10]:  # Show first 10
                self.log(f"  • {issue}")
            if len(validation_issues) > 10:
                self.log(f"  ... and {len(validation_issues) - 10} more")
        else:
            self.log("✅ All image links are valid")
        
        return validation_issues
    
    def _validate_image_link(self, image_url: str, current_file: Path) -> bool:
        """Validate that an image link points to an existing file"""
        
        # Resolve path
        if image_url.startswith('../'):
            target_path = (current_file.parent / image_url).resolve()
        elif image_url.startswith('/'):
            target_path = self.docs_dir / image_url.lstrip('/')
        else:
            target_path = current_file.parent / image_url
        
        return target_path.exists()
    
    def generate_fix_report(self):
        """Generate a fix report"""
        
        report_file = Path("image-links-fix-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Image Links Fix Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total files fixed: {len(self.fixed_files)}\n")
            f.write(f"Total image mappings: {len(self.image_mappings)}\n\n")
            
            if self.fixed_files:
                f.write("Fixed Files:\n")
                f.write("-" * 30 + "\n")
                for file_path in self.fixed_files:
                    f.write(f"{file_path}\n")
                f.write("\n")
            
            f.write("Image Mappings (sample):\n")
            f.write("-" * 30 + "\n")
            for filename, path in list(self.image_mappings.items())[:20]:
                f.write(f"{filename} -> {path}\n")
            f.write("\n")
            
            f.write("Fix Log:\n")
            f.write("-" * 30 + "\n")
            for log_entry in self.fix_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Fix report saved to: {report_file}")
    
    def run_fix(self):
        """Run the complete image links fix process"""
        
        self.log("Starting image links fix...")
        self.log(f"Docs directory: {self.docs_dir}")
        self.log(f"Assets directory: {self.assets_dir}")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        if not self.assets_dir.exists():
            self.log(f"❌ Assets directory not found: {self.assets_dir}")
            return
        
        try:
            # Fix all image links
            self.fix_all_image_links()
            
            # Validate fixed links
            validation_issues = self.validate_fixed_images()
            
            # Generate report
            self.generate_fix_report()
            
            self.log("✅ Image links fix completed!")
            
            if validation_issues:
                self.log(f"⚠️  Please review {len(validation_issues)} remaining issues")
            
        except Exception as e:
            self.log(f"❌ Image links fix failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    if not Path(docs_dir).exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return
    
    fixer = ImageLinkFixer(docs_dir)
    fixer.run_fix()

if __name__ == "__main__":
    main()