#!/usr/bin/env python3
"""
Development server for FlutterX documentation
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path
import threading
import webbrowser

class DevServer:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.server_process = None
        self.port = 8000
        self.host = "127.0.0.1"
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        
        self.log("Checking dependencies...")
        
        try:
            # Check if mkdocs is installed
            result = subprocess.run(
                ["mkdocs", "--version"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                self.log("MkDocs not found. Please install: pip install -r requirements.txt", "ERROR")
                return False
            
            self.log(f"MkDocs version: {result.stdout.strip()}")
            
            # Check if mkdocs.yml exists
            config_file = self.project_dir / "mkdocs.yml"
            if not config_file.exists():
                self.log("mkdocs.yml not found in project directory", "ERROR")
                return False
            
            self.log("All dependencies satisfied")
            return True
            
        except FileNotFoundError:
            self.log("MkDocs not found. Please install: pip install -r requirements.txt", "ERROR")
            return False
    
    def find_available_port(self, start_port: int = 8000) -> int:
        """Find an available port starting from start_port"""
        
        import socket
        
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, port))
                    return port
            except OSError:
                continue
        
        return start_port  # Fallback to original port
    
    def start_server(self, auto_reload: bool = True, open_browser: bool = True) -> bool:
        """Start the development server"""
        
        if not self.check_dependencies():
            return False
        
        # Find available port
        self.port = self.find_available_port(self.port)
        
        self.log(f"Starting development server on {self.host}:{self.port}")
        
        # Build command
        cmd = [
            "mkdocs", "serve",
            "--dev-addr", f"{self.host}:{self.port}",
            "--config-file", "mkdocs.yml"
        ]
        
        if not auto_reload:
            cmd.append("--no-livereload")
        
        try:
            # Start server process
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait a moment for server to start
            time.sleep(2)
            
            # Check if server started successfully
            if self.server_process.poll() is not None:
                self.log("Failed to start development server", "ERROR")
                return False
            
            server_url = f"http://{self.host}:{self.port}"
            self.log(f"Development server started: {server_url}")
            self.log("Press Ctrl+C to stop the server")
            
            # Open browser if requested
            if open_browser:
                self.log("Opening browser...")
                threading.Timer(1.0, lambda: webbrowser.open(server_url)).start()
            
            # Monitor server output
            self.monitor_server_output()
            
            return True
            
        except Exception as e:
            self.log(f"Error starting server: {str(e)}", "ERROR")
            return False
    
    def monitor_server_output(self):
        """Monitor and display server output"""
        
        try:
            while self.server_process and self.server_process.poll() is None:
                output = self.server_process.stdout.readline()
                if output:
                    # Clean up the output and display
                    clean_output = output.strip()
                    if clean_output and not clean_output.startswith("INFO"):
                        print(clean_output)
                else:
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            self.stop_server()
        except Exception as e:
            self.log(f"Error monitoring server: {str(e)}", "ERROR")
    
    def stop_server(self):
        """Stop the development server"""
        
        if self.server_process:
            self.log("Stopping development server...")
            
            try:
                # Send SIGTERM to gracefully stop
                self.server_process.terminate()
                
                # Wait for process to terminate
                try:
                    self.server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't stop gracefully
                    self.log("Force stopping server...", "WARNING")
                    self.server_process.kill()
                    self.server_process.wait()
                
                self.log("Development server stopped")
                
            except Exception as e:
                self.log(f"Error stopping server: {str(e)}", "ERROR")
            
            finally:
                self.server_process = None
    
    def build_site(self, clean: bool = True) -> bool:
        """Build the static site"""
        
        self.log("Building static site...")
        
        if not self.check_dependencies():
            return False
        
        # Clean previous build if requested
        if clean:
            site_dir = self.project_dir / "site"
            if site_dir.exists():
                import shutil
                shutil.rmtree(site_dir)
                self.log("Cleaned previous build")
        
        try:
            # Build site
            result = subprocess.run(
                ["mkdocs", "build", "--config-file", "mkdocs.yml"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Site built successfully")
                
                # Show build statistics
                site_dir = self.project_dir / "site"
                if site_dir.exists():
                    file_count = len(list(site_dir.rglob("*")))
                    self.log(f"Generated {file_count} files in site/ directory")
                
                return True
            else:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Build error: {str(e)}", "ERROR")
            return False
    
    def watch_and_rebuild(self):
        """Watch for file changes and rebuild automatically"""
        
        try:
            import watchdog
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
        except ImportError:
            self.log("Watchdog not installed. Install with: pip install watchdog", "ERROR")
            return False
        
        class RebuildHandler(FileSystemEventHandler):
            def __init__(self, dev_server):
                self.dev_server = dev_server
                self.last_rebuild = 0
                
            def on_modified(self, event):
                if event.is_directory:
                    return
                
                # Only rebuild for markdown and config files
                if not event.src_path.endswith(('.md', '.yml', '.yaml', '.css', '.js')):
                    return
                
                # Throttle rebuilds
                current_time = time.time()
                if current_time - self.last_rebuild < 2:  # 2 second throttle
                    return
                
                self.last_rebuild = current_time
                self.dev_server.log(f"File changed: {event.src_path}")
                self.dev_server.build_site(clean=False)
        
        observer = Observer()
        event_handler = RebuildHandler(self)
        
        # Watch docs directory and config files
        observer.schedule(event_handler, str(self.project_dir / "docs"), recursive=True)
        observer.schedule(event_handler, str(self.project_dir), recursive=False)
        
        observer.start()
        self.log("File watcher started")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.log("File watcher stopped")
        
        observer.join()

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="FlutterX Documentation Development Server")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    parser.add_argument("--build-only", action="store_true", help="Build site and exit")
    parser.add_argument("--watch", action="store_true", help="Watch files and rebuild")
    
    args = parser.parse_args()
    
    server = DevServer(args.project_dir)
    server.port = args.port
    server.host = args.host
    
    # Handle different modes
    if args.build_only:
        success = server.build_site()
        sys.exit(0 if success else 1)
    elif args.watch:
        server.watch_and_rebuild()
    else:
        # Start development server
        try:
            success = server.start_server(
                auto_reload=not args.no_reload,
                open_browser=not args.no_browser
            )
            sys.exit(0 if success else 1)
        except KeyboardInterrupt:
            server.stop_server()
            sys.exit(0)

if __name__ == "__main__":
    main()