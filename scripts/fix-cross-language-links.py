#!/usr/bin/env python3
"""
Fix cross-language links and references in markdown files
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

class CrossLanguageLinkFixer:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.fixed_files = []
        self.fix_log = []
        
    def log(self, message: str):
        """Log fix messages"""
        print(message)
        self.fix_log.append(message)
    
    def fix_all_cross_language_links(self):
        """Fix cross-language links in all markdown files"""
        
        self.log("Fixing cross-language links...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            if self.fix_file_cross_language_links(md_file):
                self.fixed_files.append(md_file)
        
        self.log(f"✅ Fixed cross-language links in {len(self.fixed_files)} files")
    
    def fix_file_cross_language_links(self, md_file: Path) -> bool:
        """Fix cross-language links in a single file"""
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Get current language
            relative_path = md_file.relative_to(self.docs_dir)
            current_lang = relative_path.parts[0] if len(relative_path.parts) > 1 else 'root'
            
            # Fix various link patterns
            content = self._fix_language_specific_links(content, current_lang, md_file)
            content = self._fix_asset_links(content, md_file)
            content = self._fix_relative_links(content, md_file)
            
            # Only write if content changed
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes = self._count_changes(original_content, content)
                self.log(f"✅ Fixed {md_file} ({changes} changes)")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error fixing {md_file}: {str(e)}")
            return False
    
    def _fix_language_specific_links(self, content: str, current_lang: str, md_file: Path) -> str:
        """Fix links that should point to same-language content"""
        
        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip external links and anchors
            if link_url.startswith(('http://', 'https://', '#')):
                return match.group(0)
            
            # Fix links that start with /zh/, /en/, /ja/ but should be relative
            lang_pattern = r'^/(zh|en|ja)/'
            if re.match(lang_pattern, link_url):
                # Extract the path after language
                path_after_lang = re.sub(lang_pattern, '', link_url)
                
                # If it's pointing to a different language, keep it
                # If it's pointing to same language, make it relative
                target_lang = re.match(lang_pattern, link_url).group(1)
                if target_lang == current_lang:
                    # Calculate relative path
                    current_depth = len(md_file.relative_to(self.docs_dir).parts) - 1
                    relative_prefix = '../' * (current_depth - 1) if current_depth > 1 else ''
                    new_url = relative_prefix + path_after_lang
                    return f"[{link_text}]({new_url})"
            
            return match.group(0)
        
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
    
    def _fix_asset_links(self, content: str, md_file: Path) -> str:
        """Fix asset links to point to correct asset directory"""
        
        # Calculate relative path to assets directory
        relative_path = md_file.relative_to(self.docs_dir)
        depth = len(relative_path.parts) - 1
        assets_prefix = '../' * depth + 'assets/'
        
        # Fix various asset link patterns
        patterns = [
            # Fix links that are already pointing to assets but with wrong depth
            (r'!\[([^\]]*)\]\(\.\.\/\.\.\/assets\/([^)]+)\)', rf'![\1]({assets_prefix}\2)'),
            (r'!\[([^\]]*)\]\(\.\.\/assets\/([^)]+)\)', rf'![\1]({assets_prefix}\2)'),
            (r'!\[([^\]]*)\]\(assets\/([^)]+)\)', rf'![\1]({assets_prefix}\2)'),
            
            # Fix old rspress-style image links that weren't caught before
            (r'!\[([^\]]*)\]\(\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            (r'!\[([^\]]*)\]\(\.\.\/public\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
            (r'!\[([^\]]*)\]\(public\/images\/([^)]+)\)', rf'![\1]({assets_prefix}images/\2)'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _fix_relative_links(self, content: str, md_file: Path) -> str:
        """Fix relative links between markdown files"""
        
        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip external links, anchors, and assets
            if (link_url.startswith(('http://', 'https://', '#', '../assets/')) or 
                '/assets/' in link_url):
                return match.group(0)
            
            # Fix relative markdown links
            if link_url.endswith('.md') or '/' in link_url:
                # Try to resolve the link
                resolved_url = self._resolve_relative_link(link_url, md_file)
                if resolved_url != link_url:
                    return f"[{link_text}]({resolved_url})"
            
            return match.group(0)
        
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
    
    def _resolve_relative_link(self, link_url: str, current_file: Path) -> str:
        """Resolve a relative link to ensure it points to the correct file"""
        
        # Remove fragment
        fragment = ''
        if '#' in link_url:
            link_url, fragment = link_url.split('#', 1)
            fragment = '#' + fragment
        
        # If it's already a proper relative path, check if it exists
        if link_url.startswith('../'):
            target_path = (current_file.parent / link_url).resolve()
            if target_path.exists():
                return link_url + fragment
        
        # Try to find the file in the same language directory
        current_relative = current_file.relative_to(self.docs_dir)
        if len(current_relative.parts) > 1:
            current_lang = current_relative.parts[0]
            
            # Look for the file in the same language
            possible_paths = [
                self.docs_dir / current_lang / link_url,
                self.docs_dir / current_lang / (link_url + '.md') if not link_url.endswith('.md') else None,
            ]
            
            for possible_path in possible_paths:
                if possible_path and possible_path.exists():
                    # Calculate relative path
                    try:
                        rel_path = possible_path.relative_to(current_file.parent)
                        return str(rel_path) + fragment
                    except ValueError:
                        # Files are not in a relative path, calculate with ../
                        current_depth = len(current_file.relative_to(self.docs_dir).parts) - 1
                        target_relative = possible_path.relative_to(self.docs_dir)
                        
                        if current_depth > 1:
                            up_levels = '../' * (current_depth - 1)
                            return up_levels + str(target_relative) + fragment
                        else:
                            return str(target_relative) + fragment
        
        return link_url + fragment
    
    def _count_changes(self, original: str, updated: str) -> int:
        """Count the number of changes made"""
        
        original_lines = original.split('\n')
        updated_lines = updated.split('\n')
        
        changes = 0
        for orig, upd in zip(original_lines, updated_lines):
            if orig != upd:
                changes += 1
        
        return changes
    
    def validate_fixed_links(self):
        """Validate that fixed links are correct"""
        
        self.log("Validating fixed links...")
        
        validation_issues = []
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all links
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                for link_text, link_url in links:
                    if not link_url.startswith(('http://', 'https://', '#')):
                        # Check internal link
                        if not self._validate_link(link_url, md_file):
                            validation_issues.append(f"{md_file}: Invalid link to {link_url}")
                
            except Exception as e:
                validation_issues.append(f"{md_file}: Error reading file - {str(e)}")
        
        if validation_issues:
            self.log(f"⚠️  Found {len(validation_issues)} validation issues after fixing")
            for issue in validation_issues[:5]:  # Show first 5
                self.log(f"  • {issue}")
            if len(validation_issues) > 5:
                self.log(f"  ... and {len(validation_issues) - 5} more")
        else:
            self.log("✅ All fixed links are valid")
        
        return validation_issues
    
    def _validate_link(self, link_url: str, current_file: Path) -> bool:
        """Validate that a link points to an existing resource"""
        
        # Remove fragment
        if '#' in link_url:
            link_url = link_url.split('#')[0]
        
        if not link_url:  # Pure anchor
            return True
        
        # Resolve path
        if link_url.startswith('../'):
            target_path = (current_file.parent / link_url).resolve()
        elif link_url.startswith('/'):
            target_path = self.docs_dir / link_url.lstrip('/')
        else:
            target_path = current_file.parent / link_url
        
        return target_path.exists()
    
    def generate_fix_report(self):
        """Generate a fix report"""
        
        report_file = Path("cross-language-links-fix-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Cross-Language Links Fix Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total files fixed: {len(self.fixed_files)}\n\n")
            
            if self.fixed_files:
                f.write("Fixed Files:\n")
                f.write("-" * 30 + "\n")
                for file_path in self.fixed_files:
                    f.write(f"{file_path}\n")
                f.write("\n")
            
            f.write("Fix Log:\n")
            f.write("-" * 30 + "\n")
            for log_entry in self.fix_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Fix report saved to: {report_file}")
    
    def run_fix(self):
        """Run the complete cross-language links fix process"""
        
        self.log("Starting cross-language links fix...")
        self.log(f"Docs directory: {self.docs_dir}")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            # Fix all cross-language links
            self.fix_all_cross_language_links()
            
            # Validate fixed links
            validation_issues = self.validate_fixed_links()
            
            # Generate report
            self.generate_fix_report()
            
            self.log("✅ Cross-language links fix completed!")
            
            if validation_issues:
                self.log(f"⚠️  Please review {len(validation_issues)} remaining issues")
            
        except Exception as e:
            self.log(f"❌ Cross-language links fix failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    if not Path(docs_dir).exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return
    
    fixer = CrossLanguageLinkFixer(docs_dir)
    fixer.run_fix()

if __name__ == "__main__":
    main()