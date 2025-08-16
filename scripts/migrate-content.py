#!/usr/bin/env python3
"""
Content migration script from rspress to mkdocs-material
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple

class ContentMigrator:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.languages = ["zh", "en", "ja"]
        self.migration_log = []
        
    def log(self, message: str):
        """Log migration messages"""
        print(message)
        self.migration_log.append(message)
    
    def create_target_structure(self):
        """Create target directory structure"""
        self.log("Creating target directory structure...")
        
        for lang in self.languages:
            lang_dir = self.target_dir / "docs" / lang
            lang_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"✅ Created directory: {lang_dir}")
    
    def migrate_markdown_files(self):
        """Migrate markdown files from source to target"""
        self.log("Migrating markdown files...")
        
        for lang in self.languages:
            source_lang_dir = self.source_dir / "docs" / lang
            target_lang_dir = self.target_dir / "docs" / lang
            
            if not source_lang_dir.exists():
                self.log(f"⚠️  Source language directory not found: {source_lang_dir}")
                continue
            
            self.log(f"Processing language: {lang}")
            self._copy_directory_recursive(source_lang_dir, target_lang_dir)
    
    def _copy_directory_recursive(self, source: Path, target: Path):
        """Recursively copy directory contents"""
        if not source.exists():
            return
            
        target.mkdir(parents=True, exist_ok=True)
        
        for item in source.iterdir():
            if item.is_file() and item.suffix == '.md':
                target_file = target / item.name
                self._copy_and_process_markdown(item, target_file)
            elif item.is_dir() and item.name != '__pycache__':
                self._copy_directory_recursive(item, target / item.name)
    
    def _copy_and_process_markdown(self, source_file: Path, target_file: Path):
        """Copy and process a markdown file"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process the content
            processed_content = self._process_markdown_content(content, source_file)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            self.log(f"✅ Migrated: {source_file} -> {target_file}")
            
        except Exception as e:
            self.log(f"❌ Error migrating {source_file}: {str(e)}")
    
    def _process_markdown_content(self, content: str, source_file: Path) -> str:
        """Process markdown content for mkdocs compatibility"""
        
        # Update image paths
        content = self._update_image_paths(content)
        
        # Update internal links
        content = self._update_internal_links(content)
        
        # Remove rspress-specific frontmatter or syntax
        content = self._clean_rspress_syntax(content)
        
        return content
    
    def _update_image_paths(self, content: str) -> str:
        """Update image paths to work with mkdocs structure"""
        
        # Pattern to match image references
        image_patterns = [
            r'!\[([^\]]*)\]\(/images/([^)]+)\)',  # ![alt](/images/path)
            r'!\[([^\]]*)\]\(\.\.\/public\/images\/([^)]+)\)',  # ![alt](../public/images/path)
            r'!\[([^\]]*)\]\(\/public\/images\/([^)]+)\)',  # ![alt](/public/images/path)
        ]
        
        for pattern in image_patterns:
            def replace_image(match):
                alt_text = match.group(1)
                image_path = match.group(2)
                # Convert to mkdocs asset path
                new_path = f"../assets/images/{image_path}"
                return f"![{alt_text}]({new_path})"
            
            content = re.sub(pattern, replace_image, content)
        
        return content
    
    def _update_internal_links(self, content: str) -> str:
        """Update internal links to work with mkdocs structure"""
        
        # Pattern to match internal links
        link_patterns = [
            r'\[([^\]]+)\]\(\/([^)]+)\.md\)',  # [text](/path.md)
            r'\[([^\]]+)\]\(\.\.\/([^)]+)\.md\)',  # [text](../path.md)
            r'\[([^\]]+)\]\(([^)]+)\.md\)',  # [text](path.md)
        ]
        
        for pattern in link_patterns:
            def replace_link(match):
                link_text = match.group(1)
                link_path = match.group(2)
                
                # Clean up the path
                if link_path.startswith('/'):
                    link_path = link_path[1:]
                
                # Keep the .md extension for mkdocs
                new_path = f"{link_path}.md"
                return f"[{link_text}]({new_path})"
            
            content = re.sub(pattern, replace_link, content)
        
        return content
    
    def _clean_rspress_syntax(self, content: str) -> str:
        """Remove rspress-specific syntax"""
        
        # Remove rspress-specific frontmatter that might conflict
        # This is a basic implementation - might need refinement
        
        # Remove any rspress-specific components or syntax
        # Add more patterns as needed based on actual content
        
        return content
    
    def validate_migration(self):
        """Validate the migration results"""
        self.log("Validating migration...")
        
        total_files = 0
        migrated_files = 0
        
        for lang in self.languages:
            source_lang_dir = self.source_dir / "docs" / lang
            target_lang_dir = self.target_dir / "docs" / lang
            
            if source_lang_dir.exists():
                source_files = list(source_lang_dir.rglob("*.md"))
                target_files = list(target_lang_dir.rglob("*.md"))
                
                total_files += len(source_files)
                migrated_files += len(target_files)
                
                self.log(f"Language {lang}: {len(source_files)} source files, {len(target_files)} migrated files")
        
        self.log(f"Migration summary: {migrated_files}/{total_files} files migrated")
        
        if migrated_files == total_files:
            self.log("✅ All files migrated successfully!")
        else:
            self.log(f"⚠️  {total_files - migrated_files} files may need manual attention")
    
    def generate_migration_report(self):
        """Generate a migration report"""
        report_file = self.target_dir / "migration-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Content Migration Report\n")
            f.write("=" * 50 + "\n\n")
            
            for log_entry in self.migration_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Migration report saved to: {report_file}")
    
    def run_migration(self):
        """Run the complete migration process"""
        self.log("Starting content migration from rspress to mkdocs...")
        self.log(f"Source: {self.source_dir}")
        self.log(f"Target: {self.target_dir}")
        
        try:
            self.create_target_structure()
            self.migrate_markdown_files()
            self.validate_migration()
            self.generate_migration_report()
            
            self.log("✅ Migration completed successfully!")
            
        except Exception as e:
            self.log(f"❌ Migration failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    # Default paths - can be overridden via command line arguments
    source_dir = "../rspress-template"
    target_dir = "."
    
    # Check if source directory exists
    if not Path(source_dir).exists():
        print(f"❌ Source directory not found: {source_dir}")
        print("Please ensure the rspress-template directory exists")
        return
    
    # Create migrator and run migration
    migrator = ContentMigrator(source_dir, target_dir)
    migrator.run_migration()

if __name__ == "__main__":
    main()