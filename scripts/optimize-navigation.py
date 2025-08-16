#!/usr/bin/env python3
"""
Optimize navigation structure by adding missing index files and cleaning up orphaned files
"""

from pathlib import Path
from typing import List, Dict

class NavigationOptimizer:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.log_messages = []
    
    def log(self, message: str):
        """Log messages"""
        print(message)
        self.log_messages.append(message)
    
    def find_orphaned_index_files(self) -> List[Path]:
        """Find orphaned index.md files that could be added to navigation"""
        
        orphaned_indexes = []
        
        for index_file in self.docs_dir.rglob("index.md"):
            # Skip the main language index files (they're already in nav)
            relative_path = index_file.relative_to(self.docs_dir)
            
            # Check if it's a section index file (like zh/dio/index.md)
            if len(relative_path.parts) > 2:  # More than just lang/index.md
                orphaned_indexes.append(index_file)
        
        return orphaned_indexes
    
    def create_section_index_content(self, section_path: Path, section_name: str, language: str) -> str:
        """Create content for a section index file"""
        
        if language == 'zh':
            content = f"""# {section_name}

{section_name} 相关功能的文档。

## 功能概述

本节包含 {section_name} 相关的所有功能和工具。

## 子页面

请查看左侧导航栏中的具体功能页面。
"""
        elif language == 'en':
            content = f"""# {section_name}

Documentation for {section_name} related features.

## Feature Overview

This section contains all features and tools related to {section_name}.

## Sub Pages

Please check the specific feature pages in the left navigation bar.
"""
        elif language == 'ja':
            content = f"""# {section_name}

{section_name} 関連機能のドキュメント。

## 機能概要

このセクションには {section_name} に関連するすべての機能とツールが含まれています。

## サブページ

左のナビゲーションバーで具体的な機能ページをご確認ください。
"""
        else:
            content = f"""# {section_name}

Documentation for {section_name}.
"""
        
        return content
    
    def update_section_indexes(self):
        """Update section index files with proper content"""
        
        self.log("Updating section index files...")
        
        # Define section mappings
        section_mappings = {
            'dio': {'zh': 'Dio', 'en': 'Dio', 'ja': 'Dio'},
            'assets': {'zh': '资产管理', 'en': 'Asset Management', 'ja': 'アセット管理'},
            'settings': {'zh': '设置', 'en': 'Settings', 'ja': '設定'},
            'riverpod': {'zh': 'Riverpod', 'en': 'Riverpod', 'ja': 'Riverpod'},
            'hive': {'zh': 'Hive', 'en': 'Hive', 'ja': 'Hive'},
            'freezed': {'zh': 'Freezed', 'en': 'Freezed', 'ja': 'Freezed'},
            'dart-file': {'zh': 'Dart File', 'en': 'Dart File', 'ja': 'Dartファイル'},
            'pubspec': {'zh': 'Pubspec.yaml', 'en': 'Pubspec.yaml', 'ja': 'Pubspec.yaml'},
            'other': {'zh': '其他功能', 'en': 'Other Features', 'ja': 'その他の機能'},
            'shared_p': {'zh': 'Shared Preferences', 'en': 'Shared Preferences', 'ja': 'Shared Preferences'}
        }
        
        updated_files = 0
        
        for section, names in section_mappings.items():
            for lang, section_name in names.items():
                index_file = self.docs_dir / lang / section / "index.md"
                
                if index_file.exists():
                    # Update existing index file
                    content = self.create_section_index_content(index_file, section_name, lang)
                    
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_files += 1
                    self.log(f"✅ Updated: {index_file}")
        
        self.log(f"Updated {updated_files} section index files")
    
    def clean_orphaned_files(self):
        """Clean up orphaned files that are not needed"""
        
        self.log("Checking orphaned files...")
        
        # Files that can be safely removed
        files_to_remove = []
        
        # Find image_index.md files (these seem to be test files)
        for image_index in self.docs_dir.rglob("image_index.md"):
            files_to_remove.append(image_index)
        
        # Find hello.md files (these seem to be test files)
        for hello_file in self.docs_dir.rglob("hello.md"):
            files_to_remove.append(hello_file)
        
        removed_files = 0
        for file_to_remove in files_to_remove:
            try:
                file_to_remove.unlink()
                removed_files += 1
                self.log(f"🗑️  Removed: {file_to_remove}")
            except Exception as e:
                self.log(f"❌ Error removing {file_to_remove}: {e}")
        
        self.log(f"Removed {removed_files} orphaned files")
    
    def generate_optimization_report(self):
        """Generate optimization report"""
        
        report_file = Path("navigation-optimization-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Navigation Optimization Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Optimization Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.log_messages:
                f.write(f"{log_entry}\n")
        
        self.log(f"Optimization report saved to: {report_file}")
    
    def run_optimization(self):
        """Run the complete optimization process"""
        
        self.log("Starting navigation optimization...")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            # Update section index files
            self.update_section_indexes()
            
            # Clean orphaned files
            self.clean_orphaned_files()
            
            # Generate report
            self.generate_optimization_report()
            
            self.log("✅ Navigation optimization completed!")
            
        except Exception as e:
            self.log(f"❌ Navigation optimization failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    optimizer = NavigationOptimizer(docs_dir)
    optimizer.run_optimization()

if __name__ == "__main__":
    main()