#!/usr/bin/env python3
"""
Path mapping utility for rspress to mkdocs migration
"""

from pathlib import Path
from typing import Dict, List, Tuple
import json

class PathMapper:
    def __init__(self):
        self.path_mappings = {}
        self.language_mappings = {
            "zh": "zh",
            "en": "en", 
            "ja": "ja"
        }
    
    def generate_path_mappings(self, source_dir: str) -> Dict[str, str]:
        """Generate path mappings from rspress to mkdocs structure"""
        
        source_path = Path(source_dir)
        mappings = {}
        
        # Map the docs directory structure
        docs_dir = source_path / "docs"
        
        if docs_dir.exists():
            for lang_dir in docs_dir.iterdir():
                if lang_dir.is_dir() and lang_dir.name in self.language_mappings:
                    lang = lang_dir.name
                    
                    # Map all markdown files in this language directory
                    for md_file in lang_dir.rglob("*.md"):
                        relative_path = md_file.relative_to(lang_dir)
                        
                        # Source path (relative to rspress docs)
                        source_key = f"{lang}/{relative_path}"
                        
                        # Target path (relative to mkdocs docs)
                        target_value = f"docs/{lang}/{relative_path}"
                        
                        mappings[source_key] = target_value
        
        # Map public assets
        public_dir = docs_dir / "public"
        if public_dir.exists():
            for asset_file in public_dir.rglob("*"):
                if asset_file.is_file():
                    relative_path = asset_file.relative_to(public_dir)
                    source_key = f"public/{relative_path}"
                    target_value = f"docs/assets/{relative_path}"
                    mappings[source_key] = target_value
        
        self.path_mappings = mappings
        return mappings
    
    def save_mappings(self, output_file: str):
        """Save path mappings to a JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.path_mappings, f, indent=2, ensure_ascii=False)
    
    def load_mappings(self, input_file: str):
        """Load path mappings from a JSON file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            self.path_mappings = json.load(f)
    
    def get_target_path(self, source_path: str) -> str:
        """Get target path for a given source path"""
        return self.path_mappings.get(source_path, source_path)
    
    def validate_mappings(self, source_dir: str, target_dir: str) -> List[str]:
        """Validate that all mapped files exist"""
        
        issues = []
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        for source_key, target_value in self.path_mappings.items():
            source_file = source_path / "docs" / source_key
            target_file = target_path / target_value
            
            if not source_file.exists():
                issues.append(f"Source file missing: {source_file}")
            
            if not target_file.parent.exists():
                issues.append(f"Target directory missing: {target_file.parent}")
        
        return issues

def main():
    """Main function for testing path mapping"""
    
    source_dir = "../rspress-template"
    
    if not Path(source_dir).exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    mapper = PathMapper()
    mappings = mapper.generate_path_mappings(source_dir)
    
    print(f"Generated {len(mappings)} path mappings:")
    for source, target in list(mappings.items())[:10]:  # Show first 10
        print(f"  {source} -> {target}")
    
    if len(mappings) > 10:
        print(f"  ... and {len(mappings) - 10} more")
    
    # Save mappings
    mapper.save_mappings("path-mappings.json")
    print("Path mappings saved to path-mappings.json")

if __name__ == "__main__":
    main()