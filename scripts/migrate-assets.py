#!/usr/bin/env python3
"""
Asset migration script for rspress to mkdocs-material
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Set

class AssetMigrator:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.asset_mappings = {}
        self.migration_log = []
        
        # Supported asset types
        self.asset_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',  # Images
            '.mp4', '.webm', '.mov', '.avi',  # Videos
            '.pdf', '.zip', '.tar.gz',  # Documents
            '.ico', '.icns'  # Icons
        }
    
    def log(self, message: str):
        """Log migration messages"""
        print(message)
        self.migration_log.append(message)
    
    def discover_assets(self) -> Dict[str, Path]:
        """Discover all assets in the source directory"""
        
        assets = {}
        public_dir = self.source_dir / "docs" / "public"
        
        if not public_dir.exists():
            self.log(f"⚠️  Public directory not found: {public_dir}")
            return assets
        
        self.log(f"Discovering assets in: {public_dir}")
        
        for asset_file in public_dir.rglob("*"):
            if asset_file.is_file():
                # Check if it's a supported asset type
                if asset_file.suffix.lower() in self.asset_extensions or asset_file.suffix == '':
                    relative_path = asset_file.relative_to(public_dir)
                    assets[str(relative_path)] = asset_file
        
        self.log(f"✅ Discovered {len(assets)} assets")
        return assets
    
    def create_asset_structure(self):
        """Create the target asset directory structure"""
        
        target_assets_dir = self.target_dir / "docs" / "assets"
        
        # Create main asset directories
        directories = [
            target_assets_dir / "images",
            target_assets_dir / "videos", 
            target_assets_dir / "gif",
            target_assets_dir / "documents"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.log(f"✅ Created directory: {directory}")
    
    def migrate_assets(self) -> Dict[str, str]:
        """Migrate all assets to the target directory"""
        
        self.log("Starting asset migration...")
        
        assets = self.discover_assets()
        if not assets:
            self.log("⚠️  No assets found to migrate")
            return {}
        
        self.create_asset_structure()
        
        migrated_assets = {}
        target_assets_dir = self.target_dir / "docs" / "assets"
        
        for relative_path, source_file in assets.items():
            try:
                # Determine target subdirectory based on file type
                target_subdir = self._get_target_subdirectory(source_file)
                target_file = target_assets_dir / target_subdir / source_file.name
                
                # Handle name conflicts
                if target_file.exists():
                    target_file = self._resolve_name_conflict(target_file)
                
                # Create parent directory if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file
                shutil.copy2(source_file, target_file)
                
                # Record the mapping
                source_key = str(relative_path)
                target_key = str(target_file.relative_to(self.target_dir / "docs"))
                migrated_assets[source_key] = target_key
                
                self.log(f"✅ Migrated: {source_key} -> {target_key}")
                
            except Exception as e:
                self.log(f"❌ Error migrating {relative_path}: {str(e)}")
        
        self.asset_mappings = migrated_assets
        return migrated_assets
    
    def _get_target_subdirectory(self, source_file: Path) -> str:
        """Determine the target subdirectory for an asset"""
        
        extension = source_file.suffix.lower()
        
        if extension in {'.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.icns'}:
            return "images"
        elif extension in {'.gif'}:
            return "gif"
        elif extension in {'.mp4', '.webm', '.mov', '.avi'}:
            return "videos"
        elif extension in {'.pdf', '.zip', '.tar.gz'}:
            return "documents"
        else:
            # Default to images for unknown types
            return "images"
    
    def _resolve_name_conflict(self, target_file: Path) -> Path:
        """Resolve naming conflicts by adding a suffix"""
        
        base_name = target_file.stem
        extension = target_file.suffix
        parent = target_file.parent
        counter = 1
        
        while target_file.exists():
            new_name = f"{base_name}_{counter}{extension}"
            target_file = parent / new_name
            counter += 1
        
        return target_file
    
    def update_markdown_references(self):
        """Update markdown files to use new asset paths"""
        
        self.log("Updating markdown file references...")
        
        if not self.asset_mappings:
            self.log("⚠️  No asset mappings available")
            return
        
        # Process all markdown files in the docs directory
        docs_dir = self.target_dir / "docs"
        updated_files = 0
        
        for md_file in docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Update asset references
                content = self._update_asset_references(content, md_file)
                
                # Only write if content changed
                if content != original_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files += 1
                    self.log(f"✅ Updated references in: {md_file}")
                
            except Exception as e:
                self.log(f"❌ Error updating {md_file}: {str(e)}")
        
        self.log(f"✅ Updated {updated_files} markdown files")
    
    def _update_asset_references(self, content: str, md_file: Path) -> str:
        """Update asset references in markdown content"""
        
        # Calculate relative path from markdown file to assets directory
        md_relative_to_docs = md_file.relative_to(self.target_dir / "docs")
        depth = len(md_relative_to_docs.parts) - 1
        assets_prefix = "../" * depth + "assets/"
        
        # Update various image reference patterns
        patterns = [
            # ![alt](/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(/images/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](/public/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(/public/images/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](../public/images/path) -> ![alt](../assets/images/path)
            (r'!\[([^\]]*)\]\(\.\.\/public\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            
            # ![alt](/gif/path) -> ![alt](../assets/gif/path)
            (r'!\[([^\]]*)\]\(/gif/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
            
            # ![alt](/public/gif/path) -> ![alt](../assets/gif/path)
            (r'!\[([^\]]*)\]\(/public/gif/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
            
            # ![alt](/videos/path) -> ![alt](../assets/videos/path)
            (r'!\[([^\]]*)\]\(/videos/([^)]+)\)', rf'![\1]({assets_prefix}videos/\2)'),
            
            # ![alt](/public/videos/path) -> ![alt](../assets/videos/path)
            (r'!\[([^\]]*)\]\(/public/videos/([^)]+)\)', rf'![\1]({assets_prefix}videos/\2)'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def copy_logo_files(self):
        """Copy logo files to the assets directory for mkdocs configuration"""
        
        self.log("Copying logo files...")
        
        public_dir = self.source_dir / "docs" / "public"
        target_images_dir = self.target_dir / "docs" / "assets" / "images"
        
        # Look for logo files
        logo_files = [
            "logo.svg",
            "rspress-icon.png", 
            "rspress-light-logo.png",
            "rspress-dark-logo.png"
        ]
        
        for logo_file in logo_files:
            source_logo = public_dir / "images" / logo_file
            if not source_logo.exists():
                source_logo = public_dir / logo_file
            
            if source_logo.exists():
                target_logo = target_images_dir / logo_file
                try:
                    shutil.copy2(source_logo, target_logo)
                    self.log(f"✅ Copied logo: {logo_file}")
                except Exception as e:
                    self.log(f"❌ Error copying logo {logo_file}: {str(e)}")
    
    def generate_asset_report(self):
        """Generate a report of migrated assets"""
        
        report_file = self.target_dir / "asset-migration-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Asset Migration Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total assets migrated: {len(self.asset_mappings)}\n\n")
            
            f.write("Asset Mappings:\n")
            f.write("-" * 30 + "\n")
            
            for source, target in self.asset_mappings.items():
                f.write(f"{source} -> {target}\n")
            
            f.write("\nMigration Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.migration_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Asset migration report saved to: {report_file}")
    
    def run_migration(self):
        """Run the complete asset migration process"""
        
        self.log("Starting asset migration from rspress to mkdocs...")
        self.log(f"Source: {self.source_dir}")
        self.log(f"Target: {self.target_dir}")
        
        try:
            # Migrate assets
            migrated_assets = self.migrate_assets()
            
            # Copy logo files
            self.copy_logo_files()
            
            # Update markdown references
            self.update_markdown_references()
            
            # Generate report
            self.generate_asset_report()
            
            self.log("✅ Asset migration completed successfully!")
            self.log(f"Migrated {len(migrated_assets)} assets")
            
        except Exception as e:
            self.log(f"❌ Asset migration failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    source_dir = "../rspress-template"
    target_dir = "."
    
    if not Path(source_dir).exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    migrator = AssetMigrator(source_dir, target_dir)
    migrator.run_migration()

if __name__ == "__main__":
    main()