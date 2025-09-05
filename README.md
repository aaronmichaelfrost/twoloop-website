# Twoloop Website with Blog System

This is the Twoloop Games website with an integrated blog system that automatically generates pages from Markdown files.

## Features

- **Dynamic Blog System**: Automatically scans and displays blog posts from Markdown files
- **Markdown Support**: Full Markdown parsing with frontmatter metadata
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive UI**: Smooth animations and transitions
- **Cover Images**: Each blog post can have a cover image

## Blog Post Format

Each blog post should be a Markdown file in the `blog-posts/` directory with the following frontmatter format:

```markdown
---
date: 2025-08-23
cover-image: fractal.gif
title: Your Blog Post Title
description: A short description of your blog post content.
---

# Your Blog Post Title

Your blog content goes here in Markdown format...
```

### Required Frontmatter Fields

- `date`: Publication date in YYYY-MM-DD format
- `title`: The title of the blog post
- `description`: A short description shown in the blog list

### Optional Frontmatter Fields

- `cover-image`: Filename of the cover image (should be in the root directory)

## Running the Website

### Option 1: Local Python Server (Recommended)

1. Open a terminal/command prompt in the website directory
2. Run the Python server:
   ```bash
   python server.py
   ```
3. Open your browser and go to `http://localhost:8000`

### Option 2: Any HTTP Server

You can use any HTTP server, such as:

- Node.js: `npx http-server`
- PHP: `php -S localhost:8000`
- Live Server VS Code extension

**Note**: The blog functionality requires an HTTP server due to CORS restrictions when loading Markdown files.

## Adding New Blog Posts

1. Create a new `.md` file in the `blog-posts/` directory
2. Add the required frontmatter at the top
3. Write your content in Markdown format
4. Add the filename to the `blogPosts` array in `blog.js`
5. Refresh the website to see your new post

## Directory Structure

```
twooloopsite/
├── index.html          # Main website file
├── blog.js            # Blog functionality and Markdown parser
├── server.py          # Local development server
├── blog-posts/        # Directory containing all blog posts
│   ├── devblog-1.md
│   ├── fractal-rendering.md
│   ├── the-journey-begins.md
│   └── community-feedback.md
├── *.gif              # Cover images and animations
├── *.png              # Static images
└── README.md          # This file
```

## Customization

### Adding New Blog Posts to the System

Edit the `blogPosts` array in `blog.js` to include your new Markdown files:

```javascript
const blogPosts = [
    'the-journey-begins.md',
    'devblog-1.md',
    'fractal-rendering.md',
    'community-feedback.md',
    'your-new-post.md'  // Add your new post here
];
```

### Styling

All blog-related styles are in the `<style>` section of `index.html`. Look for classes that start with `.blog-` to customize the appearance.

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript features are used
- CSS Grid and Flexbox for layout

## Troubleshooting

### Blog posts not loading

- Make sure you're running an HTTP server (not opening the HTML file directly)
- Check the browser console for error messages
- Verify that Markdown files are in the correct `blog-posts/` directory
- Ensure frontmatter format is correct (YAML-style with `---` delimiters)

### Images not displaying

- Make sure image files are in the root directory
- Check that the `cover-image` field in frontmatter matches the actual filename
- Verify image file extensions are correct (.gif, .png, .jpg, etc.)

## Future Enhancements

Potential improvements for the blog system:

- Automatic file scanning (no need to manually add filenames to the array)
- Search functionality
- Tag/category system
- RSS feed generation
- Social media sharing
- Comment system integration
