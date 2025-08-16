#!/usr/bin/env python3
"""
Customize mkdocs-material theme to match FlutterX branding
"""

import re
from pathlib import Path
from typing import Dict, List

class ThemeCustomizer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.docs_dir = self.project_dir / "docs"
        self.overrides_dir = self.project_dir / "overrides"
        self.stylesheets_dir = self.docs_dir / "stylesheets"
        self.customization_log = []
        
    def log(self, message: str):
        """Log customization messages"""
        print(message)
        self.customization_log.append(message)
    
    def create_custom_css(self):
        """Create enhanced custom CSS for FlutterX branding"""
        
        self.log("Creating custom CSS...")
        
        css_content = """/* FlutterX Documentation Custom Styles */

:root {
  /* FlutterX Brand Colors */
  --flutterx-primary: #2196F3;
  --flutterx-primary-dark: #1976D2;
  --flutterx-accent: #03DAC6;
  --flutterx-secondary: #FF6B6B;
  --flutterx-success: #4CAF50;
  --flutterx-warning: #FF9800;
  --flutterx-error: #F44336;
  
  /* Custom spacing */
  --flutterx-spacing-xs: 0.25rem;
  --flutterx-spacing-sm: 0.5rem;
  --flutterx-spacing-md: 1rem;
  --flutterx-spacing-lg: 1.5rem;
  --flutterx-spacing-xl: 2rem;
}

/* Header customization */
.md-header {
  background: linear-gradient(135deg, var(--flutterx-primary) 0%, var(--flutterx-primary-dark) 100%);
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
}

.md-header__title {
  font-weight: 600;
  font-size: 1.1rem;
}

/* Logo styling */
.md-header__button.md-logo img,
.md-header__button.md-logo svg {
  height: 2rem;
  width: auto;
  filter: brightness(0) invert(1);
}

/* Navigation styling */
.md-nav__title {
  font-weight: 600;
  color: var(--flutterx-primary);
  border-bottom: 2px solid var(--flutterx-primary);
  padding-bottom: var(--flutterx-spacing-xs);
  margin-bottom: var(--flutterx-spacing-sm);
}

.md-nav__link--active {
  color: var(--flutterx-primary) !important;
  font-weight: 600;
}

.md-nav__link:hover {
  color: var(--flutterx-primary-dark);
}

/* Sidebar styling */
.md-sidebar {
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.md-sidebar--secondary {
  border-left: 1px solid #e0e0e0;
}

/* Content area styling */
.md-content {
  background: #ffffff;
}

.md-content__inner {
  padding-top: var(--flutterx-spacing-lg);
}

/* Typography enhancements */
.md-typeset h1 {
  color: var(--flutterx-primary);
  font-weight: 700;
  border-bottom: 3px solid var(--flutterx-accent);
  padding-bottom: var(--flutterx-spacing-sm);
  margin-bottom: var(--flutterx-spacing-lg);
}

.md-typeset h2 {
  color: var(--flutterx-primary-dark);
  font-weight: 600;
  border-left: 4px solid var(--flutterx-accent);
  padding-left: var(--flutterx-spacing-md);
  margin-left: calc(-1 * var(--flutterx-spacing-md));
}

.md-typeset h3 {
  color: var(--flutterx-primary);
  font-weight: 600;
}

/* Code blocks styling */
.md-typeset .highlight {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  overflow: hidden;
}

.md-typeset .highlight pre {
  margin: 0;
  border-radius: 0;
}

.md-typeset code {
  background: rgba(33, 150, 243, 0.1);
  color: var(--flutterx-primary-dark);
  padding: 0.1em 0.4em;
  border-radius: 4px;
  font-weight: 500;
}

/* Admonition styling */
.md-typeset .admonition {
  border-radius: 8px;
  border-left: 4px solid var(--flutterx-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.md-typeset .admonition-title {
  font-weight: 600;
  background: rgba(33, 150, 243, 0.1);
}

/* Button styling */
.md-button {
  background: var(--flutterx-primary);
  color: white;
  border-radius: 6px;
  padding: var(--flutterx-spacing-sm) var(--flutterx-spacing-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.md-button:hover {
  background: var(--flutterx-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

/* Search styling */
.md-search__form {
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.md-search__input {
  background: transparent;
  color: white;
}

.md-search__input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

/* Table styling */
.md-typeset table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.md-typeset table th {
  background: var(--flutterx-primary);
  color: white;
  font-weight: 600;
}

.md-typeset table tr:nth-child(even) {
  background: rgba(33, 150, 243, 0.05);
}

/* Language switcher styling */
.md-select__inner {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: white;
}

.md-select__list {
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.md-select__link {
  color: var(--flutterx-primary);
  padding: var(--flutterx-spacing-sm) var(--flutterx-spacing-md);
}

.md-select__link:hover {
  background: rgba(33, 150, 243, 0.1);
  color: var(--flutterx-primary-dark);
}

/* Footer styling */
.md-footer {
  background: linear-gradient(135deg, var(--flutterx-primary-dark) 0%, var(--flutterx-primary) 100%);
  color: white;
}

.md-footer-meta {
  background: rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media screen and (max-width: 76.1875em) {
  .md-nav--primary .md-nav__title {
    background: var(--flutterx-primary);
    color: white;
  }
  
  .md-nav--primary .md-nav__title .md-nav__button {
    color: white;
  }
}

/* Dark mode adjustments */
[data-md-color-scheme="slate"] {
  --flutterx-primary: #42A5F5;
  --flutterx-primary-dark: #1E88E5;
}

[data-md-color-scheme="slate"] .md-typeset h1 {
  color: var(--flutterx-primary);
}

[data-md-color-scheme="slate"] .md-typeset h2 {
  color: var(--flutterx-primary);
}

[data-md-color-scheme="slate"] .md-typeset code {
  background: rgba(66, 165, 245, 0.2);
  color: var(--flutterx-primary);
}

/* Animation enhancements */
.md-nav__link {
  transition: color 0.3s ease, padding-left 0.3s ease;
}

.md-nav__link:hover {
  padding-left: calc(var(--flutterx-spacing-md) + 4px);
}

.md-typeset .highlight {
  transition: box-shadow 0.3s ease;
}

.md-typeset .highlight:hover {
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
}

/* Custom badges */
.flutterx-badge {
  display: inline-block;
  padding: 0.2em 0.6em;
  font-size: 0.75em;
  font-weight: 600;
  line-height: 1;
  color: white;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 4px;
  background: var(--flutterx-accent);
}

.flutterx-badge--primary {
  background: var(--flutterx-primary);
}

.flutterx-badge--success {
  background: var(--flutterx-success);
}

.flutterx-badge--warning {
  background: var(--flutterx-warning);
}

.flutterx-badge--error {
  background: var(--flutterx-error);
}

/* Print styles */
@media print {
  .md-header,
  .md-sidebar,
  .md-footer {
    display: none;
  }
  
  .md-content {
    margin: 0;
    padding: 0;
  }
}
"""
        
        # Write the enhanced CSS
        css_file = self.stylesheets_dir / "extra.css"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        self.log(f"✅ Created enhanced CSS: {css_file}")
    
    def create_custom_templates(self):
        """Create custom template overrides"""
        
        self.log("Creating custom templates...")
        
        # Create overrides directory structure
        (self.overrides_dir / "partials").mkdir(parents=True, exist_ok=True)
        
        # Create custom footer
        footer_content = """<!-- Custom footer for FlutterX documentation -->
{% extends "partials/footer.html" %}

{% block footer %}
  <footer class="md-footer">
    <div class="md-footer-meta md-typeset">
      <div class="md-footer-meta__inner md-grid">
        <div class="md-footer-copyright">
          <div class="md-footer-copyright__highlight">
            © 2024 FlutterX Plugin Documentation
          </div>
          Built with ❤️ using 
          <a href="https://squidfunk.github.io/mkdocs-material/" target="_blank" rel="noopener">
            Material for MkDocs
          </a>
        </div>
        
        <div class="md-footer-social">
          {% for social in config.extra.social %}
            <a href="{{ social.link }}" target="_blank" rel="noopener" 
               title="{{ social.name or 'Social link' }}" class="md-footer-social__link">
              {% include ".icons/" ~ social.icon ~ ".svg" %}
            </a>
          {% endfor %}
        </div>
      </div>
    </div>
  </footer>
{% endblock %}"""
        
        footer_file = self.overrides_dir / "partials" / "footer.html"
        with open(footer_file, 'w', encoding='utf-8') as f:
            f.write(footer_content)
        
        self.log(f"✅ Created custom footer: {footer_file}")
        
        # Create custom header
        header_content = """<!-- Custom header for FlutterX documentation -->
{% extends "partials/header.html" %}

{% block header %}
  <header class="md-header" data-md-component="header">
    <nav class="md-header__inner md-grid" aria-label="{{ lang.nav.title }}">
      
      <!-- Link to home -->
      <a href="{{ config.extra.homepage | d(nav.homepage.url, true) | url }}" 
         title="{{ config.site_name | e }}" class="md-header__button md-logo" 
         aria-label="{{ config.site_name }}" data-md-component="logo">
        {% include "partials/logo.html" %}
      </a>
      
      <!-- Button to open drawer -->
      <label class="md-header__button md-icon" for="__drawer">
        {% include ".icons/material/menu" ~ ".svg" %}
      </label>
      
      <!-- Header title -->
      <div class="md-header__title" data-md-component="header-title">
        <div class="md-header__ellipsis">
          <div class="md-header__topic">
            <span class="md-ellipsis">
              {{ config.site_name }}
            </span>
          </div>
          <div class="md-header__topic" data-md-component="header-topic">
            <span class="md-ellipsis">
              {% if page and page.title and not page.is_homepage %}
                {{ page.title }}
              {% else %}
                {{ config.site_name }}
              {% endif %}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Color palette -->
      {% if config.theme.palette %}
        {% if not config.theme.palette is mapping %}
          {% for palette in config.theme.palette %}
            {% set scheme = palette.scheme | d("default", true) %}
            {% set primary = palette.primary | d("indigo", true) %}
            {% set accent = palette.accent | d("indigo", true) %}
            <input class="md-option" data-md-color-media="{{ palette.media }}" 
                   data-md-color-scheme="{{ scheme | replace(' ', '-') }}" 
                   data-md-color-primary="{{ primary | replace(' ', '-') }}" 
                   data-md-color-accent="{{ accent | replace(' ', '-') }}" 
                   {% if palette.toggle %}
                     aria-label="{{ palette.toggle.name }}"
                   {% else %}
                     aria-hidden="true"
                   {% endif %}
                   type="radio" name="__palette" id="__palette_{{ loop.index }}">
            {% if palette.toggle %}
              <label class="md-header__button md-icon" title="{{ palette.toggle.name }}" 
                     for="__palette_{{ loop.index0 or loop.length }}" hidden>
                {% include ".icons/" ~ palette.toggle.icon ~ ".svg" %}
              </label>
            {% endif %}
          {% endfor %}
        {% endif %}
      {% endif %}
      
      <!-- Site language selector -->
      {% if config.extra.alternate %}
        <div class="md-header__option">
          <div class="md-select">
            <button class="md-select__inner md-icon" aria-label="{{ lang.select.language.title }}">
              {% include ".icons/material/translate.svg" %}
            </button>
            <div class="md-select__list">
              {% for alt in config.extra.alternate %}
                <a href="{{ alt.link | url }}" hreflang="{{ alt.lang }}" class="md-select__link">
                  {{ alt.name }}
                </a>
              {% endfor %}
            </div>
          </div>
        </div>
      {% endif %}
      
      <!-- Button to open search modal -->
      {% if "material/search" in config.plugins %}
        <label class="md-header__button md-icon" for="__search">
          {% include ".icons/material/magnify.svg" %}
        </label>
        
        <!-- Search interface -->
        {% include "partials/search.html" %}
      {% endif %}
      
      <!-- Repository information -->
      {% if config.repo_url %}
        <div class="md-header__source">
          {% include "partials/source.html" %}
        </div>
      {% endif %}
    </nav>
  </header>
{% endblock %}"""
        
        header_file = self.overrides_dir / "partials" / "header.html"
        with open(header_file, 'w', encoding='utf-8') as f:
            f.write(header_content)
        
        self.log(f"✅ Created custom header: {header_file}")
    
    def update_mkdocs_config(self):
        """Update mkdocs.yml with enhanced theme configuration"""
        
        self.log("Updating mkdocs.yml theme configuration...")
        
        config_file = self.project_dir / "mkdocs.yml"
        
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update theme configuration
        theme_updates = {
            'font': {
                'text': 'Roboto',
                'code': 'Roboto Mono'
            },
            'icon': {
                'logo': 'material/flutter',
                'repo': 'fontawesome/brands/github'
            }
        }
        
        # Add font configuration
        font_config = """  font:
    text: Roboto
    code: Roboto Mono
  icon:
    logo: material/flutter
    repo: fontawesome/brands/github"""
        
        # Insert font config after palette section
        palette_end = content.find('        name: Switch to light mode')
        if palette_end != -1:
            insert_pos = content.find('\n', palette_end) + 1
            content = content[:insert_pos] + font_config + '\n' + content[insert_pos:]
        
        # Write back
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log("✅ Updated mkdocs.yml theme configuration")
    
    def create_favicon(self):
        """Create or copy favicon files"""
        
        self.log("Setting up favicon...")
        
        # The logo.svg should already exist in assets/images/
        logo_file = self.docs_dir / "assets" / "images" / "logo.svg"
        
        if logo_file.exists():
            self.log(f"✅ Logo file exists: {logo_file}")
        else:
            # Create a simple SVG logo as fallback
            svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#2196F3">
  <path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 11 5.16-1.26 9-5.45 9-11V7l-10-5z"/>
  <path d="M12 7L7 10v4c0 2.78 1.92 4.87 5 5.5 3.08-.63 5-2.72 5-5.5v-4l-5-3z" fill="white"/>
