#!/usr/bin/env python3
"""
Test suite for content migration accuracy
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from test_framework import TestSuite, TestResult, assert_file_exists, assert_directory_exists, count_files_with_extension

class ContentMigrationTestSuite(TestSuite):
    def __init__(self):
        super().__init__("Content Migration Tests")
        self.source_dir = Path("../rspress-template/docs")
        self.target_dir = Path("docs")
        
        # Add tests
        self.add_test(self.test_directory_structure)
        self.add_test(self.test_language_directories)
        self.add_test(self.test_markdown_files_migrated)
        self.add_test(self.test_assets_migrated)
        self.add_test(self.test_file_count_consistency)
        self.add_test(self.test_content_preservation)
        self.add_test(self.test_image_references_updated)
        self.add_test(self.test_navigation_files_exist)
    
    def setup(self):
        """Setup for content migration tests"""
        # Ensure we're in the right directory
        if not self.target_dir.exists():
            raise Exception(f"Target directory not found: {self.target_dir}")
    
    def test_directory_structure(self) -> TestResult:
        """Test that basic directory structure exists"""
        
        required_dirs = [
            "docs",
            "docs/zh",
            "docs/en", 
            "docs/ja",
            "docs/assets",
            "docs/assets/images"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                missing_dirs.append(dir_path)
        
        success = len(missing_dirs) == 0
        message = "All required directories exist" if success else f"Missing directories: {missing_dirs}"
        
        return TestResult("directory_structure", success, message, {"missing_dirs": missing_dirs})
    
    def test_language_directories(self) -> TestResult:
        """Test that language directories have content"""
        
        languages = ["zh", "en", "ja"]
        results = {}
        
        for lang in languages:
            lang_dir = self.target_dir / lang
            if lang_dir.exists():
                md_files = list(lang_dir.rglob("*.md"))
                results[lang] = len(md_files)
            else:
                results[lang] = 0
        
        # Check that each language has at least some files
        min_files_per_lang = 10  # Reasonable minimum
        success = all(count >= min_files_per_lang for count in results.values())
        
        message = f"File counts per language: {results}"
        if not success:
            message += f" (minimum expected: {min_files_per_lang})"
        
        return TestResult("language_directories", success, message, results)
    
    def test_markdown_files_migrated(self) -> TestResult:
        """Test that markdown files were migrated"""
        
        if not self.source_dir.exists():
            return TestResult("markdown_files_migrated", False, "Source directory not found")
        
        # Count source files
        source_md_count = 0
        for lang in ["zh", "en", "ja"]:
            lang_dir = self.source_dir / lang
            if lang_dir.exists():
                source_md_count += len(list(lang_dir.rglob("*.md")))
        
        # Count target files
        target_md_count = len(list(self.target_dir.rglob("*.md")))
        
        # Allow for some variance (index files, etc.)
        success = target_md_count >= source_md_count * 0.9
        
        message = f"Source: {source_md_count} files, Target: {target_md_count} files"
        
        return TestResult("markdown_files_migrated", success, message, {
            "source_count": source_md_count,
            "target_count": target_md_count
        })
    
    def test_assets_migrated(self) -> TestResult:
        """Test that assets were migrated"""
        
        assets_dir = self.target_dir / "assets"
        
        if not assets_dir.exists():
            return TestResult("assets_migrated", False, "Assets directory not found")
        
        # Count different asset types
        image_count = (len(list(assets_dir.rglob("*.png"))) + 
                      len(list(assets_dir.rglob("*.jpg"))) + 
                      len(list(assets_dir.rglob("*.svg"))))
        
        gif_count = len(list(assets_dir.rglob("*.gif")))
        
        success = image_count > 50 and gif_count > 0  # Reasonable expectations
        
        message = f"Assets migrated: {image_count} images, {gif_count} gifs"
        
        return TestResult("assets_migrated", success, message, {
            "image_count": image_count,
            "gif_count": gif_count
        })
    
    def test_file_count_consistency(self) -> TestResult:
        """Test file count consistency across languages"""
        
        languages = ["zh", "en", "ja"]
        file_counts = {}
        
        for lang in languages:
            lang_dir = self.target_dir / lang
            if lang_dir.exists():
                # Count files by directory structure
                dir_counts = {}
                for md_file in lang_dir.rglob("*.md"):
                    relative_path = md_file.relative_to(lang_dir)
                    dir_name = str(relative_path.parent)
                    dir_counts[dir_name] = dir_counts.get(dir_name, 0) + 1
                
                file_counts[lang] = dir_counts
        
        # Check for major discrepancies
        all_dirs = set()
        for counts in file_counts.values():
            all_dirs.update(counts.keys())
        
        discrepancies = []
        for dir_name in all_dirs:
            counts = [file_counts[lang].get(dir_name, 0) for lang in languages]
            if max(counts) - min(counts) > 2:  # Allow small differences
                discrepancies.append(f"{dir_name}: {dict(zip(languages, counts))}")
        
        success = len(discrepancies) == 0
        message = "File counts consistent across languages" if success else f"Discrepancies: {discrepancies}"
        
        return TestResult("file_count_consistency", success, message, {
            "file_counts": file_counts,
            "discrepancies": discrepancies
        })
    
    def test_content_preservation(self) -> TestResult:
        """Test that content was preserved during migration"""
        
        # Sample a few files to check content preservation
        sample_files = [
            "zh/index.md",
            "en/index.md",
            "zh/安装.md",
            "en/installation.md"
        ]
        
        content_checks = []
        
        for file_path in sample_files:
            full_path = self.target_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Basic content checks
                    has_title = content.startswith('#') or '# ' in content
                    has_content = len(content.strip()) > 100
                    
                    content_checks.append({
                        "file": file_path,
                        "has_title": has_title,
                        "has_content": has_content,
                        "length": len(content)
                    })
                    
                except Exception as e:
                    content_checks.append({
                        "file": file_path,
                        "error": str(e)
                    })
        
        # Check that most files have proper content
        valid_files = sum(1 for check in content_checks 
                         if check.get("has_title") and check.get("has_content"))
        
        success = valid_files >= len(sample_files) * 0.8
        
        message = f"Content preserved in {valid_files}/{len(sample_files)} sample files"
        
        return TestResult("content_preservation", success, message, {
            "content_checks": content_checks
        })
    
    def test_image_references_updated(self) -> TestResult:
        """Test that image references were updated correctly"""
        
        # Check a few files for proper image references
        sample_files = [
            "zh/安装.md",
            "en/installation.md"
        ]
        
        image_ref_checks = []
        
        for file_path in sample_files:
            full_path = self.target_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for image references
                    import re
                    image_refs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
                    
                    # Check if references use proper relative paths
                    proper_refs = 0
                    total_refs = len(image_refs)
                    
                    for alt_text, img_path in image_refs:
                        if img_path.startswith('../assets/') or img_path.startswith('assets/'):
                            proper_refs += 1
                    
                    image_ref_checks.append({
                        "file": file_path,
                        "total_refs": total_refs,
                        "proper_refs": proper_refs,
                        "references": image_refs[:3]  # Sample first 3
                    })
                    
                except Exception as e:
                    image_ref_checks.append({
                        "file": file_path,
                        "error": str(e)
                    })
        
        # Check that image references are properly formatted
        total_refs = sum(check.get("total_refs", 0) for check in image_ref_checks)
        proper_refs = sum(check.get("proper_refs", 0) for check in image_ref_checks)
        
        success = total_refs == 0 or proper_refs / total_refs >= 0.8
        
        message = f"Image references: {proper_refs}/{total_refs} properly formatted"
        
        return TestResult("image_references_updated", success, message, {
            "image_ref_checks": image_ref_checks
        })
    
    def test_navigation_files_exist(self) -> TestResult:
        """Test that navigation-related files exist"""
        
        required_files = [
            "mkdocs.yml",
            "docs/index.md",
            "docs/zh/index.md",
            "docs/en/index.md",
            "docs/ja/index.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        success = len(missing_files) == 0
        message = "All navigation files exist" if success else f"Missing files: {missing_files}"
        
        return TestResult("navigation_files_exist", success, message, {
            "missing_files": missing_files
        })

def main():
    """Run content migration tests"""
    
    from test_framework import TestRunner
    
    runner = TestRunner()
    runner.add_suite(ContentMigrationTestSuite())
    
    results = runner.run_all_suites()
    runner.generate_report(results, "content-migration-test-report.json")
    
    return results['total_passed'] == results['total_tests']

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)