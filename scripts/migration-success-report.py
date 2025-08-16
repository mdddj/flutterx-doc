#!/usr/bin/env python3
"""
Generate migration success report for FlutterX documentation
"""

import json
import time
from pathlib import Path
import subprocess
import sys

class MigrationSuccessReporter:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.success_metrics = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages"""
        print(f"[{level}] {message}")
    
    def analyze_content_migration(self) -> dict:
        """Analyze content migration success"""
        
        self.log("📄 Analyzing content migration...")
        
        docs_dir = self.project_dir / "docs"
        languages = ["zh", "en", "ja"]
        
        metrics = {
            'languages_migrated': 0,
            'total_markdown_files': 0,
            'files_per_language': {},
            'content_structure_complete': True
        }
        
        for lang in languages:
            lang_dir = docs_dir / lang
            if lang_dir.exists():
                metrics['languages_migrated'] += 1
                md_files = list(lang_dir.rglob("*.md"))
                metrics['files_per_language'][lang] = len(md_files)
                metrics['total_markdown_files'] += len(md_files)
            else:
                metrics['content_structure_complete'] = False
        
        self.log(f"✅ Languages migrated: {metrics['languages_migrated']}/3")
        self.log(f"✅ Total markdown files: {metrics['total_markdown_files']}")
        
        return metrics
    
    def analyze_asset_migration(self) -> dict:
        """Analyze asset migration success"""
        
        self.log("🖼️  Analyzing asset migration...")
        
        assets_dir = self.project_dir / "docs" / "assets"
        
        metrics = {
            'assets_directory_exists': assets_dir.exists(),
            'total_images': 0,
            'image_types': {},
            'total_size_mb': 0
        }
        
        if assets_dir.exists():
            image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
            
            for ext in image_extensions:
                images = list(assets_dir.rglob(f"*{ext}"))
                if images:
                    metrics['image_types'][ext] = len(images)
                    metrics['total_images'] += len(images)
            
            # Calculate total size
            total_size = 0
            for file_path in assets_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            
            metrics['total_size_mb'] = total_size / (1024 * 1024)
        
        self.log(f"✅ Assets directory: {'exists' if metrics['assets_directory_exists'] else 'missing'}")
        self.log(f"✅ Total images: {metrics['total_images']}")
        self.log(f"✅ Assets size: {metrics['total_size_mb']:.2f} MB")
        
        return metrics
    
    def analyze_navigation_structure(self) -> dict:
        """Analyze navigation structure"""
        
        self.log("🧭 Analyzing navigation structure...")
        
        mkdocs_config = self.project_dir / "mkdocs.yml"
        
        metrics = {
            'config_exists': mkdocs_config.exists(),
            'has_navigation': False,
            'multi_language_nav': False,
            'navigation_items': 0
        }
        
        if mkdocs_config.exists():
            try:
                with open(mkdocs_config, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metrics['has_navigation'] = 'nav:' in content
                
                # Check for multi-language navigation
                language_indicators = ["简体中文", "English", "日本語"]
                metrics['multi_language_nav'] = all(lang in content for lang in language_indicators)
                
                # Count navigation items (rough estimate)
                nav_lines = [line for line in content.split('\n') if line.strip().startswith('- ')]
                metrics['navigation_items'] = len(nav_lines)
                
            except Exception as e:
                self.log(f"Error reading mkdocs.yml: {e}", "WARNING")
        
        self.log(f"✅ Config file: {'exists' if metrics['config_exists'] else 'missing'}")
        self.log(f"✅ Navigation: {'configured' if metrics['has_navigation'] else 'missing'}")
        self.log(f"✅ Multi-language nav: {'yes' if metrics['multi_language_nav'] else 'no'}")
        self.log(f"✅ Navigation items: {metrics['navigation_items']}")
        
        return metrics
    
    def analyze_theme_customization(self) -> dict:
        """Analyze theme customization"""
        
        self.log("🎨 Analyzing theme customization...")
        
        metrics = {
            'custom_css_exists': False,
            'overrides_directory': False,
            'theme_configured': False
        }
        
        # Check custom CSS
        css_file = self.project_dir / "docs" / "stylesheets" / "extra.css"
        metrics['custom_css_exists'] = css_file.exists()
        
        # Check overrides directory
        overrides_dir = self.project_dir / "overrides"
        metrics['overrides_directory'] = overrides_dir.exists()
        
        # Check theme configuration
        mkdocs_config = self.project_dir / "mkdocs.yml"
        if mkdocs_config.exists():
            try:
                with open(mkdocs_config, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metrics['theme_configured'] = 'theme:' in content and 'material' in content
                
            except Exception:
                pass
        
        self.log(f"✅ Custom CSS: {'exists' if metrics['custom_css_exists'] else 'missing'}")
        self.log(f"✅ Theme overrides: {'exists' if metrics['overrides_directory'] else 'missing'}")
        self.log(f"✅ Theme configured: {'yes' if metrics['theme_configured'] else 'no'}")
        
        return metrics
    
    def analyze_build_readiness(self) -> dict:
        """Analyze build readiness"""
        
        self.log("🔨 Analyzing build readiness...")
        
        metrics = {
            'requirements_file': False,
            'build_scripts': 0,
            'test_scripts': 0,
            'site_buildable': False
        }
        
        # Check requirements file
        requirements_file = self.project_dir / "requirements.txt"
        metrics['requirements_file'] = requirements_file.exists()
        
        # Check build scripts
        scripts_dir = self.project_dir / "scripts"
        if scripts_dir.exists():
            build_scripts = [
                "build-site.py",
                "build-automation.py",
                "production-build.py",
                "dev-server.py"
            ]
            
            for script in build_scripts:
                if (scripts_dir / script).exists():
                    metrics['build_scripts'] += 1
        
        # Check test scripts
        tests_dir = self.project_dir / "tests"
        if tests_dir.exists():
            test_files = list(tests_dir.glob("test_*.py"))
            metrics['test_scripts'] = len(test_files)
        
        # Check if site can be built (basic check)
        site_dir = self.project_dir / "site"
        metrics['site_buildable'] = site_dir.exists()
        
        self.log(f"✅ Requirements file: {'exists' if metrics['requirements_file'] else 'missing'}")
        self.log(f"✅ Build scripts: {metrics['build_scripts']}/4")
        self.log(f"✅ Test scripts: {metrics['test_scripts']}")
        self.log(f"✅ Site buildable: {'yes' if metrics['site_buildable'] else 'no'}")
        
        return metrics
    
    def calculate_overall_success_rate(self) -> float:
        """Calculate overall migration success rate"""
        
        total_checks = 0
        passed_checks = 0
        
        # Content migration checks
        content_metrics = self.success_metrics.get('content_migration', {})
        total_checks += 3
        if content_metrics.get('languages_migrated', 0) >= 3:
            passed_checks += 1
        if content_metrics.get('total_markdown_files', 0) > 100:
            passed_checks += 1
        if content_metrics.get('content_structure_complete', False):
            passed_checks += 1
        
        # Asset migration checks
        asset_metrics = self.success_metrics.get('asset_migration', {})
        total_checks += 2
        if asset_metrics.get('assets_directory_exists', False):
            passed_checks += 1
        if asset_metrics.get('total_images', 0) > 50:
            passed_checks += 1
        
        # Navigation checks
        nav_metrics = self.success_metrics.get('navigation_structure', {})
        total_checks += 3
        if nav_metrics.get('config_exists', False):
            passed_checks += 1
        if nav_metrics.get('has_navigation', False):
            passed_checks += 1
        if nav_metrics.get('multi_language_nav', False):
            passed_checks += 1
        
        # Theme checks
        theme_metrics = self.success_metrics.get('theme_customization', {})
        total_checks += 2
        if theme_metrics.get('custom_css_exists', False):
            passed_checks += 1
        if theme_metrics.get('theme_configured', False):
            passed_checks += 1
        
        # Build readiness checks
        build_metrics = self.success_metrics.get('build_readiness', {})
        total_checks += 3
        if build_metrics.get('requirements_file', False):
            passed_checks += 1
        if build_metrics.get('build_scripts', 0) >= 3:
            passed_checks += 1
        if build_metrics.get('test_scripts', 0) >= 3:
            passed_checks += 1
        
        return (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    def generate_success_report(self) -> dict:
        """Generate comprehensive success report"""
        
        self.log("📊 Generating migration success report...")
        
        # Collect all metrics
        self.success_metrics = {
            'content_migration': self.analyze_content_migration(),
            'asset_migration': self.analyze_asset_migration(),
            'navigation_structure': self.analyze_navigation_structure(),
            'theme_customization': self.analyze_theme_customization(),
            'build_readiness': self.analyze_build_readiness()
        }
        
        # Calculate overall success rate
        success_rate = self.calculate_overall_success_rate()
        
        # Create summary
        summary = {
            'migration_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall_success_rate': success_rate,
            'status': 'SUCCESS' if success_rate >= 80 else 'PARTIAL' if success_rate >= 60 else 'NEEDS_WORK',
            'metrics': self.success_metrics,
            'recommendations': self.generate_recommendations()
        }
        
        return summary
    
    def generate_recommendations(self) -> list:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        # Content recommendations
        content_metrics = self.success_metrics.get('content_migration', {})
        if content_metrics.get('languages_migrated', 0) < 3:
            recommendations.append("Complete migration for all three languages (zh, en, ja)")
        
        # Asset recommendations
        asset_metrics = self.success_metrics.get('asset_migration', {})
        if not asset_metrics.get('assets_directory_exists', False):
            recommendations.append("Create and populate assets directory")
        
        # Navigation recommendations
        nav_metrics = self.success_metrics.get('navigation_structure', {})
        if not nav_metrics.get('multi_language_nav', False):
            recommendations.append("Configure multi-language navigation in mkdocs.yml")
        
        # Theme recommendations
        theme_metrics = self.success_metrics.get('theme_customization', {})
        if not theme_metrics.get('custom_css_exists', False):
            recommendations.append("Add custom CSS for FlutterX branding")
        
        # Build recommendations
        build_metrics = self.success_metrics.get('build_readiness', {})
        if build_metrics.get('build_scripts', 0) < 3:
            recommendations.append("Complete build automation scripts")
        
        if not recommendations:
            recommendations.append("Migration is complete and ready for production!")
        
        return recommendations
    
    def save_report(self, report: dict):
        """Save the success report"""
        
        # Save JSON report
        json_file = self.project_dir / "migration-success-report.json"
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error saving JSON report: {e}", "WARNING")
        
        # Save text report
        text_file = self.project_dir / "migration-success-report.txt"
        try:
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write("FlutterX Documentation Migration Success Report\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Migration Date: {report['migration_date']}\n")
                f.write(f"Overall Success Rate: {report['overall_success_rate']:.1f}%\n")
                f.write(f"Status: {report['status']}\n\n")
                
                # Content migration
                content = report['metrics']['content_migration']
                f.write("Content Migration:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Languages migrated: {content['languages_migrated']}/3\n")
                f.write(f"Total markdown files: {content['total_markdown_files']}\n")
                f.write(f"Files per language: {content['files_per_language']}\n\n")
                
                # Asset migration
                assets = report['metrics']['asset_migration']
                f.write("Asset Migration:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Assets directory: {'✅' if assets['assets_directory_exists'] else '❌'}\n")
                f.write(f"Total images: {assets['total_images']}\n")
                f.write(f"Image types: {assets['image_types']}\n")
                f.write(f"Total size: {assets['total_size_mb']:.2f} MB\n\n")
                
                # Navigation
                nav = report['metrics']['navigation_structure']
                f.write("Navigation Structure:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Config exists: {'✅' if nav['config_exists'] else '❌'}\n")
                f.write(f"Has navigation: {'✅' if nav['has_navigation'] else '❌'}\n")
                f.write(f"Multi-language nav: {'✅' if nav['multi_language_nav'] else '❌'}\n")
                f.write(f"Navigation items: {nav['navigation_items']}\n\n")
                
                # Theme
                theme = report['metrics']['theme_customization']
                f.write("Theme Customization:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Custom CSS: {'✅' if theme['custom_css_exists'] else '❌'}\n")
                f.write(f"Overrides directory: {'✅' if theme['overrides_directory'] else '❌'}\n")
                f.write(f"Theme configured: {'✅' if theme['theme_configured'] else '❌'}\n\n")
                
                # Build readiness
                build = report['metrics']['build_readiness']
                f.write("Build Readiness:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Requirements file: {'✅' if build['requirements_file'] else '❌'}\n")
                f.write(f"Build scripts: {build['build_scripts']}/4\n")
                f.write(f"Test scripts: {build['test_scripts']}\n")
                f.write(f"Site buildable: {'✅' if build['site_buildable'] else '❌'}\n\n")
                
                # Recommendations
                f.write("Recommendations:\n")
                f.write("-" * 20 + "\n")
                for i, rec in enumerate(report['recommendations'], 1):
                    f.write(f"{i}. {rec}\n")
                    
        except Exception as e:
            self.log(f"Error saving text report: {e}", "WARNING")
        
        self.log(f"Reports saved: {json_file.name}, {text_file.name}")
    
    def run_analysis(self) -> bool:
        """Run complete migration success analysis"""
        
        self.log("🎯 Starting migration success analysis...")
        
        try:
            report = self.generate_success_report()
            self.save_report(report)
            
            # Print summary
            self.log(f"\n📊 Migration Success Summary:")
            self.log(f"Overall Success Rate: {report['overall_success_rate']:.1f}%")
            self.log(f"Status: {report['status']}")
            
            if report['status'] == 'SUCCESS':
                self.log("🎉 Migration completed successfully!")
                self.log("✅ Ready for production deployment")
            elif report['status'] == 'PARTIAL':
                self.log("⚠️  Migration partially successful")
                self.log("Some improvements recommended before production")
            else:
                self.log("❌ Migration needs more work")
                self.log("Please address issues before deployment")
            
            return report['status'] in ['SUCCESS', 'PARTIAL']
            
        except Exception as e:
            self.log(f"Error during analysis: {e}", "ERROR")
            return False

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration success analysis")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    args = parser.parse_args()
    
    reporter = MigrationSuccessReporter(args.project_dir)
    success = reporter.run_analysis()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()