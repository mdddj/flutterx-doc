#!/usr/bin/env python3
"""
Update image paths in markdown files for mkdocs compatibility
"""

import re
from pathlib import Path
from typing import List, Tuple

class ImagePathUpdater:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.updated_files = []
        self.update_log = []
    
    def log(self, message: str):
        """Log update messages"""
        print(message)
        self.update_log.append(message)
    
    def update_all_markdown_files(self):
        """Update image paths in all markdown files"""
        
        self.log("Updating image paths in markdown files...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            if self.update_file_image_paths(md_file):
                self.updated_files.append(md_file)
        
        self.log(f"✅ Updated {len(self.updated_files)} files")
    
    def update_file_image_paths(self, md_file: Path) -> bool:
        """Update image paths in a single markdown file"""
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Calculate relative path to assets directory
            relative_to_docs = md_file.relative_to(self.docs_dir)
            depth = len(relative_to_docs.parts) - 1
            assets_prefix = "../" * depth + "assets/"
            
            # Update various image reference patterns
            content = self._update_image_references(content, assets_prefix)
            
            # Only write if content changed
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes = self._count_changes(original_content, content)
                self.log(f"✅ Updated {md_file} ({changes} changes)")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error updating {md_file}: {str(e)}")
            return False
    
    def _update_image_references(self, content: str, assets_prefix: str) -> str:
        """Update image references in content"""
        
        # Define replacement patterns
        patterns = [
            # ![alt](/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(/images/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](/public/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(/public/images/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](../public/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(\.\.\/public\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](./public/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(\.\/public\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](/gif/path) -> ![alt](../assets/gif/path)
            (r'!\[([^\]]*)\]\(/gif/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
            
            # ![alt](/public/gif/path) -> ![alt](../assets/gif/path)
            (r'!\[([^\]]*)\]\(/public/gif/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
            
            # ![alt](../public/gif/path) -> ![alt](../assets/gif/path)
            (r'!\[([^\]]*)\]\(\.\.\/public\/gif\/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
            
            # ![alt](/videos/path) -> ![alt](../assets/videos/path)
            (r'!\[([^\]]*)\]\(/videos/([^)]+)\)', rf'![\1]({assets_prefix}videos/\2)'),
            
            # ![alt](/public/videos/path) -> ![alt](../assets/videos/path)
            (r'!\[([^\]]*)\]\(/public/videos/([^)]+)\)', rf'![\1]({assets_prefix}videos/\2)'),
            
            # ![alt](../public/videos/path) -> ![alt](../assets/videos/path)
            (r'!\[([^\]]*)\]\(\.\.\/public\/videos\/([^)]+)\)', rf'![\1]({assets_prefix}videos/\2)'),
            
            # Handle HTML img tags as well
            (r'<img[^>]+src="/images/([^"]+)"', rf'<img src="{assets_prefix}images/\1"'),
            (r'<img[^>]+src="/public/images/([^"]+)"', rf'<img src="{assets_prefix}images/\1"'),
            (r'<img[^>]+src="../public/images/([^"]+)"', rf'<img src="{assets_prefix}images/\1"'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _count_changes(self, original: str, updated: str) -> int:
        """Count the number of changes made"""
        
        # Simple change counting by comparing lines
        original_lines = original.split('\n')
        updated_lines = updated.split('\n')
        
        changes = 0
        for orig, upd in zip(original_lines, updated_lines):
            if orig != upd:
                changes += 1
        
        return changes
    
    def generate_update_report(self):
        """Generate an update report"""
        
        report_file = self.docs_dir.parent / "image-path-update-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Image Path Update Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total files updated: {len(self.updated_files)}\n\n")
            
            f.write("Updated Files:\n")
            f.write("-" * 30 + "\n")
            
            for file_path in self.updated_files:
                f.write(f"{file_path}\n")
            
            f.write("\nUpdate Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.update_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Update report saved to: {report_file}")
    
    def run_update(self):
        """Run the complete update process"""
        
        self.log("Starting image path updates...")
        self.log(f"Docs directory: {self.docs_dir}")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            self.update_all_markdown_files()
            self.generate_update_report()
            
            self.log("✅ Image path update completed successfully!")
            
        except Exception as e:
            self.log(f"❌ Image path update failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    if not Path(docs_dir).exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return
    
    updater = ImagePathUpdater(docs_dir)
    updater.run_update()

if __name__ == "__main__":
    main()