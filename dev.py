#!/usr/bin/env python3
"""
FlutterX Documentation Development Manager
"""

import subprocess
import sys
import os
import json
from pathlib import Path
import argparse

class DevManager:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.scripts_dir = self.project_dir / "scripts"
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load development configuration"""
        
        config_file = self.project_dir / "dev-config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Error loading config: {e}")
        
        # Default configuration
        return {
            "development": {
                "server": {"host": "127.0.0.1", "port": 8000},
                "build": {"strict_mode": False}
            }
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages"""
        print(f"[{level}] {message}")
    
    def run_script(self, script_name: str, args: list = None) -> bool:
        """Run a development script"""
        
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            self.log(f"Script not found: {script_name}", "ERROR")
            return False
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, cwd=self.project_dir)
            return result.returncode == 0
        except Exception as e:
            self.log(f"Error running script: {e}", "ERROR")
            return False
    
    def serve(self, args) -> bool:
        """Start development server"""
        
        self.log("Starting development server...")
        
        server_args = []
        
        if args.port:
            server_args.extend(["--port", str(args.port)])
        elif "port" in self.config.get("development", {}).get("server", {}):
            server_args.extend(["--port", str(self.config["development"]["server"]["port"])])
        
        if args.host:
            server_args.extend(["--host", args.host])
        elif "host" in self.config.get("development", {}).get("server", {}):
            server_args.extend(["--host", self.config["development"]["server"]["host"]])
        
        if args.no_browser:
            server_args.append("--no-browser")
        
        if args.no_reload:
            server_args.append("--no-reload")
        
        return self.run_script("dev-server.py", server_args)
    
    def build(self, args) -> bool:
        """Build the site"""
        
        if args.production:
            self.log("Running production build...")
            build_args = []
            
            if args.no_minify:
                build_args.append("--no-minify")
            if args.no_gzip:
                build_args.append("--no-gzip")
            if args.no_hash:
                build_args.append("--no-hash")
            
            return self.run_script("production-build.py", build_args)
        else:
            self.log("Running development build...")
            build_args = []
            
            if args.no_tests:
                build_args.append("--no-tests")
            if args.no_optimize:
                build_args.append("--no-optimize")
            
            return self.run_script("build-automation.py", build_args)
    
    def test(self, args) -> bool:
        """Run tests"""
        
        self.log("Running tests...")
        
        if args.suite:
            # Run specific test suite
            test_file = f"test_{args.suite}.py"
            return self.run_script(f"../tests/{test_file}")
        elif args.quick:
            # Run quick tests
            return self.run_script("../tests/run_all_tests.py", ["--quick"])
        else:
            # Run all tests
            return self.run_script("../tests/run_all_tests.py")
    
    def migrate(self, args) -> bool:
        """Run migration"""
        
        self.log("Running migration...")
        
        migration_args = []
        
        if args.source:
            migration_args.extend(["--source", args.source])
        if args.target:
            migration_args.extend(["--target", args.target])
        if args.dry_run:
            migration_args.append("--dry-run")
        
        return self.run_script("run-migration.py", migration_args)
    
    def validate(self, args) -> bool:
        """Run validation"""
        
        self.log("Running validation...")
        
        if args.content:
            return self.run_script("validate-content-comprehensive.py")
        elif args.links:
            return self.run_script("validate-links.py")
        elif args.navigation:
            return self.run_script("validate-navigation.py")
        else:
            # Run comprehensive validation
            scripts = [
                "validate-content-comprehensive.py",
                "validate-navigation.py",
                "validate-assets.py"
            ]
            
            for script in scripts:
                if not self.run_script(script):
                    return False
            
            return True
    
    def clean(self, args) -> bool:
        """Clean build artifacts"""
        
        self.log("Cleaning build artifacts...")
        
        import shutil
        
        # Directories to clean
        clean_dirs = ["site"]
        
        if args.all:
            clean_dirs.extend(["__pycache__", ".pytest_cache"])
        
        for dir_name in clean_dirs:
            dir_path = self.project_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    self.log(f"Cleaned: {dir_name}")
                except Exception as e:
                    self.log(f"Error cleaning {dir_name}: {e}", "ERROR")
        
        # Files to clean
        clean_patterns = ["*.pyc", "*.log", "*-report.txt", "*-report.json"]
        
        if args.all:
            clean_patterns.extend(["*.tmp", "*.bak"])
        
        for pattern in clean_patterns:
            for file_path in self.project_dir.rglob(pattern):
                try:
                    file_path.unlink()
                    self.log(f"Cleaned: {file_path.name}")
                except Exception as e:
                    self.log(f"Error cleaning {file_path}: {e}", "ERROR")
        
        return True
    
    def status(self, args) -> bool:
        """Show project status"""
        
        self.log("FlutterX Documentation Project Status")
        print("=" * 50)
        
        # Check project structure
        required_files = ["mkdocs.yml", "requirements.txt", "docs/"]
        missing_files = []
        
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
        else:
            print("✅ Project structure complete")
        
        # Check dependencies
        try:
            result = subprocess.run(
                ["mkdocs", "--version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print(f"✅ MkDocs: {result.stdout.strip()}")
            else:
                print("❌ MkDocs not found")
        except FileNotFoundError:
            print("❌ MkDocs not installed")
        
        # Check site status
        site_dir = self.project_dir / "site"
        if site_dir.exists():
            file_count = len(list(site_dir.rglob("*")))
            print(f"✅ Site built: {file_count} files")
        else:
            print("⚠️  Site not built")
        
        # Check test reports
        test_reports = list(self.project_dir.glob("*-test-report.txt"))
        if test_reports:
            print(f"✅ Test reports: {len(test_reports)} available")
        else:
            print("⚠️  No test reports found")
        
        return True
    
    def help_command(self, args) -> bool:
        """Show help information"""
        
        print("FlutterX Documentation Development Commands")
        print("=" * 50)
        print()
        print("Available commands:")
        print("  serve     - Start development server")
        print("  build     - Build the site")
        print("  test      - Run tests")
        print("  migrate   - Run migration")
        print("  validate  - Run validation")
        print("  clean     - Clean build artifacts")
        print("  status    - Show project status")
        print("  help      - Show this help")
        print()
        print("Use 'python dev.py <command> --help' for command-specific help")
        
        return True

def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description="FlutterX Documentation Development Manager")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start development server")
    serve_parser.add_argument("--port", type=int, help="Server port")
    serve_parser.add_argument("--host", help="Server host")
    serve_parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    serve_parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build the site")
    build_parser.add_argument("--production", action="store_true", help="Production build")
    build_parser.add_argument("--no-tests", action="store_true", help="Skip tests")
    build_parser.add_argument("--no-optimize", action="store_true", help="Skip optimization")
    build_parser.add_argument("--no-minify", action="store_true", help="Skip minification")
    build_parser.add_argument("--no-gzip", action="store_true", help="Skip gzip compression")
    build_parser.add_argument("--no-hash", action="store_true", help="Skip file hashing")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--suite", help="Specific test suite to run")
    test_parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    # Migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Run migration")
    migrate_parser.add_argument("--source", help="Source directory")
    migrate_parser.add_argument("--target", help="Target directory")
    migrate_parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Run validation")
    validate_parser.add_argument("--content", action="store_true", help="Validate content only")
    validate_parser.add_argument("--links", action="store_true", help="Validate links only")
    validate_parser.add_argument("--navigation", action="store_true", help="Validate navigation only")
    
    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean build artifacts")
    clean_parser.add_argument("--all", action="store_true", help="Clean all artifacts")
    
    # Status command
    subparsers.add_parser("status", help="Show project status")
    
    # Help command
    subparsers.add_parser("help", help="Show help information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = DevManager(args.project_dir)
    
    # Route to appropriate command
    command_map = {
        "serve": manager.serve,
        "build": manager.build,
        "test": manager.test,
        "migrate": manager.migrate,
        "validate": manager.validate,
        "clean": manager.clean,
        "status": manager.status,
        "help": manager.help_command
    }
    
    if args.command in command_map:
        success = command_map[args.command](args)
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()