</svg>"""
            
            with open(logo_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            self.log(f"✅ Created fallback logo: {logo_file}")
    
    def generate_customization_report(self):
        """Generate a customization report"""
        
        report_file = self.project_dir / "theme-customization-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Theme Customization Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Customizations Applied:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.customization_log:
                f.write(f"{log_entry}\n")
            
            f.write("\nCustomization Features:\n")
            f.write("-" * 30 + "\n")
            f.write("• Enhanced CSS with FlutterX branding\n")
            f.write("• Custom color scheme and typography\n")
            f.write("• Improved navigation styling\n")
            f.write("• Custom header and footer templates\n")
            f.write("• Responsive design enhancements\n")
            f.write("• Dark mode support\n")
            f.write("• Print-friendly styles\n")
            f.write("• Animation and transition effects\n")
            f.write("• Custom badges and components\n")
            f.write("• Language switcher styling\n")
        
        self.log(f"Customization report saved to: {report_file}")
    
    def run_customization(self):
        """Run the complete theme customization process"""
        
        self.log("Starting theme customization...")
        self.log(f"Project directory: {self.project_dir}")
        
        try:
            # Create directories
            self.stylesheets_dir.mkdir(parents=True, exist_ok=True)
            self.overrides_dir.mkdir(parents=True, exist_ok=True)
            
            # Apply customizations
            self.create_custom_css()
            self.create_custom_templates()
            self.update_mkdocs_config()
            self.create_favicon()
            
            # Generate report
            self.generate_customization_report()
            
            self.log("✅ Theme customization completed successfully!")
            self.log("🎨 Your FlutterX documentation now has enhanced styling!")
            
        except Exception as e:
            self.log(f"❌ Theme customization failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    project_dir = "."
    
    customizer = ThemeCustomizer(project_dir)
    customizer.run_customization()

if __name__ == "__main__":
    main()