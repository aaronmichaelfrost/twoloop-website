#!/usr/bin/env python3
"""
Generate individual HTML files for each blog post with correct meta tags.
This creates static files that social media crawlers can read properly.
"""

import os
import re
import glob

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

def inject_meta_tags(html_content, title, description, image, url):
    """Inject specific meta tags into HTML content."""
    
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

def add_redirect_script(html_content, post_slug):
    """Add JavaScript to redirect to the correct blog post view."""
    redirect_script = f"""
    <script>
        // Auto-redirect to blog post view for social media crawlers
        if (window.location.search === '' && window.location.hash === '') {{
            // Only redirect if no query params - this means direct access
            window.location.href = '/?page=blog&post={post_slug}';
        }}
    </script>
    """
    
    # Insert before closing </body> tag
    html_content = html_content.replace('</body>', f'{redirect_script}</body>')
    return html_content

def generate_blog_pages():
    """Generate individual HTML files for each blog post."""
    base_url = "https://twoloop.net"
    
    # Read the original index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_html = f.read()
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return
    
    # Get all blog post markdown files
    blog_posts_dir = 'blog-posts'
    if not os.path.exists(blog_posts_dir):
        print(f"Blog posts directory '{blog_posts_dir}' not found!")
        return
    
    md_files = glob.glob(os.path.join(blog_posts_dir, '*.md'))
    
    for md_file in md_files:
        # Get post slug from filename
        post_slug = os.path.splitext(os.path.basename(md_file))[0]
        
        # Parse metadata
        metadata = parse_blog_post_metadata(md_file)
        
        if not metadata:
            print(f"No metadata found for {post_slug}, skipping...")
            continue
        
        # Prepare meta tag values
        title = f"{metadata.get('title', post_slug)} - twoloop"
        description = metadata.get('description', 'twoloop games blog post')
        
        # Handle cover image
        cover_image = metadata.get('cover-image', '')
        if cover_image:
            if cover_image.startswith('http') or cover_image.startswith('//'):
                image = cover_image
            else:
                image = f"{base_url}/blog-posts/{cover_image}"
        else:
            image = f"{base_url}/playtest.png"
        
        url = f"{base_url}/?page=blog&post={post_slug}"
        
        # Create HTML with correct meta tags
        blog_html = inject_meta_tags(original_html, title, description, image, url)
        
        # Add redirect script
        blog_html = add_redirect_script(blog_html, post_slug)
        
        # Write to file
        output_filename = f"{post_slug}.html"
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(blog_html)
            print(f"Generated {output_filename}")
        except Exception as e:
            print(f"Error writing {output_filename}: {e}")

if __name__ == "__main__":
    generate_blog_pages()
    print("Done! Upload the generated HTML files to your web server.")
    print("Social media links should use URLs like: https://twoloop.net/devblog-1.html")
