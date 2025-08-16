#!/usr/bin/env python3
"""
Main migration script that orchestrates the entire migration process
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
import os
import importlib.util

def import_module_from_file(module_name, file_path):
    """Import a module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get script directory
script_dir = Path(__file__).parent

# Import our migration modules
try:
    migrate_content = import_module_from_file("migrate_content", script_dir / "migrate-content.py")
    path_mapper = import_module_from_file("path_mapper", script_dir / "path-mapper.py")
    validate_content = import_module_from_file("validate_content", script_dir / "validate-content.py")
    
    ContentMigrator = migrate_content.ContentMigrator
    PathMapper = path_mapper.PathMapper
    ContentValidator = validate_content.ContentValidator
    
except Exception as e:
    print(f"❌ Error importing migration modules: {e}")
    print("Please ensure all migration scripts are in the same directory")
    sys.exit(1)

def main():
    """Main migration orchestrator"""
    
    parser = argparse.ArgumentParser(description="Migrate rspress documentation to mkdocs-material")
    parser.add_argument("--source", default="../rspress-template", 
                       help="Source rspress directory (default: ../rspress-template)")
    parser.add_argument("--target", default=".", 
                       help="Target mkdocs directory (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Perform a dry run without actually copying files")
    parser.add_argument("--validate-only", action="store_true",
                       help="Only validate existing content without migration")
    
    args = parser.parse_args()
    
    source_dir = Path(args.source)
    target_dir = Path(args.target)
    
    print("FlutterX Documentation Migration Tool")
    print("=" * 50)
    print(f"Source: {source_dir.absolute()}")
    print(f"Target: {target_dir.absolute()}")
    print()
    
    # Validate source directory
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        print("Please ensure the rspress-template directory exists")
        return 1
    
    # If validate-only mode, just run validation
    if args.validate_only:
        print("Running content validation only...")
        docs_dir = target_dir / "docs"
        if docs_dir.exists():
            validator = ContentValidator(str(docs_dir))
            results = validator.validate_all_content()
            
            total_issues = sum(len(issues) for issues in results.values())
            print(f"Validation complete. Found {total_issues} issues.")
            
            validator.generate_validation_report(results, str(target_dir / "validation-report.txt"))
        else:
            print(f"❌ Target docs directory not found: {docs_dir}")
        return 0
    
    try:
        # Step 1: Generate path mappings
        print("Step 1: Generating path mappings...")
        mapper = PathMapper()
        mappings = mapper.generate_path_mappings(str(source_dir))
        mapper.save_mappings(str(target_dir / "path-mappings.json"))
        print(f"✅ Generated {len(mappings)} path mappings")
        
        # Step 2: Validate mappings
        print("\nStep 2: Validating path mappings...")
        issues = mapper.validate_mappings(str(source_dir), str(target_dir))
        if issues:
            print(f"⚠️  Found {len(issues)} mapping issues:")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"  • {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
        else:
            print("✅ All path mappings validated")
        
        if args.dry_run:
            print("\n🔍 Dry run mode - no files will be copied")
            print("Migration would proceed with the following steps:")
            print("  3. Migrate markdown content")
            print("  4. Validate migrated content")
            print("  5. Generate migration report")
            return 0
        
        # Step 3: Migrate content
        print("\nStep 3: Migrating content...")
        migrator = ContentMigrator(str(source_dir), str(target_dir))
        migrator.run_migration()
        
        # Step 4: Validate migrated content
        print("\nStep 4: Validating migrated content...")
        docs_dir = target_dir / "docs"
        if docs_dir.exists():
            validator = ContentValidator(str(docs_dir))
            results = validator.validate_all_content()
            
            total_issues = sum(len(issues) for issues in results.values())
            print(f"Content validation complete. Found {total_issues} issues.")
            
            if total_issues > 0:
                validator.generate_validation_report(results, str(target_dir / "validation-report.txt"))
                print("⚠️  Please review the validation report for details")
            else:
                print("✅ All content validated successfully")
        
        print("\n🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Review the migration report and validation results")
        print("2. Test the mkdocs build: mkdocs build")
        print("3. Start the development server: mkdocs serve")
        print("4. Review and adjust navigation in mkdocs.yml")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())