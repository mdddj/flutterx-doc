#!/usr/bin/env python3
"""
Update internal links and references in markdown files for mkdocs compatibility
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple, Set
from urllib.parse import urlparse

class InternalLinkUpdater:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.updated_files = []
        self.update_log = []
        self.link_mappings = {}
        self.broken_links = []
        
    def log(self, message: str):
        """Log update messages"""
        print(message)
        self.update_log.append(message)
    
    def scan_all_files(self) -> Dict[str, Path]:
        """Scan all markdown files and create a mapping"""
        
        self.log("Scanning all markdown files...")
        
        file_mappings = {}
        
        for md_file in self.docs_dir.rglob("*.md"):
            relative_path = md_file.relative_to(self.docs_dir)
            
            # Create multiple possible keys for this file
            keys = [
                str(relative_path),  # Full path: zh/dio/starter.md
                relative_path.name,  # Just filename: starter.md
                relative_path.stem,  # Without extension: starter
            ]
            
            # Add language-specific mappings
            if len(relative_path.parts) >= 2:
                lang = relative_path.parts[0]
                rest_path = "/".join(relative_path.parts[1:])
                keys.append(f"/{lang}/{rest_path}")  # /zh/dio/starter.md
                keys.append(f"/{rest_path}")  # /dio/starter.md
                keys.append(rest_path)  # dio/starter.md
            
            for key in keys:
                file_mappings[key] = md_file
        
        self.log(f"✅ Created mappings for {len(set(file_mappings.values()))} files")
        return file_mappings
    
    def update_all_internal_links(self):
        """Update internal links in all markdown files"""
        
        self.log("Updating internal links in all markdown files...")
        
        # First, scan all files to create mappings
        file_mappings = self.scan_all_files()
        
        for md_file in self.docs_dir.rglob("*.md"):
            if self.update_file_internal_links(md_file, file_mappings):
                self.updated_files.append(md_file)
        
        self.log(f"✅ Updated internal links in {len(self.updated_files)} files")
    
    def update_file_internal_links(self, md_file: Path, file_mappings: Dict[str, Path]) -> bool:
        """Update internal links in a single markdown file"""
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update various link patterns
            content = self._update_markdown_links(content, md_file, file_mappings)
            content = self._update_html_links(content, md_file, file_mappings)
            
            # Only write if content changed
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes = self._count_link_changes(original_content, content)
                self.log(f"✅ Updated {md_file} ({changes} link changes)")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error updating {md_file}: {str(e)}")
            return False
    
    def _update_markdown_links(self, content: str, md_file: Path, file_mappings: Dict[str, Path]) -> str:
        """Update markdown-style links [text](url)"""
        
        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip external links
            if self._is_external_link(link_url):
                return match.group(0)
            
            # Skip anchor links
            if link_url.startswith('#'):
                return match.group(0)
            
            # Update internal link
            new_url = self._resolve_internal_link(link_url, md_file, file_mappings)
            if new_url != link_url:
                return f"[{link_text}]({new_url})"
            
            return match.group(0)
        
        # Pattern for markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(link_pattern, replace_link, content)
    
    def _update_html_links(self, content: str, md_file: Path, file_mappings: Dict[str, Path]) -> str:
        """Update HTML-style links <a href="url">"""
        
        def replace_link(match):
            full_tag = match.group(0)
            href_url = match.group(1)
            
            # Skip external links
            if self._is_external_link(href_url):
                return full_tag
            
            # Skip anchor links
            if href_url.startswith('#'):
                return full_tag
            
            # Update internal link
            new_url = self._resolve_internal_link(href_url, md_file, file_mappings)
            if new_url != href_url:
                return full_tag.replace(f'href="{href_url}"', f'href="{new_url}"')
            
            return full_tag
        
        # Pattern for HTML links
        link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>.*?</a>'
        return re.sub(link_pattern, replace_link, content, flags=re.DOTALL)
    
    def _is_external_link(self, url: str) -> bool:
        """Check if a URL is external"""
        
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://')):
            return True
        
        # Check if it has a domain
        parsed = urlparse(url)
        return bool(parsed.netloc)
    
    def _resolve_internal_link(self, link_url: str, current_file: Path, file_mappings: Dict[str, Path]) -> str:
        """Resolve an internal link to the correct path"""
        
        # Clean up the URL
        clean_url = link_url.strip()
        
        # Remove fragment (anchor) part
        if '#' in clean_url:
            clean_url, fragment = clean_url.split('#', 1)
            fragment = '#' + fragment
        else:
            fragment = ''
        
        # Try to find the target file
        target_file = self._find_target_file(clean_url, current_file, file_mappings)
        
        if target_file:
            # Calculate relative path from current file to target file
            try:
                relative_path = self._calculate_relative_path(current_file, target_file)
                return relative_path + fragment
            except Exception as e:
                self.log(f"⚠️  Error calculating relative path from {current_file} to {target_file}: {e}")
                return link_url
        else:
            # Log broken link
            self.broken_links.append(f"{current_file}: Broken link to {link_url}")
            return link_url
    
    def _find_target_file(self, url: str, current_file: Path, file_mappings: Dict[str, Path]) -> Path:
        """Find the target file for a given URL"""
        
        # List of possible variations to try
        variations = [
            url,
            url.lstrip('/'),
            url + '.md' if not url.endswith('.md') else url,
            url.lstrip('/') + '.md' if not url.endswith('.md') else url.lstrip('/'),
        ]
        
        # If URL starts with /, try language-specific paths
        if url.startswith('/'):
            current_lang = current_file.relative_to(self.docs_dir).parts[0]
            variations.extend([
                f"{current_lang}{url}",
                f"{current_lang}{url}.md" if not url.endswith('.md') else f"{current_lang}{url}",
            ])
        
        # Try relative to current file's directory
        current_dir = current_file.parent.relative_to(self.docs_dir)
        if current_dir != Path('.'):
            variations.extend([
                str(current_dir / url),
                str(current_dir / (url + '.md')) if not url.endswith('.md') else str(current_dir / url),
            ])
        
        # Try each variation
        for variation in variations:
            if variation in file_mappings:
                return file_mappings[variation]
        
        return None
    
    def _calculate_relative_path(self, from_file: Path, to_file: Path) -> str:
        """Calculate relative path from one file to another"""
        
        from_dir = from_file.parent
        to_path = to_file.relative_to(self.docs_dir)
        from_path = from_dir.relative_to(self.docs_dir)
        
        # Calculate how many levels up we need to go
        if from_path == Path('.'):
            # From root docs directory
            return str(to_path)
        
        # Count levels
        levels_up = len(from_path.parts)
        
        # Build relative path
        relative_parts = ['..'] * levels_up + list(to_path.parts)
        return '/'.join(relative_parts)
    
    def _count_link_changes(self, original: str, updated: str) -> int:
        """Count the number of link changes made"""
        
        # Simple counting by comparing markdown links
        original_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', original)
        updated_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', updated)
        
        changes = 0
        for orig_link, upd_link in zip(original_links, updated_links):
            if orig_link[1] != upd_link[1]:  # Compare URLs
                changes += 1
        
        return changes
    
    def validate_updated_links(self):
        """Validate that updated links are correct"""
        
        self.log("Validating updated links...")
        
        validation_issues = []
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all markdown links
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                for link_text, link_url in links:
                    if not self._is_external_link(link_url) and not link_url.startswith('#'):
                        # Check if internal link exists
                        if not self._validate_internal_link(link_url, md_file):
                            validation_issues.append(f"{md_file}: Invalid link to {link_url}")
                
            except Exception as e:
                validation_issues.append(f"{md_file}: Error reading file - {str(e)}")
        
        if validation_issues:
            self.log(f"⚠️  Found {len(validation_issues)} validation issues")
            for issue in validation_issues[:10]:  # Show first 10
                self.log(f"  • {issue}")
            if len(validation_issues) > 10:
                self.log(f"  ... and {len(validation_issues) - 10} more")
        else:
            self.log("✅ All updated links are valid")
        
        return validation_issues
    
    def _validate_internal_link(self, link_url: str, current_file: Path) -> bool:
        """Validate that an internal link points to an existing file"""
        
        # Remove fragment
        if '#' in link_url:
            link_url = link_url.split('#')[0]
        
        if not link_url:  # Pure anchor link
            return True
        
        # Try to resolve the path
        if link_url.startswith('../'):
            # Relative path
            target_path = (current_file.parent / link_url).resolve()
        elif link_url.startswith('/'):
            # Absolute path from docs root
            target_path = self.docs_dir / link_url.lstrip('/')
        else:
            # Relative to current directory
            target_path = current_file.parent / link_url
        
        return target_path.exists()
    
    def generate_update_report(self):
        """Generate a detailed update report"""
        
        report_file = Path("internal-links-update-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Internal Links Update Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total files updated: {len(self.updated_files)}\n")
            f.write(f"Broken links found: {len(self.broken_links)}\n\n")
            
            if self.updated_files:
                f.write("Updated Files:\n")
                f.write("-" * 30 + "\n")
                for file_path in self.updated_files:
                    f.write(f"{file_path}\n")
                f.write("\n")
            
            if self.broken_links:
                f.write("Broken Links:\n")
                f.write("-" * 30 + "\n")
                for broken_link in self.broken_links:
                    f.write(f"{broken_link}\n")
                f.write("\n")
            
            f.write("Update Log:\n")
            f.write("-" * 30 + "\n")
            for log_entry in self.update_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Update report saved to: {report_file}")
    
    def run_update(self):
        """Run the complete internal links update process"""
        
        self.log("Starting internal links update...")
        self.log(f"Docs directory: {self.docs_dir}")
        
        if not self.docs_dir.exists():
            self.log(f"❌ Docs directory not found: {self.docs_dir}")
            return
        
        try:
            # Update all internal links
            self.update_all_internal_links()
            
            # Validate updated links
            validation_issues = self.validate_updated_links()
            
            # Generate report
            self.generate_update_report()
            
            self.log("✅ Internal links update completed!")
            
            if validation_issues:
                self.log(f"⚠️  Please review {len(validation_issues)} validation issues")
            
        except Exception as e:
            self.log(f"❌ Internal links update failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    docs_dir = "docs"
    
    if not Path(docs_dir).exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return
    
    updater = InternalLinkUpdater(docs_dir)
    updater.run_update()

if __name__ == "__main__":
    main()