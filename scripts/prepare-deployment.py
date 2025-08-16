#!/usr/bin/env python3
"""
Prepare documentation for deployment
"""

import os
import shutil
import gzip
import json
from pathlib import Path
from typing import List, Dict

class DeploymentPreparator:
    def __init__(self, site_dir: str, output_dir: str = "deploy"):
        self.site_dir = Path(site_dir)
        self.output_dir = Path(output_dir)
        self.preparation_log = []
        self.stats = {
            'total_files': 0,
            'compressed_files': 0,
            'total_size': 0,
            'compressed_size': 0
        }
        
    def log(self, message: str):
        """Log preparation messages"""
        print(message)
        self.preparation_log.append(message)
    
    def prepare_deployment_directory(self):
        """Prepare deployment directory"""
        
        self.log("Preparing deployment directory...")
        
        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        
        self.output_dir.mkdir(parents=True)
        
        # Copy site files
        if self.site_dir.exists():
            shutil.copytree(self.site_dir, self.output_dir / "site")
            self.log(f"✅ Copied site files to {self.output_dir / 'site'}")
        else:
            self.log(f"❌ Site directory not found: {self.site_dir}")
            return False
        
        return True
    
    def optimize_files(self):
        """Optimize files for deployment"""
        
        self.log("Optimizing files for deployment...")
        
        site_deploy_dir = self.output_dir / "site"
        
        for file_path in site_deploy_dir.rglob("*"):
            if file_path.is_file():
                self.stats['total_files'] += 1
                file_size = file_path.stat().st_size
                self.stats['total_size'] += file_size
                
                # Compress text files
                if self._should_compress(file_path):
                    compressed_size = self._compress_file(file_path)
                    if compressed_size:
                        self.stats['compressed_files'] += 1
                        self.stats['compressed_size'] += compressed_size
    
    def _should_compress(self, file_path: Path) -> bool:
        """Check if file should be compressed"""
        
        compressible_extensions = {
            '.html', '.css', '.js', '.json', '.xml', '.txt', '.svg'
        }
        
        return (file_path.suffix.lower() in compressible_extensions and 
                file_path.stat().st_size > 1024)  # Only compress files > 1KB
    
    def _compress_file(self, file_path: Path) -> int:
        """Compress file with gzip"""
        
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            compressed_size = Path(f"{file_path}.gz").stat().st_size
            return compressed_size
            
        except Exception as e:
            self.log(f"Error compressing {file_path}: {e}")
            return 0
    
    def create_deployment_config(self):
        """Create deployment configuration files"""
        
        self.log("Creating deployment configuration...")
        
        # Create .htaccess for Apache
        htaccess_content = """# FlutterX Documentation - Apache Configuration
RewriteEngine On

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Set cache headers
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
    ExpiresByType image/svg+xml "access plus 1 month"
    ExpiresByType text/html "access plus 1 day"
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Redirect to HTTPS (uncomment if using HTTPS)
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
"""
        
        htaccess_file = self.output_dir / "site" / ".htaccess"
        with open(htaccess_file, 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
        
        self.log("✅ Created .htaccess file")
        
        # Create nginx.conf for Nginx
        nginx_content = """# FlutterX Documentation - Nginx Configuration
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/your/site;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Set cache headers
    location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }

    location ~* \\.(html)$ {
        expires 1d;
        add_header Cache-Control "public";
    }

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Try files
    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    # Redirect to HTTPS (uncomment if using HTTPS)
    # return 301 https://$server_name$request_uri;
}
"""
        
        nginx_file = self.output_dir / "nginx.conf"
        with open(nginx_file, 'w', encoding='utf-8') as f:
            f.write(nginx_content)
        
        self.log("✅ Created nginx.conf file")
    
    def create_docker_config(self):
        """Create Docker configuration for deployment"""
        
        self.log("Creating Docker configuration...")
        
        # Create Dockerfile
        dockerfile_content = """# FlutterX Documentation - Docker Configuration
FROM nginx:alpine

# Copy site files
COPY site/ /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost/ || exit 1

# Labels
LABEL maintainer="FlutterX Team"
LABEL description="FlutterX Plugin Documentation"
LABEL version="1.0"
"""
        
        dockerfile = self.output_dir / "Dockerfile"
        with open(dockerfile, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        self.log("✅ Created Dockerfile")
        
        # Create docker-compose.yml
        compose_content = """version: '3.8'

services:
  flutterx-docs:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
    environment:
      - NGINX_HOST=localhost
      - NGINX_PORT=80
    volumes:
      - ./logs:/var/log/nginx
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.flutterx-docs.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.flutterx-docs.entrypoints=web"
"""
        
        compose_file = self.output_dir / "docker-compose.yml"
        with open(compose_file, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        
        self.log("✅ Created docker-compose.yml")
    
    def create_deployment_scripts(self):
        """Create deployment scripts"""
        
        self.log("Creating deployment scripts...")
        
        # Create deploy.sh script
        deploy_script = """#!/bin/bash
# FlutterX Documentation Deployment Script

set -e

echo "Starting FlutterX Documentation deployment..."

# Configuration
SITE_DIR="site"
BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"
DEPLOY_TARGET="/var/www/html"  # Change this to your deployment target

# Create backup
if [ -d "$DEPLOY_TARGET" ]; then
    echo "Creating backup..."
    cp -r "$DEPLOY_TARGET" "$BACKUP_DIR"
    echo "Backup created: $BACKUP_DIR"
fi

# Deploy new version
echo "Deploying new version..."
rsync -av --delete "$SITE_DIR/" "$DEPLOY_TARGET/"

# Set permissions
echo "Setting permissions..."
find "$DEPLOY_TARGET" -type f -exec chmod 644 {} \\;
find "$DEPLOY_TARGET" -type d -exec chmod 755 {} \\;

# Restart web server (uncomment as needed)
# systemctl reload nginx
# systemctl reload apache2

echo "Deployment completed successfully!"
echo "Site deployed to: $DEPLOY_TARGET"
"""
        
        deploy_file = self.output_dir / "deploy.sh"
        with open(deploy_file, 'w', encoding='utf-8') as f:
            f.write(deploy_script)
        
        # Make executable
        deploy_file.chmod(0o755)
        
        self.log("✅ Created deploy.sh script")
        
        # Create rollback script
        rollback_script = """#!/bin/bash
# FlutterX Documentation Rollback Script

set -e

echo "Starting rollback..."

# Configuration
DEPLOY_TARGET="/var/www/html"  # Change this to your deployment target

# Find latest backup
LATEST_BACKUP=$(ls -1d backup-* 2>/dev/null | tail -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No backup found!"
    exit 1
fi

echo "Rolling back to: $LATEST_BACKUP"

# Restore backup
rsync -av --delete "$LATEST_BACKUP/" "$DEPLOY_TARGET/"

# Restart web server (uncomment as needed)
# systemctl reload nginx
# systemctl reload apache2

echo "Rollback completed successfully!"
"""
        
        rollback_file = self.output_dir / "rollback.sh"
        with open(rollback_file, 'w', encoding='utf-8') as f:
            f.write(rollback_script)
        
        # Make executable
        rollback_file.chmod(0o755)
        
        self.log("✅ Created rollback.sh script")
    
    def create_readme(self):
        """Create deployment README"""
        
        self.log("Creating deployment README...")
        
        readme_content = """# FlutterX Documentation Deployment

This directory contains the prepared FlutterX documentation for deployment.

## Contents

- `site/` - Built documentation files
- `nginx.conf` - Nginx configuration
- `.htaccess` - Apache configuration (in site directory)
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `deploy.sh` - Deployment script
- `rollback.sh` - Rollback script

## Deployment Options

### Option 1: Static File Server

Simply copy the contents of the `site/` directory to your web server's document root.

### Option 2: Docker Deployment

```bash
docker-compose up -d
```

### Option 3: Manual Deployment

```bash
./deploy.sh
```

### Option 4: Nginx

1. Copy `site/` contents to your web root
2. Use the provided `nginx.conf` as a reference for your server configuration

### Option 5: Apache

The `site/` directory includes a `.htaccess` file with optimized settings.

## Configuration

Before deployment, update the following:

1. Domain names in configuration files
2. SSL/HTTPS settings if applicable
3. File paths in deployment scripts
4. Server-specific optimizations

## Monitoring

After deployment, monitor:

- Site accessibility
- Load times
- Search functionality
- Multi-language switching
- Mobile responsiveness

## Rollback

If issues occur, use the rollback script:

```bash
./rollback.sh
```

## Support

For issues with the FlutterX plugin documentation, visit:
https://github.com/mdddj/dd_flutter_idea_plugin
"""
        
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.log("✅ Created deployment README")
    
    def generate_deployment_report(self):
        """Generate deployment preparation report"""
        
        report_file = self.output_dir / "deployment-report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Deployment Preparation Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Statistics
            f.write("Statistics:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total files: {self.stats['total_files']}\n")
            f.write(f"Compressed files: {self.stats['compressed_files']}\n")
            f.write(f"Total size: {self.stats['total_size'] / 1024 / 1024:.2f} MB\n")
            f.write(f"Compressed size: {self.stats['compressed_size'] / 1024 / 1024:.2f} MB\n")
            
            if self.stats['total_size'] > 0:
                compression_ratio = (1 - self.stats['compressed_size'] / self.stats['total_size']) * 100
                f.write(f"Compression ratio: {compression_ratio:.1f}%\n")
            
            f.write("\nPreparation Log:\n")
            f.write("-" * 20 + "\n")
            
            for log_entry in self.preparation_log:
                f.write(f"{log_entry}\n")
        
        self.log(f"Deployment report saved to: {report_file}")
    
    def run_preparation(self) -> bool:
        """Run complete deployment preparation"""
        
        self.log("Starting deployment preparation...")
        
        try:
            # Prepare deployment
            if not self.prepare_deployment_directory():
                return False
            
            self.optimize_files()
            self.create_deployment_config()
            self.create_docker_config()
            self.create_deployment_scripts()
            self.create_readme()
            
            # Generate report
            self.generate_deployment_report()
            
            self.log("✅ Deployment preparation completed!")
            self.log(f"📦 Deployment package ready in: {self.output_dir}")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Deployment preparation failed: {str(e)}")
            return False

def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare documentation for deployment")
    parser.add_argument("--site-dir", default="site", help="Built site directory")
    parser.add_argument("--output-dir", default="deploy", help="Output directory for deployment package")
    
    args = parser.parse_args()
    
    preparator = DeploymentPreparator(args.site_dir, args.output_dir)
    success = preparator.run_preparation()
    
    import sys
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()