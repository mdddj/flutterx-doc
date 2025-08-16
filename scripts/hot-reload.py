#!/usr/bin/env python3
"""
Hot reload development server for FlutterX documentation
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
import json

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

class HotReloadServer:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.server_process = None
        self.observer = None
        self.last_reload = 0
        self.reload_delay = 1.0  # Minimum delay between reloads
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load hot reload configuration"""
        
        default_config = {
            'watch_patterns': ['*.md', '*.yml', '*.yaml', '*.css', '*.js', '*.html'],
            'ignore_patterns': ['site/*', '*.pyc', '__pycache__/*', '.git/*'],
            'watch_directories': ['docs', 'overrides', '.'],
            'reload_delay': 1.0,
            'auto_open_browser': True,
            'server_port': 8000,
            'server_host': '127.0.0.1'
        }
        
        config_file = self.project_dir / 'hot-reload-config.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration"""
        
        config_file = self.project_dir / 'hot-reload-config.json'
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Error saving config: {e}")
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def should_reload_for_file(self, file_path: str) -> bool:
        """Check if file change should trigger reload"""
        
        file_path = file_path.replace('\\', '/')
        
        # Check ignore patterns
        for pattern in self.config['ignore_patterns']:
            if self.match_pattern(file_path, pattern):
                return False
        
        # Check watch patterns
        for pattern in self.config['watch_patterns']:
            if self.match_pattern(file_path, pattern):
                return True
        
        return False
    
    def match_pattern(self, file_path: str, pattern: str) -> bool:
        """Simple pattern matching"""
        
        import fnmatch
        
        # Handle directory patterns
        if pattern.endswith('/*'):
            dir_pattern = pattern[:-2]
            return file_path.startswith(dir_pattern + '/')
        
        # Handle file patterns
        return fnmatch.fnmatch(os.path.basename(file_path), pattern)
    
    def start_mkdocs_server(self) -> bool:
        """Start MkDocs development server"""
        
        self.log("Starting MkDocs development server...")
        
        cmd = [
            "mkdocs", "serve",
            "--dev-addr", f"{self.config['server_host']}:{self.config['server_port']}",
            "--config-file", "mkdocs.yml"
        ]
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment and check if server started
            time.sleep(2)
            
            if self.server_process.poll() is not None:
                stdout, stderr = self.server_process.communicate()
                self.log(f"Server failed to start: {stderr}", "ERROR")
                return False
            
            server_url = f"http://{self.config['server_host']}:{self.config['server_port']}"
            self.log(f"Server started: {server_url}")
            
            # Open browser if configured
            if self.config['auto_open_browser']:
                self.open_browser(server_url)
            
            return True
            
        except Exception as e:
            self.log(f"Error starting server: {e}", "ERROR")
            return False
    
    def open_browser(self, url: str):
        """Open browser to the server URL"""
        
        import webbrowser
        
        def delayed_open():
            time.sleep(1)
            try:
                webbrowser.open(url)
                self.log("Opened browser")
            except Exception as e:
                self.log(f"Could not open browser: {e}", "WARNING")
        
        threading.Thread(target=delayed_open, daemon=True).start()
    
    def stop_server(self):
        """Stop the MkDocs server"""
        
        if self.server_process:
            self.log("Stopping server...")
            
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            except Exception as e:
                self.log(f"Error stopping server: {e}", "ERROR")
            
            self.server_process = None
            self.log("Server stopped")

class ReloadEventHandler(FileSystemEventHandler):
    """File system event handler for hot reload"""
    
    def __init__(self, hot_reload_server):
        self.server = hot_reload_server
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        self.handle_file_change(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        self.handle_file_change(event.src_path)
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        
        self.handle_file_change(event.src_path)
    
    def handle_file_change(self, file_path: str):
        """Handle file change event"""
        
        if not self.server.should_reload_for_file(file_path):
            return
        
        # Throttle reloads
        current_time = time.time()
        if current_time - self.server.last_reload < self.server.config['reload_delay']:
            return
        
        self.server.last_reload = current_time
        
        # Get relative path for display
        try:
            rel_path = Path(file_path).relative_to(self.server.project_dir)
        except ValueError:
            rel_path = Path(file_path).name
        
        self.server.log(f"File changed: {rel_path}")
        self.server.log("Reloading...")

def start_hot_reload_server(project_dir: str = ".") -> bool:
    """Start hot reload development server"""
    
    if not WATCHDOG_AVAILABLE:
        print("Error: watchdog package not installed")
        print("Install with: pip install watchdog")
        return False
    
    server = HotReloadServer(project_dir)
    
    # Start MkDocs server
    if not server.start_mkdocs_server():
        return False
    
    # Set up file watcher
    observer = Observer()
    event_handler = ReloadEventHandler(server)
    
    # Watch configured directories
    for watch_dir in server.config['watch_directories']:
        dir_path = server.project_dir / watch_dir
        if dir_path.exists():
            observer.schedule(event_handler, str(dir_path), recursive=True)
            server.log(f"Watching: {dir_path}")
    
    observer.start()
    server.observer = observer
    
    server.log("Hot reload enabled - watching for file changes...")
    server.log("Press Ctrl+C to stop")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if server is still running
            if server.server_process and server.server_process.poll() is not None:
                server.log("Server process ended", "ERROR")
                break
                
    except KeyboardInterrupt:
        server.log("Shutting down...")
    finally:
        # Cleanup
        if observer:
            observer.stop()
            observer.join()
        
        server.stop_server()
    
    return True

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="FlutterX Hot Reload Development Server")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", help="Server host")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    parser.add_argument("--config", help="Configuration file")
    
    args = parser.parse_args()
    
    # Override config if arguments provided
    if args.port or args.host or args.no_browser:
        server = HotReloadServer(args.project_dir)
        
        if args.port:
            server.config['server_port'] = args.port
        if args.host:
            server.config['server_host'] = args.host
        if args.no_browser:
            server.config['auto_open_browser'] = False
        
        server.save_config()
    
    success = start_hot_reload_server(args.project_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()