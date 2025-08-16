#!/usr/bin/env python3
"""
Validation script for multi-language configuration
"""

import os
from pathlib import Path

def validate_language_structure():
    """Validate that all language directories have the required structure"""
    
    docs_dir = Path("docs")
    languages = ["zh", "en", "ja"]
    
    print("Validating multi-language structure...")
    
    for lang in languages:
        lang_dir = docs_dir / lang
        
        if not lang_dir.exists():
            print(f"❌ Missing language directory: {lang_dir}")
            continue
            
        # Check for index file
        index_file = lang_dir / "index.md"
        if not index_file.exists():
            print(f"❌ Missing index file: {index_file}")
        else:
            print(f"✅ Found index file: {index_file}")
    
    # Check i18n configuration
    i18n_file = Path("i18n.yml")
    if i18n_file.exists():
        print("✅ Found i18n.yml configuration file")
    else:
        print("❌ Missing i18n.yml configuration file")
    
    # Check mkdocs.yml for multi-language config
    mkdocs_file = Path("mkdocs.yml")
    if mkdocs_file.exists():
        with open(mkdocs_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'static-i18n' in content:
                print("✅ Found static-i18n plugin configuration")
            else:
                print("❌ Missing static-i18n plugin configuration")
    
    print("Validation complete!")

if __name__ == "__main__":
    validate_language_structure()