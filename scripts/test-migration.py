#!/usr/bin/env python3
"""
Simple test script to run content migration
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_migration():
    """Test the migration process"""
    
    print("Testing content migration...")
    
    # Import and test path mapper
    try:
        # Import from file with dash in name
        import importlib.util
        spec = importlib.util.spec_from_file_location("path_mapper", "scripts/path-mapper.py")
        path_mapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(path_mapper_module)
        PathMapper = path_mapper_module.PathMapper
        
        source_dir = "../rspress-template"
        if not Path(source_dir).exists():
            print(f"❌ Source directory not found: {source_dir}")
            return False
        
        mapper = PathMapper()
        mappings = mapper.generate_path_mappings(source_dir)
        print(f"✅ Generated {len(mappings)} path mappings")
        
        # Save mappings for reference
        mapper.save_mappings("test-path-mappings.json")
        print("✅ Path mappings saved")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing migration: {e}")
        return False

if __name__ == "__main__":
    success = test_migration()
    sys.exit(0 if success else 1)