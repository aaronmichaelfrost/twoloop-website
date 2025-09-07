# Static Blog Page Solution

Since you can't deploy the Python server to production, this solution creates individual HTML files for each blog post with the correct meta tags already embedded.

## How It Works

1. **Generated Files**: The script `generate-blog-pages.py` creates individual HTML files for each blog post:
   - `devblog-1.html` - Contains meta tags for Devblog 1
   - `devblog-2.html` - Contains meta tags for Devblog 2

2. **Correct Meta Tags**: Each file has the proper Open Graph and Twitter Card meta tags:
   - Title: "[Blog Post Title] - twoloop"
   - Description: From the blog post's frontmatter
   - Image: The cover image from the blog post
   - URL: The canonical blog post URL

3. **Auto-Redirect**: Each file includes JavaScript that redirects visitors to the proper blog view (`/?page=blog&post=slug`)

## Usage

### For Social Media Sharing:
Instead of sharing: `https://twoloop.net/?page=blog&post=devblog-2`
Share this: `https://twoloop.net/devblog-2.html`

### Upload Process:
1. Run `python generate-blog-pages.py` to create the HTML files
2. Upload the generated `.html` files to your web server root directory
3. Social media crawlers will now see the correct meta tags

### When You Add New Blog Posts:
1. Add the new `.md` file to `blog-posts/` directory
2. Run `python generate-blog-pages.py` again
3. Upload the new `.html` file to your server

## File Structure After Upload:
```
twoloop.net/
├── index.html          (main website)
├── devblog-1.html      (blog post 1 with correct meta tags)
├── devblog-2.html      (blog post 2 with correct meta tags)
├── blog-posts/         (markdown files and images)
└── ... (other files)
```

## Testing:
- Direct access to `https://twoloop.net/devblog-2.html` will redirect to `/?page=blog&post=devblog-2`
- Social media crawlers will read the static meta tags before any JavaScript runs
- The correct cover image and title will appear in Discord, Twitter, etc.

## Benefits:
- ✅ No server-side code required
- ✅ Social media crawlers see correct meta tags immediately
- ✅ Users still get redirected to the proper blog interface
- ✅ Works with any static hosting provider
- ✅ Easy to maintain and update
