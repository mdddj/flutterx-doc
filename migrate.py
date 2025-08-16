#!/usr/bin/env python3
"""
Simple content migration script for rspress to mkdocs
"""

import os
import shutil
import re
from pathlib import Path

def migrate_assets():
    """Migrate assets from rspress to mkdocs structure"""
    
    print("Migrating assets...")
    
    source_dir = Path("../rspress-template")
    target_dir = Path(".")
    
    # Create assets directory structure
    assets_dir = target_dir / "docs" / "assets"
    (assets_dir / "images").mkdir(parents=True, exist_ok=True)
    (assets_dir / "gif").mkdir(parents=True, exist_ok=True)
    (assets_dir / "videos").mkdir(parents=True, exist_ok=True)
    
    # Copy assets from public directory
    public_dir = source_dir / "docs" / "public"
    if not public_dir.exists():
        print("  ⚠️  No public directory found")
        return 0
    
    copied_assets = 0
    
    # Copy images
    images_source = public_dir / "images"
    if images_source.exists():
        for img_file in images_source.rglob("*"):
            if img_file.is_file():
                target_file = assets_dir / "images" / img_file.name
                try:
                    shutil.copy2(img_file, target_file)
                    copied_assets += 1
                except Exception as e:
                    print(f"  ❌ Error copying {img_file}: {e}")
    
    # Copy gifs
    gif_source = public_dir / "gif"
    if gif_source.exists():
        for gif_file in gif_source.rglob("*"):
            if gif_file.is_file():
                target_file = assets_dir / "gif" / gif_file.name
                try:
                    shutil.copy2(gif_file, target_file)
                    copied_assets += 1
                except Exception as e:
                    print(f"  ❌ Error copying {gif_file}: {e}")
    
    # Copy videos
    videos_source = public_dir / "videos"
    if videos_source.exists():
        for video_file in videos_source.rglob("*"):
            if video_file.is_file():
                # Put video files in gif directory since they're mostly gifs
                target_file = assets_dir / "gif" / video_file.name
                try:
                    shutil.copy2(video_file, target_file)
                    copied_assets += 1
                except Exception as e:
                    print(f"  ❌ Error copying {video_file}: {e}")
    
    # Copy root level assets (logos, etc.)
    for asset_file in public_dir.glob("*"):
        if asset_file.is_file():
            target_file = assets_dir / "images" / asset_file.name
            try:
                shutil.copy2(asset_file, target_file)
                copied_assets += 1
            except Exception as e:
                print(f"  ❌ Error copying {asset_file}: {e}")
    
    print(f"  ✅ Copied {copied_assets} assets")
    return copied_assets

def migrate_content():
    """Main migration function"""
    
    source_dir = Path("../rspress-template")
    target_dir = Path(".")
    
    print("FlutterX Content Migration")
    print("=" * 30)
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
    
    # Languages to migrate
    languages = ["zh", "en", "ja"]
    
    print(f"Source: {source_dir.absolute()}")
    print(f"Target: {target_dir.absolute()}")
    print()
    
    # First migrate assets
    total_assets = migrate_assets()
    print()
    
    # Then migrate content for each language
    total_files = 0
    for lang in languages:
        print(f"Migrating {lang} content...")
        
        source_lang_dir = source_dir / "docs" / lang
        target_lang_dir = target_dir / "docs" / lang
        
        if not source_lang_dir.exists():
            print(f"  ⚠️  Source language directory not found: {source_lang_dir}")
            continue
        
        # Create target directory
        target_lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all markdown files
        copied_files = 0
        for md_file in source_lang_dir.rglob("*.md"):
            relative_path = md_file.relative_to(source_lang_dir)
            target_file = target_lang_dir / relative_path
            
            # Create parent directories
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy and process the file
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic content processing
                processed_content = process_markdown_content(content, target_file)
                
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                copied_files += 1
                
            except Exception as e:
                print(f"  ❌ Error copying {md_file}: {e}")
        
        print(f"  ✅ Copied {copied_files} files")
        total_files += copied_files
    
    print()
    print("✅ Content migration completed!")
    print(f"📊 Summary: {total_files} markdown files, {total_assets} assets")
    print()
    print("Next steps:")
    print("1. Run: mkdocs serve")
    print("2. Check the site at: http://127.0.0.1:8000")
    print("3. Update navigation in mkdocs.yml as needed")
    
    return True

def process_markdown_content(content: str, target_file: Path) -> str:
    """Process markdown content for mkdocs compatibility"""
    
    # Calculate relative path to assets directory
    docs_dir = Path("docs")
    relative_to_docs = target_file.relative_to(docs_dir)
    depth = len(relative_to_docs.parts) - 1
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
        
        # ![alt](/videos/path) -> ![alt](../assets/gif/path) (videos are mostly gifs)
        (r'!\[([^\]]*)\]\(/videos/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
        
        # ![alt](/public/videos/path) -> ![alt](../assets/gif/path)
        (r'!\[([^\]]*)\]\(/public/videos/([^)]+)\)', rf'![\1]({assets_prefix}gif/\2)'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

if __name__ == "__main__":
    success = migrate_content()
    exit(0 if success else 1)