#!/usr/bin/env python3
"""
Test configuration and utilities
"""

import os
from pathlib import Path

class TestConfig:
    """Test configuration settings"""
    
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        
        # Test directories
        self.docs_dir = self.project_dir / "docs"
        self.site_dir = self.project_dir / "site"
        self.assets_dir = self.docs_dir / "assets"
        self.scripts_dir = self.project_dir / "scripts"
        self.tests_dir = self.project_dir / "tests"
        
        # Languages
        self.languages = ["zh", "en", "ja"]
        self.language_names = {
            "zh": "简体中文",
            "en": "English", 
            "ja": "日本語"
        }
        
        # File patterns
        self.markdown_pattern = "*.md"
        self.image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg"]
        
        # Test thresholds
        self.max_file_size_mb = 1  # 1MB
        self.min_markdown_files = 100
        self.max_build_time_seconds = 300  # 5 minutes
        self.max_site_size_mb = 100  # 100MB
        
        # Required files
        self.required_config_files = [
            "mkdocs.yml",
            "requirements.txt",
            "README.md"
        ]
        
        self.required_directories = [
            "docs",
            "docs/assets",
            "docs/assets/images",
            "docs/stylesheets",
            "overrides",
            "scripts"
        ]
        
        self.required_scripts = [
            "migrate.py",
            "scripts/migrate-content.py",
            "scripts/migrate-assets.py",
            "scripts/build-navigation.py",
            "scripts/validate-content-comprehensive.py",
            "scripts/build-site.py",
            "scripts/test-build.py"
        ]
        
        # Template files
        self.template_files = [
            "overrides/partials/footer.html",
            "overrides/partials/header.html"
        ]
        
        # CSS files
        self.css_files = [
            "docs/stylesheets/extra.css"
        ]
    
    def get_language_dirs(self):
        """Get language directories"""
        return [self.docs_dir / lang for lang in self.languages]
    
    def get_all_markdown_files(self):
        """Get all markdown files"""
        return list(self.docs_dir.rglob(self.markdown_pattern))
    
    def get_all_image_files(self):
        """Get all image files"""
        image_files = []
        for pattern in self.image_patterns:
            image_files.extend(self.assets_dir.rglob(pattern))
        return image_files
    
    def validate_project_structure(self):
        """Validate basic project structure"""
        issues = []
        
        # Check required directories
        for dir_path in self.required_directories:
            full_path = self.project_dir / dir_path
            if not full_path.exists():
                issues.append(f"Missing directory: {dir_path}")
            elif not full_path.is_dir():
                issues.append(f"Not a directory: {dir_path}")
        
        # Check required files
        for file_path in self.required_config_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                issues.append(f"Missing file: {file_path}")
            elif not full_path.is_file():
                issues.append(f"Not a file: {file_path}")
        
        # Check required scripts
        for script_path in self.required_scripts:
            full_path = self.project_dir / script_path
            if not full_path.exists():
                issues.append(f"Missing script: {script_path}")
            elif not os.access(full_path, os.X_OK):
                issues.append(f"Script not executable: {script_path}")
        
        return issues

class TestUtils:
    """Test utility functions"""
    
    @staticmethod
    def count_files_by_extension(directory: Path, extension: str) -> int:
        """Count files with specific extension"""
        return len(list(directory.rglob(f"*.{extension.lstrip('.')}")))
    
    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Get file size in MB"""
        if file_path.exists():
            return file_path.stat().st_size / (1024 * 1024)
        return 0
    
    @staticmethod
    def get_directory_size_mb(directory: Path) -> float:
        """Get total directory size in MB"""
        total_size = 0
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size / (1024 * 1024)
    
    @staticmethod
    def validate_markdown_syntax(file_path: Path) -> list:
        """Basic markdown syntax validation"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for balanced brackets
            open_brackets = content.count('[')
            close_brackets = content.count(']')
            if open_brackets != close_brackets:
                issues.append(f"Unbalanced square brackets: {open_brackets} open, {close_brackets} close")
            
            # Check for balanced parentheses in links
            open_parens = content.count('](')
            close_parens = content.count(')')
            # This is a rough check - more sophisticated parsing would be better
            
            # Check for empty links
            if ']()" in content or ']()' in content:
                issues.append("Empty link found")
            
        except Exception as e:
            issues.append(f"Error reading file: {str(e)}")
        
        return issues
    
    @staticmethod
    def extract_image_references(file_path: Path) -> list:
        """Extract image references from markdown file"""
        import re
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find image references
            image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
            images = re.findall(image_pattern, content)
            
            return [(alt_text, image_path) for alt_text, image_path in images]
            
        except Exception:
            return []
    
    @staticmethod
    def validate_image_reference(base_path: Path, image_path: str) -> bool:
        """Validate that an image reference points to an existing file"""
        
        # Skip external URLs
        if image_path.startswith(('http://', 'https://')):
            return True
        
        # Handle relative paths
        if image_path.startswith('../'):
            full_path = (base_path.parent / image_path).resolve()
        else:
            full_path = base_path.parent / image_path
        
        return full_path.exists()

# Test data for validation
TEST_DATA = {
    'expected_file_counts': {
        'markdown_files_min': 100,
        'image_files_min': 50,
        'css_files_min': 1,
        'html_templates_min': 2
    },
    
    'performance_thresholds': {
        'build_time_max_seconds': 300,
        'site_size_max_mb': 100,
        'file_size_max_mb': 1
    },
    
    'content_requirements': {
        'languages': ['zh', 'en', 'ja'],
        'required_sections': ['nav', 'theme', 'plugins'],
        'required_files': ['index.md']
    }
}