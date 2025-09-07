# Blog URL Routing Implementation

## Overview
Each blog post now has its own unique URL that can be shared, bookmarked, and accessed directly. The system supports proper browser navigation (back/forward buttons) and social media sharing with correct meta tags.

## URL Structure

### Blog List
- **URL:** `https://twoloop.net/?page=blog`
- **Description:** Shows all blog posts in a list format
- **Meta Tags:** Generic blog meta tags for social sharing

### Individual Blog Posts
- **URL Pattern:** `https://twoloop.net/?page=blog&post={slug}`
- **Examples:**
  - `https://twoloop.net/?page=blog&post=devblog-1`
  - `https://twoloop.net/?page=blog&post=devblog-2`
- **Description:** Shows a specific blog post with its full content
- **Meta Tags:** Post-specific meta tags including title and description

### Other Pages
- **About:** `https://twoloop.net/` or `https://twoloop.net/?page=about`
- **Docs:** `https://twoloop.net/?page=docs`

## Implementation Details

### Files Modified
1. **`index.html`** - Updated routing logic and meta tag handling
2. **`blog.js`** - Added URL updates to blog navigation functions

### Key Functions

#### `showBlogPost(slug)`
- Displays a specific blog post
- Updates URL to include post parameter
- Updates meta tags for social sharing
- Handles background image updates

#### `showBlogList()`
- Displays the blog post list
- Updates URL to remove post parameter
- Resets to blog list meta tags
- Handles background image updates

#### `handleRouting()`
- Parses current URL parameters
- Routes to appropriate page/post
- Handles direct URL access
- Manages browser back/forward navigation

#### `updateMetaTags(page, doc, post)`
- Updates Open Graph and Twitter meta tags
- Sets post-specific titles and descriptions
- Maintains consistent social sharing images

### URL Parameter Parsing
The system uses query parameters for routing:
- `?page=blog` - Shows blog list
- `?page=blog&post=devblog-1` - Shows specific post
- `?page=docs` - Shows documentation
- No parameters or `?page=about` - Shows about page

## Features

### ✅ Implemented
- [x] Individual URLs for each blog post
- [x] Direct URL access to specific posts
- [x] Browser back/forward button support
- [x] URL updates when navigating between posts
- [x] Proper meta tags for social sharing
- [x] **Custom preview images for each blog post**
- [x] **Cover image support for social media sharing**
- [x] Fallback handling for missing posts
- [x] Scroll position reset on navigation

### 🔄 Automatic Behaviors
- URLs update automatically when clicking blog posts
- Meta tags update automatically for social sharing
- Browser history is maintained for back/forward navigation
- Error handling for non-existent posts (falls back to blog list)

## Testing URLs

You can test these URLs directly in your browser:

1. **Blog List:** http://localhost:8000/?page=blog
2. **Devblog 1:** http://localhost:8000/?page=blog&post=devblog-1
3. **Devblog 2:** http://localhost:8000/?page=blog&post=devblog-2

## Social Sharing

Each blog post now has proper meta tags for social media platforms, with **custom preview images**:

### Preview Images
- **Individual blog posts:** Use their cover image from the frontmatter (e.g., `devblog1-images/cover.png`)
- **Blog list page:** Uses default `playtest.png`
- **All other pages:** Use default `playtest.png`

### Example Meta Tags

**For Devblog 1 (`?page=blog&post=devblog-1`):**
```html
<meta property="og:title" content="Devblog 1 - twoloop">
<meta property="og:description" content="Covers first two weeks of work on Fractium after a long break.">
<meta property="og:url" content="https://twoloop.net/?page=blog&post=devblog-1">
<meta property="og:image" content="https://twoloop.net/blog-posts/devblog1-images/cover.png">
```

**For Blog List (`?page=blog`):**
```html
<meta property="og:title" content="Blog - twoloop">
<meta property="og:description" content="twoloop games development blog">
<meta property="og:url" content="https://twoloop.net/?page=blog">
<meta property="og:image" content="https://twoloop.net/playtest.png">
```

### Testing Social Sharing
1. **Discord:** Paste blog post URLs to see cover image previews
2. **iMessage:** URLs will show the appropriate cover image
3. **Facebook:** Use [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
4. **Twitter:** Use [Twitter Card Validator](https://cards-dev.twitter.com/validator)

## Browser Support

The implementation uses standard web technologies and should work in all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Future Enhancements

Potential improvements for the future:
- SEO-friendly URLs (e.g., `/blog/devblog-1` instead of `?page=blog&post=devblog-1`)
- Breadcrumb navigation
- Previous/Next post navigation
- Blog post categories/tags
- Search functionality

## Maintenance

To add new blog posts:
1. Create a new `.md` file in the `blog-posts/` directory
2. Follow the existing frontmatter format with `title`, `description`, `date`, etc.
3. The post will automatically get a URL based on its filename (without `.md` extension)

Example: `new-post.md` becomes accessible at `?page=blog&post=new-post`
