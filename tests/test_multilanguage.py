#!/usr/bin/env python3
"""
Test suite for multi-language functionality
"""

import sys
import os
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from test_framework import TestSuite, TestResult

class MultiLanguageTestSuite(TestSuite):
    def __init__(self):
        super().__init__("Multi-Language Tests")
        self.docs_dir = Path("docs")
        self.config_file = Path("mkdocs.yml")
        self.languages = ["zh", "en", "ja"]
        
        # Add tests
        self.add_test(self.test_language_directories_exist)
        self.add_test(self.test_language_config)
        self.add_test(self.test_language_navigation)
        self.add_test(self.test_language_content_structure)
        self.add_test(self.test_language_switcher_config)
        self.add_test(self.test_index_files_exist)
        self.add_test(self.test_cross_language_consistency)
        self.add_test(self.test_language_specific_content)
    
    def test_language_directories_exist(self) -> TestResult:
        """Test that all language directories exist"""
        
        missing_dirs = []
        for lang in self.languages:
            lang_dir = self.docs_dir / lang
            if not lang_dir.exists():
                missing_dirs.append(lang)
        
        success = len(missing_dirs) == 0
        message = "All language directories exist" if success else f"Missing: {missing_dirs}"
        
        return TestResult("language_directories_exist", success, message)
    
    def test_language_config(self) -> TestResult:
        """Test language configuration in mkdocs.yml"""
        
        if not self.config_file.exists():
            return TestResult("language_config", False, "mkdocs.yml not found")
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # Check for i18n plugin
            has_i18n = 'static-i18n' in config_content
            
            # Check for language definitions
            lang_configs = []
            for lang in self.languages:
                if f'{lang}:' in config_content:
                    lang_configs.append(lang)
            
            success = has_i18n and len(lang_configs) >= 2
            
            message = f"i18n plugin: {has_i18n}, Language configs: {lang_configs}"
            
            return TestResult("language_config", success, message, {
                "has_i18n": has_i18n,
                "configured_languages": lang_configs
            })
            
        except Exception as e:
            return TestResult("language_config", False, str(e))
    
    def test_language_navigation(self) -> TestResult:
        """Test that navigation exists for each language"""
        
        if not self.config_file.exists():
            return TestResult("language_navigation", False, "mkdocs.yml not found")
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # Check for navigation sections for each language
            nav_sections = {}
            
            # Look for language-specific navigation
            for lang in self.languages:
                lang_pattern = f'{lang}/'
                if lang_pattern in config_content:
                    nav_sections[lang] = True
                else:
                    nav_sections[lang] = False
            
            success = sum(nav_sections.values()) >= 2
            
            message = f"Navigation sections: {nav_sections}"
            
            return TestResult("language_navigation", success, message, nav_sections)
            
        except Exception as e:
            return TestResult("language_navigation", False, str(e))
    
    def test_language_content_structure(self) -> TestResult:
        """Test content structure consistency across languages"""
        
        structure_comparison = {}
        
        for lang in self.languages:
            lang_dir = self.docs_dir / lang
            if lang_dir.exists():
                # Get directory structure
                dirs = set()
                for item in lang_dir.rglob("*"):
                    if item.is_dir():
                        relative_path = item.relative_to(lang_dir)
                        dirs.add(str(relative_path))
                
                structure_comparison[lang] = dirs
        
        # Check for structural consistency
        if len(structure_comparison) < 2:
            return TestResult("language_content_structure", False, "Not enough languages to compare")
        
        # Find common directories
        all_dirs = set()
        for dirs in structure_comparison.values():
            all_dirs.update(dirs)
        
        # Check how many languages have each directory
        consistency_score = 0
        total_dirs = len(all_dirs)
        
        for dir_name in all_dirs:
            lang_count = sum(1 for dirs in structure_comparison.values() if dir_name in dirs)
            if lang_count >= 2:  # At least 2 languages have this directory
                consistency_score += 1
        
        success = total_dirs == 0 or consistency_score / total_dirs >= 0.7
        
        message = f"Structure consistency: {consistency_score}/{total_dirs} directories consistent"
        
        return TestResult("language_content_structure", success, message, {
            "structure_comparison": {k: list(v) for k, v in structure_comparison.items()},
            "consistency_score": consistency_score,
            "total_directories": total_dirs
        })
    
    def test_language_switcher_config(self) -> TestResult:
        """Test language switcher configuration"""
        
        if not self.config_file.exists():
            return TestResult("language_switcher_config", False, "mkdocs.yml not found")
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # Check for alternate language configuration
            has_alternate = 'alternate:' in config_content
            
            # Check for language entries
            lang_entries = []
            for lang in self.languages:
                if f'lang: {lang}' in config_content:
                    lang_entries.append(lang)
            
            success = has_alternate and len(lang_entries) >= 2
            
            message = f"Language switcher: {has_alternate}, Entries: {lang_entries}"
            
            return TestResult("language_switcher_config", success, message, {
                "has_alternate": has_alternate,
                "language_entries": lang_entries
            })
            
        except Exception as e:
            return TestResult("language_switcher_config", False, str(e))
    
    def test_index_files_exist(self) -> TestResult:
        """Test that index files exist for each language"""
        
        missing_indexes = []
        
        for lang in self.languages:
            index_file = self.docs_dir / lang / "index.md"
            if not index_file.exists():
                missing_indexes.append(lang)
        
        success = len(missing_indexes) == 0
        message = "All language index files exist" if success else f"Missing indexes: {missing_indexes}"
        
        return TestResult("index_files_exist", success, message, {
            "missing_indexes": missing_indexes
        })
    
    def test_cross_language_consistency(self) -> TestResult:
        """Test consistency of content across languages"""
        
        # Check that major sections exist in all languages
        major_sections = ["dio", "freezed", "settings", "assets"]
        
        section_availability = {}
        
        for lang in self.languages:
            lang_dir = self.docs_dir / lang
            if lang_dir.exists():
                available_sections = []
                for section in major_sections:
                    section_dir = lang_dir / section
                    if section_dir.exists() and any(section_dir.rglob("*.md")):
                        available_sections.append(section)
                
                section_availability[lang] = available_sections
        
        # Calculate consistency score
        total_possible = len(major_sections) * len(self.languages)
        actual_sections = sum(len(sections) for sections in section_availability.values())
        
        consistency_score = actual_sections / total_possible if total_possible > 0 else 0
        success = consistency_score >= 0.8
        
        message = f"Cross-language consistency: {consistency_score:.1%}"
        
        return TestResult("cross_language_consistency", success, message, {
            "section_availability": section_availability,
            "consistency_score": consistency_score
        })
    
    def test_language_specific_content(self) -> TestResult:
        """Test that language-specific content is properly localized"""
        
        # Check for language-specific content in index files
        localization_checks = []
        
        expected_content = {
            "zh": ["FlutterX", "插件", "文档", "功能"],
            "en": ["FlutterX", "Plugin", "Documentation", "Features"],
            "ja": ["FlutterX", "プラグイン", "ドキュメント", "機能"]
        }
        
        for lang, keywords in expected_content.items():
            index_file = self.docs_dir / lang / "index.md"
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    found_keywords = sum(1 for keyword in keywords if keyword in content)
                    localization_checks.append({
                        "language": lang,
                        "found_keywords": found_keywords,
                        "total_keywords": len(keywords),
                        "score": found_keywords / len(keywords)
                    })
                    
                except Exception as e:
                    localization_checks.append({
                        "language": lang,
                        "error": str(e)
                    })
        
        # Check localization quality
        avg_score = sum(check.get("score", 0) for check in localization_checks) / len(localization_checks)
        success = avg_score >= 0.5
        
        message = f"Localization quality: {avg_score:.1%}"
        
        return TestResult("language_specific_content", success, message, {
            "localization_checks": localization_checks
        })

def main():
    """Run multi-language tests"""
    
    from test_framework import TestRunner
    
    runner = TestRunner()
    runner.add_suite(MultiLanguageTestSuite())
    
    results = runner.run_all_suites()
    runner.generate_report(results, "multilanguage-test-report.json")
    
    return results['total_passed'] == results['total_tests']

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)