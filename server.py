#!/usr/bin/env python3
"""
Simple HTTP server for testing the blog functionality locally.
Run this script and visit http://localhost:8000 to view the website.
"""

import http.server
import socketserver
import os
import sys
import json
import glob
import re
from urllib.parse import urlparse, parse_qs

# Set the port
PORT = 8001

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def parse_blog_post_metadata(filepath):
    """Parse frontmatter metadata from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            return {}
        
        frontmatter = frontmatter_match.group(1)
        metadata = {}
        
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        return metadata
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return {}

def inject_meta_tags(html_content, page, post_slug=None):
    """Inject appropriate meta tags into HTML content."""
    # Detect if we're running locally or in production
    import socket
    hostname = socket.gethostname()
    is_local = hostname.lower() in ['localhost', '127.0.0.1'] or 'local' in hostname.lower()
    
    if is_local or PORT == 8001:
        base_url = f"http://localhost:{PORT}"
    else:
        base_url = "https://twoloop.net"
    
    # Default values
    title = "twoloop"
    description = "twoloop games - Fractium development"
    image = f"{base_url}/playtest.png"
    url = base_url
    
    if page == 'blog' and post_slug:
        # Try to load blog post metadata
        blog_post_path = f"blog-posts/{post_slug}.md"
        if os.path.exists(blog_post_path):
            metadata = parse_blog_post_metadata(blog_post_path)
            
            if metadata:
                title = f"{metadata.get('title', post_slug)} - twoloop"
                description = metadata.get('description', 'twoloop games blog post')
                
                # Use cover image if available
                cover_image = metadata.get('cover-image', '')
                if cover_image:
                    if not (cover_image.startswith('http') or cover_image.startswith('//')):
                        image = f"{base_url}/blog-posts/{cover_image}"
                    else:
                        image = cover_image
                
                url = f"{base_url}/?page=blog&post={post_slug}"
    elif page == 'blog':
        title = "Blog - twoloop"
        description = "twoloop games development blog"
        url = f"{base_url}/?page=blog"
    elif page == 'docs':
        title = "Documentation - twoloop"
        description = "twoloop games documentation and guides"
        url = f"{base_url}/?page=docs"
    
    # Replace meta tags
    replacements = {
        r'<meta property="og:title" content="[^"]*">': f'<meta property="og:title" content="{title}">',
        r'<meta property="og:description" content="[^"]*">': f'<meta property="og:description" content="{description}">',
        r'<meta property="og:image" content="[^"]*">': f'<meta property="og:image" content="{image}">',
        r'<meta property="og:image:secure_url" content="[^"]*">': f'<meta property="og:image:secure_url" content="{image}">',
        r'<meta property="og:url" content="[^"]*">': f'<meta property="og:url" content="{url}">',
        r'<meta name="twitter:title" content="[^"]*">': f'<meta name="twitter:title" content="{title}">',
        r'<meta name="twitter:description" content="[^"]*">': f'<meta name="twitter:description" content="{description}">',
        r'<meta name="twitter:image" content="[^"]*">': f'<meta name="twitter:image" content="{image}">',
        r'<meta name="description" content="[^"]*">': f'<meta name="description" content="{description}">',
        r'<title>[^<]*</title>': f'<title>{title}</title>'
    }
    
    for pattern, replacement in replacements.items():
        html_content = re.sub(pattern, replacement, html_content)
    
    return html_content

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Handle API endpoint for listing blog posts
        if self.path == '/api/blog-posts':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get all .md files from blog-posts directory
            blog_posts = []
            blog_posts_dir = 'blog-posts'
            if os.path.exists(blog_posts_dir):
                md_files = glob.glob(os.path.join(blog_posts_dir, '*.md'))
                blog_posts = [os.path.basename(f) for f in md_files]
                blog_posts.sort()  # Sort alphabetically for consistent ordering
            
            self.wfile.write(json.dumps(blog_posts).encode())
            return
        
        # Handle index.html requests with meta tag injection
        if self.path == '/' or self.path.startswith('/?'):
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            page = query_params.get('page', ['about'])[0]
            post_slug = query_params.get('post', [None])[0]
            
            # Read the original index.html
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Inject appropriate meta tags
                html_content = inject_meta_tags(html_content, page, post_slug)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
                return
                
            except Exception as e:
                print(f"Error serving index.html: {e}")
                # Fall back to default behavior
        
        # Default behavior for all other requests
        super().do_GET()

    def guess_type(self, path):
        # Ensure .md files are served with correct content type
        if path.endswith('.md'):
            return 'text/plain'
        return super().guess_type(path)

def main():
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"Server running at http://localhost:{PORT}/")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {PORT} is already in use. Try a different port or stop the existing server.")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    main()
