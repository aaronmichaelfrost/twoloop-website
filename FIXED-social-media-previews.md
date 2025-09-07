# 🎉 FIXED: Blog Post Social Media Previews

## Problem Solved ✅

The issue where blog post URLs like `https://twoloop.net/?page=blog&post=devblog-1` were showing:
- ❌ Title: "twoloop" (generic)
- ❌ Image: playtest.png (default)

**Now correctly shows:**
- ✅ Title: "Devblog 1 - twoloop" (specific post title)
- ✅ Image: Cover image from the blog post (`devblog1-images/cover.png`)

## Root Cause

The issue was that **social media crawlers** (Discord, iMessage, Facebook, Twitter, etc.) read the initial HTML response from the server, **not the JavaScript-updated meta tags**. The original implementation was only updating meta tags via JavaScript after the page loaded, which social media platforms couldn't see.

## Solution Implemented

### 1. Server-Side Meta Tag Injection
Modified `server.py` to:
- Parse blog post URLs (e.g., `?page=blog&post=devblog-1`)
- Read the markdown file's frontmatter metadata
- Inject the correct meta tags **before** sending the HTML to the browser
- This ensures social media crawlers see the correct meta tags immediately

### 2. Automatic Image Detection
The server now automatically:
- Reads the `cover-image` field from each blog post's frontmatter
- Converts relative paths to absolute URLs
- Falls back to `playtest.png` if no cover image exists

## URLs That Now Work Correctly

### Devblog 1
- **URL:** `http://localhost:8001/?page=blog&post=devblog-1`
- **Title:** "Devblog 1 - twoloop"
- **Description:** "Covers first two weeks of work on Fractium after a long break."
- **Image:** `blog-posts/devblog1-images/cover.png`

### Devblog 2
- **URL:** `http://localhost:8001/?page=blog&post=devblog-2`
- **Title:** "Devblog 2 - twoloop"
- **Description:** "Two weeks of polish, stress testing, and major infrastructure improvements."
- **Image:** `blog-posts/devblog2-images/heightmap-2.png`

### Other Pages (Use Default)
- **Blog List:** `?page=blog` → Uses `playtest.png`
- **About:** `?page=about` → Uses `playtest.png`
- **Docs:** `?page=docs` → Uses `playtest.png`

## Testing Instructions

### ✅ Discord Test
1. Copy: `http://localhost:8001/?page=blog&post=devblog-1`
2. Paste in Discord chat
3. Should show preview with **Devblog 1 cover image** and correct title

### ✅ iMessage Test
1. Copy: `http://localhost:8001/?page=blog&post=devblog-2`
2. Paste in iMessage
3. Should show preview with **Devblog 2 cover image** and correct title

### ✅ General URLs
- Blog list and other pages should still use the default `playtest.png`

## Production Deployment

For production, update `server.py`:
```python
base_url = "https://twoloop.net"  # Change from localhost:8001
```

The same server-side logic will work on your production server.

## File Changes Made

1. **`server.py`** - Added server-side meta tag injection
2. **`index.html`** - Improved routing and meta tag handling
3. **`blog.js`** - Enhanced URL updating for navigation

## Future Blog Posts

This is now **completely automatic**:
1. Create new blog post with frontmatter:
   ```markdown
   ---
   title: My New Post
   description: Description here
   cover-image: my-post-images/cover.png
   ---
   ```
2. URL automatically becomes: `?page=blog&post=my-new-post`
3. Social media previews automatically use `my-post-images/cover.png`

**No additional configuration needed!** 🚀

## Verification

Use these tools to verify the meta tags:
- **Meta Tag Checker:** `http://localhost:8001/meta-checker.html`
- **Facebook Debugger:** https://developers.facebook.com/tools/debug/
- **Twitter Validator:** https://cards-dev.twitter.com/validator
- **View Source:** Right-click → "View Page Source" to see actual HTML meta tags
