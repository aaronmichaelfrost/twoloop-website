#!/usr/bin/env python3
"""
Social Media Sharing Verification Script
This script helps verify that your website's social media meta tags are properly configured.
"""

import requests
from urllib.parse import urljoin
import re
import sys

def check_meta_tags(url):
    """Check if the website has proper social media meta tags."""
    try:
        print(f"🔍 Checking meta tags for: {url}")
        
        # Set a proper User-Agent to mimic social media crawlers
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; facebookexternalhit/1.1; +http://www.facebook.com/externalhit_uatext.php)'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html = response.text
        
        # Check for Open Graph tags
        og_tags = {
            'og:title': re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html),
            'og:description': re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html),
            'og:image': re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', html),
            'og:url': re.search(r'<meta\s+property="og:url"\s+content="([^"]*)"', html),
            'og:type': re.search(r'<meta\s+property="og:type"\s+content="([^"]*)"', html),
        }
        
        # Check for Twitter Card tags
        twitter_tags = {
            'twitter:card': re.search(r'<meta\s+name="twitter:card"\s+content="([^"]*)"', html),
            'twitter:title': re.search(r'<meta\s+name="twitter:title"\s+content="([^"]*)"', html),
            'twitter:description': re.search(r'<meta\s+name="twitter:description"\s+content="([^"]*)"', html),
            'twitter:image': re.search(r'<meta\s+name="twitter:image"\s+content="([^"]*)"', html),
        }
        
        print("\n📱 Open Graph Tags:")
        for tag, match in og_tags.items():
            if match:
                content = match.group(1)
                print(f"  ✅ {tag}: {content}")
                
                # Special check for image URL
                if tag == 'og:image':
                    if content.startswith('http'):
                        print(f"    🔗 Image URL is absolute: ✅")
                        # Try to check if image is accessible
                        try:
                            img_response = requests.head(content, timeout=5)
                            if img_response.status_code == 200:
                                print(f"    📸 Image is accessible: ✅")
                            else:
                                print(f"    ❌ Image returned status {img_response.status_code}")
                        except Exception as e:
                            print(f"    ⚠️  Could not verify image accessibility: {e}")
                    else:
                        print(f"    ❌ Image URL should be absolute (starts with http/https)")
            else:
                print(f"  ❌ {tag}: Not found")
        
        print("\n🐦 Twitter Card Tags:")
        for tag, match in twitter_tags.items():
            if match:
                content = match.group(1)
                print(f"  ✅ {tag}: {content}")
            else:
                print(f"  ❌ {tag}: Not found")
        
        # Check if playtest.png is being used
        og_image = og_tags.get('og:image')
        twitter_image = twitter_tags.get('twitter:image')
        
        print(f"\n🖼️  Image Verification:")
        if og_image and 'playtest.png' in og_image.group(1):
            print(f"  ✅ Using playtest.png for Open Graph")
        else:
            print(f"  ❌ Not using playtest.png for Open Graph")
            
        if twitter_image and 'playtest.png' in twitter_image.group(1):
            print(f"  ✅ Using playtest.png for Twitter")
        else:
            print(f"  ❌ Not using playtest.png for Twitter")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Error fetching URL: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    # Default URL - update this to match your actual domain
    default_url = "https://twoloop.games/"
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(f"Enter URL to check (default: {default_url}): ").strip()
        if not url:
            url = default_url
    
    print(f"🚀 Social Media Meta Tags Verification")
    print(f"=" * 50)
    
    success = check_meta_tags(url)
    
    if success:
        print(f"\n✅ Verification completed!")
        print(f"\n🔧 Next steps:")
        print(f"  1. Test your URLs in social media debuggers:")
        print(f"     • Facebook: https://developers.facebook.com/tools/debug/")
        print(f"     • Twitter: https://cards-dev.twitter.com/validator")
        print(f"     • LinkedIn: https://www.linkedin.com/post-inspector/")
        print(f"  2. Try sharing your URL in Discord or other messaging apps")
        print(f"  3. Note: Social platforms cache previews, so changes may take time to appear")
    else:
        print(f"\n❌ Verification failed. Please check your website configuration.")

if __name__ == "__main__":
    main()
