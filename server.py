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

# Set the port
PORT = 8000

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
