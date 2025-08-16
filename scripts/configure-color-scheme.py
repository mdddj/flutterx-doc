#!/usr/bin/env python3
"""
Configure color scheme and typography to match FlutterX branding
"""

import re
from pathlib import Path

class ColorSchemeConfigurator:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config_file = self.project_dir / "mkdocs.yml"
        self.configuration_log = []
        
    def log(self, message: str):
        """Log configuration messages"""
        print(message)
        self.configuration_log.append(message)
    
    def update_color_palette(self):
        """Update the color palette in mkdocs.yml"""
        
        self.log("Updating color palette configuration...")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhanced palette configuration
        new_palette = """  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: cyan
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    
    # Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: cyan
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
    
    # Manual light mode
    - scheme: default
      primary: blue
      accent: cyan
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    
    # Manual dark mode
    - scheme: slate
      primary: blue
      accent: cyan
      toggle:
        icon: material/brightness-4
        name: Switch to light mode"""
        
        # Replace existing palette section
        palette_pattern = r'  palette:.*?(?=\n\w|\n#|\ntheme:|\nplugins:|\Z)'
        content = re.sub(palette_pattern, new_palette, content, flags=re.DOTALL)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log("✅ Updated color palette configuration")
    
    def create_color_variables_css(self):
        """Create CSS with comprehensive color variables"""
        
        self.log("Creating color variables CSS...")
        
        color_css = """/* FlutterX Color Scheme Variables */

/* Light mode colors */
[data-md-color-scheme="default"] {
  /* Primary colors */
  --md-primary-fg-color: #2196F3;
  --md-primary-fg-color--light: #42A5F5;
  --md-primary-fg-color--dark: #1976D2;
  
  /* Accent colors */
  --md-accent-fg-color: #00BCD4;
  --md-accent-fg-color--transparent: rgba(0, 188, 212, 0.1);
  
  /* Background colors */
  --md-default-bg-color: #ffffff;
  --md-default-bg-color--light: #f8f9fa;
  --md-default-bg-color--lighter: #f1f3f4;
  --md-default-bg-color--lightest: #fafbfc;
  
  /* Foreground colors */
  --md-default-fg-color: #212121;
  --md-default-fg-color--light: #424242;
  --md-default-fg-color--lighter: #757575;
  --md-default-fg-color--lightest: #9e9e9e;
  
  /* Code colors */
  --md-code-bg-color: rgba(33, 150, 243, 0.05);
  --md-code-fg-color: #1976D2;
  
  /* Admonition colors */
  --md-admonition-bg-color: rgba(33, 150, 243, 0.05);
  --md-admonition-fg-color: var(--md-primary-fg-color);
  
  /* Success colors */
  --md-success-fg-color: #4CAF50;
  --md-success-bg-color: rgba(76, 175, 80, 0.1);
  
  /* Warning colors */
  --md-warning-fg-color: #FF9800;
  --md-warning-bg-color: rgba(255, 152, 0, 0.1);
  
  /* Error colors */
  --md-error-fg-color: #F44336;
  --md-error-bg-color: rgba(244, 67, 54, 0.1);
  
  /* Info colors */
  --md-info-fg-color: #2196F3;
  --md-info-bg-color: rgba(33, 150, 243, 0.1);
}

/* Dark mode colors */
[data-md-color-scheme="slate"] {
  /* Primary colors */
  --md-primary-fg-color: #42A5F5;
  --md-primary-fg-color--light: #64B5F6;
  --md-primary-fg-color--dark: #1E88E5;
  
  /* Accent colors */
  --md-accent-fg-color: #26C6DA;
  --md-accent-fg-color--transparent: rgba(38, 198, 218, 0.1);
  
  /* Background colors */
  --md-default-bg-color: #1a1a1a;
  --md-default-bg-color--light: #2d2d2d;
  --md-default-bg-color--lighter: #404040;
  --md-default-bg-color--lightest: #525252;
  
  /* Foreground colors */
  --md-default-fg-color: #ffffff;
  --md-default-fg-color--light: #e0e0e0;
  --md-default-fg-color--lighter: #bdbdbd;
  --md-default-fg-color--lightest: #9e9e9e;
  
  /* Code colors */
  --md-code-bg-color: rgba(66, 165, 245, 0.1);
  --md-code-fg-color: #42A5F5;
  
  /* Admonition colors */
  --md-admonition-bg-color: rgba(66, 165, 245, 0.1);
  --md-admonition-fg-color: var(--md-primary-fg-color);
  
  /* Success colors */
  --md-success-fg-color: #66BB6A;
  --md-success-bg-color: rgba(102, 187, 106, 0.1);
  
  /* Warning colors */
  --md-warning-fg-color: #FFB74D;
  --md-warning-bg-color: rgba(255, 183, 77, 0.1);
  
  /* Error colors */
  --md-error-fg-color: #EF5350;
  --md-error-bg-color: rgba(239, 83, 80, 0.1);
  
  /* Info colors */
  --md-info-fg-color: #42A5F5;
  --md-info-bg-color: rgba(66, 165, 245, 0.1);
}

/* Apply color variables to components */
.md-header {
  background: linear-gradient(135deg, var(--md-primary-fg-color) 0%, var(--md-primary-fg-color--dark) 100%);
}

.md-nav__title {
  color: var(--md-primary-fg-color);
  border-bottom-color: var(--md-accent-fg-color);
}

.md-nav__link--active {
  color: var(--md-primary-fg-color) !important;
}

.md-typeset h1 {
  color: var(--md-primary-fg-color);
  border-bottom-color: var(--md-accent-fg-color);
}

.md-typeset h2 {
  color: var(--md-primary-fg-color--dark);
  border-left-color: var(--md-accent-fg-color);
}

.md-typeset h3 {
  color: var(--md-primary-fg-color);
}

.md-typeset code {
  background: var(--md-code-bg-color);
  color: var(--md-code-fg-color);
}

.md-button {
  background: var(--md-primary-fg-color);
}

.md-button:hover {
  background: var(--md-primary-fg-color--dark);
}

/* Admonition color variants */
.md-typeset .admonition.note {
  border-left-color: var(--md-info-fg-color);
}

.md-typeset .admonition.note > .admonition-title {
  background: var(--md-info-bg-color);
  color: var(--md-info-fg-color);
}

.md-typeset .admonition.tip {
  border-left-color: var(--md-success-fg-color);
}

.md-typeset .admonition.tip > .admonition-title {
  background: var(--md-success-bg-color);
  color: var(--md-success-fg-color);
}

.md-typeset .admonition.warning {
  border-left-color: var(--md-warning-fg-color);
}

.md-typeset .admonition.warning > .admonition-title {
  background: var(--md-warning-bg-color);
  color: var(--md-warning-fg-color);
}

.md-typeset .admonition.danger {
  border-left-color: var(--md-error-fg-color);
}

.md-typeset .admonition.danger > .admonition-title {
  background: var(--md-error-bg-color);
  color: var(--md-error-fg-color);
}
"""
        
        # Append to existing CSS
        css_file = self.project_dir / "docs" / "stylesheets" / "extra.css"
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write('\n\n' + color_css)
        
        self.log(f"✅ Created color variables CSS: {css_file}")
    
    def generate_configuration_report(self):
        """Generate configuration report"""
        
        report_file = self.project_dir / "color-scheme-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Color Scheme Configuration Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Configuration Applied:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.configuration_log:
                f.write(f"{log_entry}\n")
            
            f.write("\nColor Scheme Features:\n")
            f.write("-" * 30 + "\n")
            f.write("• Automatic light/dark mode detection\n")
            f.write("• Manual theme toggle\n")
            f.write("• FlutterX brand colors (Blue primary, Cyan accent)\n")
            f.write("• Comprehensive color variables\n")
            f.write("• Dark mode optimized colors\n")
            f.write("• Semantic color system\n")
            f.write("• Admonition color variants\n")
            f.write("• Consistent component theming\n")
        
        self.log(f"Configuration report saved to: {report_file}")
    
    def run_configuration(self):
        """Run the complete color scheme configuration"""
        
        self.log("Starting color scheme configuration...")
        
        try:
            # Apply configurations
            self.update_color_palette()
            self.create_color_variables_css()
            
            # Generate report
            self.generate_configuration_report()
            
            self.log("✅ Color scheme configuration completed!")
            self.log("🎨 Your documentation now has FlutterX brand colors!")
            
        except Exception as e:
            self.log(f"❌ Color scheme configuration failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    project_dir = "."
    
    configurator = ColorSchemeConfigurator(project_dir)
    configurator.run_configuration()

if __name__ == "__main__":
    main()