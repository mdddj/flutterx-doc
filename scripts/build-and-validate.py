#!/usr/bin/env python3
"""
One-click build and validation script for FlutterX documentation
"""

import subprocess
import sys
from pathlib import Path

class BuildAndValidator:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.log_messages = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages"""
        formatted_message = f"[{level}] {message}"
        print(formatted_message)
        self.log_messages.append(formatted_message)
    
    def run_script(self, script_name: str, args: list = None) -> bool:
        """Run a Python script and return success status"""
        
        script_path = self.project_dir / "scripts" / script_name
        if not script_path.exists():
            self.log(f"Script not found: {script_path}", "ERROR")
            return False
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, cwd=self.project_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log(f"✅ {script_name} completed successfully")
                return True
            else:
                self.log(f"❌ {script_name} failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error running {script_name}: {str(e)}", "ERROR")
            return False
    
    def run_complete_pipeline(self) -> bool:
        """Run the complete build and validation pipeline"""
        
        self.log("🚀 Starting complete build and validation pipeline...")
        
        pipeline_steps = [
            ("Content Migration", "migrate.py", []),
            ("Content Validation", "validate-content-comprehensive.py", []),
            ("Navigation Validation", "validate-navigation.py", []),
            ("Asset Validation", "validate-assets.py", []),
            ("Build Test", "test-build.py", []),
            ("Site Build", "build-site.py", []),
            ("Link Validation", "validate-links.py", ["--site-dir", "site"]),
            ("Deployment Preparation", "prepare-deployment.py", [])
        ]
        
        successful_steps = 0
        total_steps = len(pipeline_steps)
        
        for step_name, script_name, args in pipeline_steps:
            self.log(f"📋 Running: {step_name}")
            
            if self.run_script(script_name, args):
                successful_steps += 1
            else:
                self.log(f"❌ Pipeline failed at: {step_name}", "ERROR")
                break
        
        # Generate summary
        self.log(f"\n📊 Pipeline Summary:")
        self.log(f"   Completed steps: {successful_steps}/{total_steps}")
        
        if successful_steps == total_steps:
            self.log("🎉 Complete pipeline executed successfully!")
            self.log("📦 Your documentation is ready for deployment!")
            return True
        else:
            self.log(f"⚠️  Pipeline incomplete - {total_steps - successful_steps} steps failed")
            return False
    
    def run_quick_validation(self) -> bool:
        """Run quick validation without full build"""
        
        self.log("⚡ Starting quick validation...")
        
        validation_steps = [
            ("Content Validation", "validate-content-comprehensive.py", []),
            ("Navigation Validation", "validate-navigation.py", []),
            ("Asset Validation", "validate-assets.py", [])
        ]
        
        successful_steps = 0
        total_steps = len(validation_steps)
        
        for step_name, script_name, args in validation_steps:
            self.log(f"📋 Running: {step_name}")
            
            if self.run_script(script_name, args):
                successful_steps += 1
            else:
                self.log(f"❌ Validation failed at: {step_name}", "ERROR")
        
        # Generate summary
        self.log(f"\n📊 Validation Summary:")
        self.log(f"   Completed validations: {successful_steps}/{total_steps}")
        
        if successful_steps == total_steps:
            self.log("✅ All validations passed!")
            return True
        else:
            self.log(f"⚠️  {total_steps - successful_steps} validations failed")
            return False
    
    def run_build_only(self) -> bool:
        """Run build process only"""
        
        self.log("🔨 Starting build process...")
        
        build_steps = [
            ("Build Test", "test-build.py", []),
            ("Site Build", "build-site.py", [])
        ]
        
        successful_steps = 0
        total_steps = len(build_steps)
        
        for step_name, script_name, args in build_steps:
            self.log(f"📋 Running: {step_name}")
            
            if self.run_script(script_name, args):
                successful_steps += 1
            else:
                self.log(f"❌ Build failed at: {step_name}", "ERROR")
                break
        
        # Generate summary
        self.log(f"\n📊 Build Summary:")
        self.log(f"   Completed steps: {successful_steps}/{total_steps}")
        
        if successful_steps == total_steps:
            self.log("✅ Build completed successfully!")
            return True
        else:
            self.log(f"❌ Build failed")
            return False
    
    def generate_final_report(self):
        """Generate final execution report"""
        
        report_file = self.project_dir / "build-validation-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Build and Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Execution Log:\n")
            f.write("-" * 30 + "\n")
            
            for log_entry in self.log_messages:
                f.write(f"{log_entry}\n")
            
            f.write("\nGenerated Files:\n")
            f.write("-" * 30 + "\n")
            
            # List generated files
            generated_files = [
                "site/",
                "deploy/",
                "comprehensive-validation-report.txt",
                "validation-report.json",
                "navigation-validation-report.txt",
                "asset-validation-report.txt",
                "build-report.txt"
            ]
            
            for file_path in generated_files:
                full_path = self.project_dir / file_path
                if full_path.exists():
                    f.write(f"✅ {file_path}\n")
                else:
                    f.write(f"❌ {file_path} (not found)\n")
        
        self.log(f"📄 Final report saved to: {report_file}")

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Build and validate FlutterX documentation")
    parser.add_argument("--mode", choices=["full", "validate", "build"], default="full",
                       help="Execution mode: full pipeline, validation only, or build only")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    args = parser.parse_args()
    
    builder = BuildAndValidator(args.project_dir)
    
    if args.mode == "full":
        success = builder.run_complete_pipeline()
    elif args.mode == "validate":
        success = builder.run_quick_validation()
    elif args.mode == "build":
        success = builder.run_build_only()
    
    # Generate final report
    builder.generate_final_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()