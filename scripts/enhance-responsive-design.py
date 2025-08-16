#!/usr/bin/env python3
"""
Enhance responsive design for mobile and tablet devices
"""

from pathlib import Path

class ResponsiveDesignEnhancer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.stylesheets_dir = self.project_dir / "docs" / "stylesheets"
        self.enhancement_log = []
        
    def log(self, message: str):
        """Log enhancement messages"""
        print(message)
        self.enhancement_log.append(message)
    
    def create_responsive_css(self):
        """Create responsive design enhancements"""
        
        self.log("Creating responsive design enhancements...")
        
        responsive_css = """/* Responsive Design Enhancements for FlutterX Documentation */

/* Mobile-first approach */
@media screen and (max-width: 480px) {
  /* Header adjustments */
  .md-header__title {
    font-size: 0.9rem;
  }
  
  .md-header__button.md-logo img,
  .md-header__button.md-logo svg {
    height: 1.5rem;
  }
  
  /* Navigation adjustments */
  .md-nav--primary .md-nav__title {
    font-size: 0.9rem;
    padding: var(--flutterx-spacing-sm);
  }
  
  .md-nav__link {
    font-size: 0.85rem;
    padding: var(--flutterx-spacing-xs) var(--flutterx-spacing-sm);
  }
  
  /* Content adjustments */
  .md-content__inner {
    padding: var(--flutterx-spacing-sm);
  }
  
  .md-typeset h1 {
    font-size: 1.5rem;
    margin-bottom: var(--flutterx-spacing-md);
  }
  
  .md-typeset h2 {
    font-size: 1.25rem;
    padding-left: var(--flutterx-spacing-sm);
    margin-left: calc(-1 * var(--flutterx-spacing-sm));
  }
  
  .md-typeset h3 {
    font-size: 1.1rem;
  }
  
  /* Code blocks */
  .md-typeset .highlight {
    margin: var(--flutterx-spacing-sm) 0;
  }
  
  .md-typeset pre {
    font-size: 0.75rem;
    padding: var(--flutterx-spacing-sm);
  }
  
  /* Tables */
  .md-typeset table {
    font-size: 0.8rem;
  }
  
  .md-typeset table th,
  .md-typeset table td {
    padding: var(--flutterx-spacing-xs);
  }
  
  /* Search */
  .md-search__form {
    height: 2.5rem;
  }
  
  .md-search__input {
    font-size: 0.9rem;
  }
}

/* Tablet adjustments */
@media screen and (min-width: 481px) and (max-width: 768px) {
  .md-header__title {
    font-size: 1rem;
  }
  
  .md-content__inner {
    padding: var(--flutterx-spacing-md);
  }
  
  .md-typeset h1 {
    font-size: 1.75rem;
  }
  
  .md-typeset h2 {
    font-size: 1.4rem;
  }
  
  .md-typeset h3 {
    font-size: 1.2rem;
  }
  
  .md-nav__link {
    font-size: 0.9rem;
  }
}

/* Large tablet and small desktop */
@media screen and (min-width: 769px) and (max-width: 1024px) {
  .md-sidebar {
    width: 12rem;
  }
  
  .md-content {
    margin-left: 12rem;
  }
  
  .md-nav__link {
    font-size: 0.9rem;
    padding: var(--flutterx-spacing-xs) var(--flutterx-spacing-sm);
  }
}

/* Touch-friendly enhancements */
@media (hover: none) and (pointer: coarse) {
  /* Larger touch targets */
  .md-nav__link {
    min-height: 2.5rem;
    display: flex;
    align-items: center;
  }
  
  .md-header__button {
    min-width: 2.5rem;
    min-height: 2.5rem;
  }
  
  .md-select__inner {
    min-height: 2.5rem;
    padding: var(--flutterx-spacing-sm);
  }
  
  /* Remove hover effects on touch devices */
  .md-nav__link:hover {
    padding-left: var(--flutterx-spacing-sm);
  }
  
  .md-typeset .highlight:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .md-header__button.md-logo img,
  .md-header__button.md-logo svg {
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
  }
}

/* Landscape orientation on mobile */
@media screen and (max-width: 768px) and (orientation: landscape) {
  .md-header {
    height: 3rem;
  }
  
  .md-nav--primary .md-nav__title {
    height: 3rem;
    line-height: 3rem;
  }
  
  .md-content {
    padding-top: 3rem;
  }
}

/* Print optimizations */
@media print {
  /* Hide interactive elements */
  .md-header,
  .md-sidebar,
  .md-footer,
  .md-search,
  .md-select {
    display: none !important;
  }
  
  /* Optimize content for print */
  .md-content {
    margin: 0;
    padding: 0;
    max-width: none;
  }
  
  .md-content__inner {
    padding: 0;
  }
  
  /* Typography for print */
  .md-typeset {
    font-size: 12pt;
    line-height: 1.4;
  }
  
  .md-typeset h1 {
    font-size: 18pt;
    page-break-after: avoid;
  }
  
  .md-typeset h2 {
    font-size: 16pt;
    page-break-after: avoid;
  }
  
  .md-typeset h3 {
    font-size: 14pt;
    page-break-after: avoid;
  }
  
  /* Code blocks for print */
  .md-typeset .highlight {
    border: 1px solid #ccc;
    page-break-inside: avoid;
  }
  
  .md-typeset pre {
    font-size: 10pt;
    white-space: pre-wrap;
  }
  
  /* Tables for print */
  .md-typeset table {
    page-break-inside: avoid;
    font-size: 10pt;
  }
  
  /* Links for print */
  .md-typeset a[href^="http"]:after {
    content: " (" attr(href) ")";
    font-size: 10pt;
    color: #666;
  }
}

/* Accessibility enhancements */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  :root {
    --flutterx-primary: #0066CC;
    --flutterx-primary-dark: #004499;
  }
  
  .md-typeset h1,
  .md-typeset h2,
  .md-typeset h3 {
    color: #000;
  }
  
  .md-nav__link {
    border-bottom: 1px solid transparent;
  }
  
  .md-nav__link--active {
    border-bottom-color: var(--flutterx-primary);
  }
}

/* Dark mode preferences */
@media (prefers-color-scheme: dark) {
  [data-md-color-scheme="default"] {
    --md-default-bg-color: #1a1a1a;
    --md-default-fg-color: #ffffff;
  }
}

/* Focus indicators for keyboard navigation */
.md-nav__link:focus,
.md-header__button:focus,
.md-select__inner:focus {
  outline: 2px solid var(--flutterx-accent);
  outline-offset: 2px;
}

/* Skip to content link for screen readers */
.skip-to-content {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--flutterx-primary);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 1000;
}

.skip-to-content:focus {
  top: 6px;
}
"""
        
        # Append to existing CSS file
        css_file = self.stylesheets_dir / "extra.css"
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write('\n\n' + responsive_css)
        
        self.log(f"✅ Enhanced responsive CSS: {css_file}")
    
    def create_mobile_navigation_template(self):
        """Create mobile-optimized navigation template"""
        
        self.log("Creating mobile navigation template...")
        
        overrides_dir = self.project_dir / "overrides" / "partials"
        overrides_dir.mkdir(parents=True, exist_ok=True)
        
        mobile_nav_content = """<!-- Mobile-optimized navigation -->
{% extends "partials/nav.html" %}

{% block nav %}
  <nav class="md-nav md-nav--primary" aria-label="{{ lang.nav.title }}" data-md-level="0">
    
    <!-- Site title -->
    <label class="md-nav__title" for="__drawer">
      <a href="{{ config.extra.homepage | d(nav.homepage.url, true) | url }}" 
         title="{{ config.site_name | e }}" class="md-nav__button md-logo" 
         aria-label="{{ config.site_name }}" data-md-component="logo">
        {% include "partials/logo.html" %}
      </a>
      {{ config.site_name }}
    </label>
    
    <!-- Navigation list -->
    <ul class="md-nav__list" data-md-scrollfix>
      {% for nav_item in nav %}
        {% if nav_item.children %}
          <li class="md-nav__item md-nav__item--nested">
            
            <!-- Section header -->
            <input class="md-nav__toggle md-toggle" 
                   data-md-toggle="nav-{{ loop.index }}" 
                   type="checkbox" id="nav-{{ loop.index }}">
            
            <label class="md-nav__link" for="nav-{{ loop.index }}">
              {{ nav_item.title }}
              <span class="md-nav__icon md-icon">
                {% include ".icons/material/chevron-right.svg" %}
              </span>
            </label>
            
            <!-- Nested navigation -->
            <nav class="md-nav" aria-label="{{ nav_item.title }}" data-md-level="1">
              <label class="md-nav__title" for="nav-{{ loop.index }}">
                <span class="md-nav__icon md-icon">
                  {% include ".icons/material/arrow-left.svg" %}
                </span>
                {{ nav_item.title }}
              </label>
              
              <ul class="md-nav__list" data-md-scrollfix>
                {% for nav_item in nav_item.children %}
                  <li class="md-nav__item">
                    <a href="{{ nav_item.url | url }}" class="md-nav__link">
                      {{ nav_item.title }}
                    </a>
                  </li>
                {% endfor %}
              </ul>
            </nav>
          </li>
        {% else %}
          <li class="md-nav__item">
            <a href="{{ nav_item.url | url }}" class="md-nav__link">
              {{ nav_item.title }}
            </a>
          </li>
        {% endif %}
      {% endfor %}
    </ul>
  </nav>
{% endblock %}"""
        
        nav_file = overrides_dir / "nav.html"
        with open(nav_file, 'w', encoding='utf-8') as f:
            f.write(mobile_nav_content)
        
        self.log(f"✅ Created mobile navigation template: {nav_file}")
    
    def generate_enhancement_report(self):
        """Generate enhancement report"""
        
        report_file = self.project_dir / "responsive-design-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Responsive Design Enhancement Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Enhancements Applied:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.enhancement_log:
                f.write(f"{log_entry}\n")
            
            f.write("\nResponsive Features:\n")
            f.write("-" * 30 + "\n")
            f.write("• Mobile-first responsive design\n")
            f.write("• Touch-friendly interface elements\n")
            f.write("• Optimized typography for different screen sizes\n")
            f.write("• Landscape orientation support\n")
            f.write("• High DPI display optimization\n")
            f.write("• Print-friendly styles\n")
            f.write("• Accessibility enhancements\n")
            f.write("• Reduced motion support\n")
            f.write("• High contrast mode support\n")
            f.write("• Keyboard navigation improvements\n")
        
        self.log(f"Enhancement report saved to: {report_file}")
    
    def run_enhancement(self):
        """Run the complete responsive design enhancement"""
        
        self.log("Starting responsive design enhancement...")
        
        try:
            # Create enhancements
            self.create_responsive_css()
            self.create_mobile_navigation_template()
            
            # Generate report
            self.generate_enhancement_report()
            
            self.log("✅ Responsive design enhancement completed!")
            self.log("📱 Your documentation is now mobile-friendly!")
            
        except Exception as e:
            self.log(f"❌ Responsive design enhancement failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    project_dir = "."
    
    enhancer = ResponsiveDesignEnhancer(project_dir)
    enhancer.run_enhancement()

if __name__ == "__main__":
    main()