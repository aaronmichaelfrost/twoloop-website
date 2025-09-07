#!/usr/bin/env python3
"""
Simple HTTP server for testing the blog functionality locally.
Run this script and visit http://localhost:8000 to view the website.
"""

import http.server
import socketserver
import os
import sys

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

    def guess_type(self, path):
        # Ensure .md files are served with correct content type
        if path.endswith('.md'):
            return 'text/plain'
        return super().guess_type(path)
    
    def do_GET(self):
        # Handle SPA routing - serve index.html for routes that don't correspond to actual files
        path = self.path.split('?')[0]  # Remove query parameters
        
        # Routes that should serve index.html
        spa_routes = ['/blog', '/docs']
        
        # Check if it's a SPA route or a sub-route of a SPA route
        should_serve_index = False
        
        if path in spa_routes:
            should_serve_index = True
        else:
            # Check for sub-routes like /blog/post-name or /docs/doc-name
            for route in spa_routes:
                if path.startswith(route + '/'):
                    should_serve_index = True
                    break
        
        if should_serve_index:
            # Serve index.html instead
            self.path = '/index.html'
        
        # Let the parent class handle the request
        super().do_GET()

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
