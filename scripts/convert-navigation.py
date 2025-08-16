#!/usr/bin/env python3
"""
Convert navigation structure from rspress config to mkdocs format
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class NavigationConverter:
    def __init__(self, rspress_config_path: str, mkdocs_config_path: str):
        self.rspress_config_path = Path(rspress_config_path)
        self.mkdocs_config_path = Path(mkdocs_config_path)
        self.conversion_log = []
        
    def log(self, message: str):
        """Log conversion messages"""
        print(message)
        self.conversion_log.append(message)
    
    def extract_rspress_navigation(self) -> Dict[str, Any]:
        """Extract navigation structure from rspress config"""
        
        self.log("Extracting navigation from rspress config...")
        
        if not self.rspress_config_path.exists():
            raise FileNotFoundError(f"Rspress config not found: {self.rspress_config_path}")
        
        with open(self.rspress_config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Parse the TypeScript config file to extract navigation
        navigation_data = self._parse_rspress_config(config_content)
        
        self.log(f"✅ Extracted navigation for {len(navigation_data)} languages")
        return navigation_data
    
    def _parse_rspress_config(self, content: str) -> Dict[str, Any]:
        """Parse rspress TypeScript config to extract navigation"""
        
        # This is a simplified parser for the rspress config
        # In a real implementation, you might want to use a proper TypeScript parser
        
        navigation_data = {}
        
        # Extract locales section
        locales_match = re.search(r'locales:\s*\[(.*?)\]', content, re.DOTALL)
        if not locales_match:
            self.log("⚠️  No locales found in rspress config")
            return navigation_data
        
        locales_content = locales_match.group(1)
        
        # Split into individual locale objects
        locale_objects = self._split_locale_objects(locales_content)
        
        for locale_obj in locale_objects:
            lang_data = self._parse_locale_object(locale_obj)
            if lang_data:
                navigation_data[lang_data['lang']] = lang_data
        
        return navigation_data
    
    def _split_locale_objects(self, locales_content: str) -> List[str]:
        """Split the locales content into individual locale objects"""
        
        objects = []
        brace_count = 0
        current_object = ""
        
        for char in locales_content:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            
            current_object += char
            
            if brace_count == 0 and current_object.strip():
                objects.append(current_object.strip().rstrip(','))
                current_object = ""
        
        return [obj for obj in objects if obj.strip()]
    
    def _parse_locale_object(self, locale_obj: str) -> Optional[Dict[str, Any]]:
        """Parse a single locale object"""
        
        # Extract language
        lang_match = re.search(r'lang:\s*[\'"]([^\'"]+)[\'"]', locale_obj)
        if not lang_match:
            return None
        
        lang = lang_match.group(1)
        
        # Extract label
        label_match = re.search(r'label:\s*[\'"]([^\'"]+)[\'"]', locale_obj)
        label = label_match.group(1) if label_match else lang
        
        # Extract title
        title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', locale_obj)
        title = title_match.group(1) if title_match else f"{label} Documentation"
        
        # Extract sidebar
        sidebar_match = re.search(r'sidebar:\s*{(.*?)}', locale_obj, re.DOTALL)
        sidebar = {}
        
        if sidebar_match:
            sidebar_content = sidebar_match.group(1)
            sidebar = self._parse_sidebar(sidebar_content)
        
        return {
            'lang': lang,
            'label': label,
            'title': title,
            'sidebar': sidebar
        }
    
    def _parse_sidebar(self, sidebar_content: str) -> Dict[str, List[Dict]]:
        """Parse sidebar content"""
        
        sidebar = {}
        
        # Find sidebar sections like "/zh/": [...]
        section_pattern = r'[\'"]([^\'"]+)[\'"]\s*:\s*\[(.*?)\]'
        sections = re.findall(section_pattern, sidebar_content, re.DOTALL)
        
        for section_path, section_content in sections:
            sidebar[section_path] = self._parse_sidebar_items(section_content)
        
        return sidebar
    
    def _parse_sidebar_items(self, items_content: str) -> List[Dict]:
        """Parse sidebar items"""
        
        items = []
        
        # Split into individual item objects
        item_objects = self._split_sidebar_items(items_content)
        
        for item_obj in item_objects:
            item = self._parse_sidebar_item(item_obj)
            if item:
                items.append(item)
        
        return items
    
    def _split_sidebar_items(self, items_content: str) -> List[str]:
        """Split sidebar items content into individual items"""
        
        items = []
        brace_count = 0
        current_item = ""
        
        for char in items_content:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            
            current_item += char
            
            if brace_count == 0 and current_item.strip():
                items.append(current_item.strip().rstrip(','))
                current_item = ""
        
        return [item for item in items if item.strip()]
    
    def _parse_sidebar_item(self, item_obj: str) -> Optional[Dict]:
        """Parse a single sidebar item"""
        
        # Extract text
        text_match = re.search(r'[\'"]text[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', item_obj)
        if not text_match:
            return None
        
        text = text_match.group(1)
        
        # Extract link (optional)
        link_match = re.search(r'[\'"]link[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', item_obj)
        link = link_match.group(1) if link_match else None
        
        # Extract items (sub-items)
        items_match = re.search(r'[\'"]items[\'"]\s*:\s*\[(.*?)\]', item_obj, re.DOTALL)
        items = []
        
        if items_match:
            items_content = items_match.group(1)
            items = self._parse_sidebar_items(items_content)
        
        item = {'text': text}
        if link:
            item['link'] = link
        if items:
            item['items'] = items
        
        return item
    
    def convert_to_mkdocs_navigation(self, rspress_nav: Dict[str, Any]) -> Dict[str, List]:
        """Convert rspress navigation to mkdocs format"""
        
        self.log("Converting navigation to mkdocs format...")
        
        mkdocs_nav = {}
        
        for lang, lang_data in rspress_nav.items():
            self.log(f"Converting navigation for language: {lang}")
            
            lang_nav = []
            
            # Add language home page
            lang_nav.append({f"{lang_data['label']}": f"{lang}/index.md"})
            
            # Convert sidebar items
            for section_path, items in lang_data['sidebar'].items():
                # Extract language from section path (e.g., "/zh/" -> "zh")
                section_lang = section_path.strip('/').split('/')[0] if '/' in section_path else lang
                
                if section_lang == lang:
                    converted_items = self._convert_sidebar_items(items, lang)
                    lang_nav.extend(converted_items)
            
            mkdocs_nav[lang] = lang_nav
        
        return mkdocs_nav
    
    def _convert_sidebar_items(self, items: List[Dict], lang: str) -> List[Dict]:
        """Convert sidebar items to mkdocs format"""
        
        converted = []
        
        for item in items:
            if 'link' in item and 'items' not in item:
                # Simple link item
                link = self._convert_link_path(item['link'], lang)
                converted.append({item['text']: link})
            elif 'items' in item:
                # Section with sub-items
                sub_items = self._convert_sidebar_items(item['items'], lang)
                converted.append({item['text']: sub_items})
            else:
                # Text-only item (section header)
                converted.append(item['text'])
        
        return converted
    
    def _convert_link_path(self, rspress_link: str, lang: str) -> str:
        """Convert rspress link path to mkdocs format"""
        
        # Remove leading slash
        if rspress_link.startswith('/'):
            rspress_link = rspress_link[1:]
        
        # Ensure .md extension
        if not rspress_link.endswith('.md'):
            rspress_link += '.md'
        
        return rspress_link
    
    def update_mkdocs_config(self, mkdocs_nav: Dict[str, List]):
        """Update mkdocs.yml with the new navigation"""
        
        self.log("Updating mkdocs.yml with new navigation...")
        
        # Read current mkdocs config
        with open(self.mkdocs_config_path, 'r', encoding='utf-8') as f:
            mkdocs_config = yaml.safe_load(f)
        
        # Create combined navigation
        combined_nav = []
        
        # Add main index
        combined_nav.append({'首页': 'index.md'})
        
        # Add language-specific navigation
        for lang in ['zh', 'en', 'ja']:
            if lang in mkdocs_nav:
                lang_section = {
                    '简体中文' if lang == 'zh' else 'English' if lang == 'en' else '日本語': 
                    mkdocs_nav[lang]
                }
                combined_nav.append(lang_section)
        
        # Update the config
        mkdocs_config['nav'] = combined_nav
        
        # Write back to file
        with open(self.mkdocs_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(mkdocs_config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        self.log("✅ Updated mkdocs.yml with new navigation")
    
    def generate_conversion_report(self, rspress_nav: Dict[str, Any], mkdocs_nav: Dict[str, List]):
        """Generate a conversion report"""
        
        report_file = Path("navigation-conversion-report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Navigation Conversion Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Source (Rspress) Navigation:\n")
            f.write("-" * 30 + "\n")
            
            for lang, lang_data in rspress_nav.items():
                f.write(f"\nLanguage: {lang} ({lang_data['label']})\n")
                f.write(f"Title: {lang_data['title']}\n")
                
                for section_path, items in lang_data['sidebar'].items():
                    f.write(f"Section: {section_path}\n")
                    self._write_items_to_report(f, items, indent=2)
            
            f.write("\n\nTarget (MkDocs) Navigation:\n")
            f.write("-" * 30 + "\n")
            
            for lang, nav_items in mkdocs_nav.items():
                f.write(f"\nLanguage: {lang}\n")
                self._write_mkdocs_nav_to_report(f, nav_items, indent=2)
            
            f.write("\n\nConversion Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.conversion_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Conversion report saved to: {report_file}")
    
    def _write_items_to_report(self, f, items: List[Dict], indent: int = 0):
        """Write sidebar items to report file"""
        
        prefix = "  " * indent
        
        for item in items:
            if isinstance(item, dict):
                f.write(f"{prefix}- {item.get('text', 'Unknown')}")
                if 'link' in item:
                    f.write(f" -> {item['link']}")
                f.write("\n")
                
                if 'items' in item:
                    self._write_items_to_report(f, item['items'], indent + 1)
            else:
                f.write(f"{prefix}- {item}\n")
    
    def _write_mkdocs_nav_to_report(self, f, nav_items: List, indent: int = 0):
        """Write mkdocs navigation to report file"""
        
        prefix = "  " * indent
        
        for item in nav_items:
            if isinstance(item, dict):
                for key, value in item.items():
                    f.write(f"{prefix}- {key}")
                    if isinstance(value, str):
                        f.write(f" -> {value}")
                    f.write("\n")
                    
                    if isinstance(value, list):
                        self._write_mkdocs_nav_to_report(f, value, indent + 1)
            else:
                f.write(f"{prefix}- {item}\n")
    
    def run_conversion(self):
        """Run the complete navigation conversion process"""
        
        self.log("Starting navigation conversion...")
        self.log(f"Source: {self.rspress_config_path}")
        self.log(f"Target: {self.mkdocs_config_path}")
        
        try:
            # Extract rspress navigation
            rspress_nav = self.extract_rspress_navigation()
            
            # Convert to mkdocs format
            mkdocs_nav = self.convert_to_mkdocs_navigation(rspress_nav)
            
            # Update mkdocs config
            self.update_mkdocs_config(mkdocs_nav)
            
            # Generate report
            self.generate_conversion_report(rspress_nav, mkdocs_nav)
            
            self.log("✅ Navigation conversion completed successfully!")
            
        except Exception as e:
            self.log(f"❌ Navigation conversion failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    rspress_config = "../rspress-template/rspress.config.ts"
    mkdocs_config = "mkdocs.yml"
    
    if not Path(rspress_config).exists():
        print(f"❌ Rspress config not found: {rspress_config}")
        return
    
    if not Path(mkdocs_config).exists():
        print(f"❌ MkDocs config not found: {mkdocs_config}")
        return
    
    converter = NavigationConverter(rspress_config, mkdocs_config)
    converter.run_conversion()

if __name__ == "__main__":
    main()