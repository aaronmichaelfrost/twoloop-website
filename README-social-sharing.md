# Social Media Sharing Setup

This setup ensures that `playtest.png` is used as the cover image when sharing any URL from your website on social media platforms like Discord, Twitter, Facebook, LinkedIn, iMessage, etc.

## What's Been Configured

### 1. Main Website (`index.html`)
- ✅ Added comprehensive Open Graph meta tags
- ✅ Added Twitter Card meta tags  
- ✅ Set up dynamic meta tag updating for different pages (blog, docs, etc.)
- ✅ All social images point to `https://twoloop.games/playtest.png`

### 2. Configuration System
- ✅ Created `site-config.js` for centralized domain and social media settings
- ✅ Easy to update domain if it changes
- ✅ Consistent social image across all pages

### 3. Testing Tools
- ✅ `test-social-sharing.html` - Browser-based meta tag validator
- ✅ `verify-social-sharing.py` - Python script for automated checking
- ✅ `robots.txt` - Ensures social media crawlers can access your site

## Key Features

### Universal Cover Image
- **All pages** (home, blog posts, docs) use `playtest.png` as the social media preview
- Uses absolute URLs (`https://twoloop.games/playtest.png`) for compatibility
- Optimized for 1200x630 pixels (recommended social media dimensions)

### Dynamic Meta Tags
The website automatically updates meta tags when navigating to different sections:
- Home page: "twoloop"
- Blog posts: "Post Title - twoloop" 
- Documentation: "Documentation - twoloop"
- Always uses the same cover image

### Social Platform Support
Configured for optimal sharing on:
- 🐦 Twitter/X
- 📘 Facebook
- 💼 LinkedIn  
- 💬 Discord
- 📱 iMessage
- 💬 WhatsApp
- 🔗 Other messaging platforms

## Testing Your Setup

### 1. Use the Built-in Test Page
Open `test-social-sharing.html` in your browser to:
- View all current meta tags
- Check if absolute URLs are being used
- Verify playtest.png is configured correctly
- Get links to social media debug tools

### 2. Social Media Debug Tools
Test your URLs in these official tools:
- **Facebook**: https://developers.facebook.com/tools/debug/
- **Twitter**: https://cards-dev.twitter.com/validator
- **LinkedIn**: https://www.linkedin.com/post-inspector/

### 3. Real-world Testing
- Share your URL in Discord and check the preview
- Send the link in iMessage or WhatsApp
- Post on social media platforms

## Configuration

### Update Your Domain
If your domain is different from `twoloop.games`, update `site-config.js`:

```javascript
const SITE_CONFIG = {
    domain: 'https://your-actual-domain.com', // Update this
    defaultSocialImage: '/playtest.png',
    // ... rest of config
};
```

### Change the Social Image
To use a different image instead of `playtest.png`:

1. Update `site-config.js`:
```javascript
defaultSocialImage: '/your-new-image.png',
```

2. Make sure the image is:
   - At least 1200x630 pixels
   - Under 8MB in size
   - In PNG, JPG, or WebP format
   - Accessible via absolute URL

## Troubleshooting

### Common Issues

1. **Social platforms showing old image**
   - Social media platforms cache previews heavily
   - Use debug tools to force refresh the cache
   - It may take hours or days for changes to appear

2. **Image not loading**
   - Verify the image URL is accessible publicly
   - Check that your server serves the image with proper headers
   - Ensure no authentication is required to access the image

3. **Wrong domain in meta tags**
   - Update `site-config.js` with your actual domain
   - The domain must match where your site is hosted

### Verification Steps

1. ✅ Image `playtest.png` exists and is accessible
2. ✅ Meta tags use absolute URLs (start with `https://`)
3. ✅ Domain in configuration matches your actual domain
4. ✅ Social media crawlers can access your site (check `robots.txt`)
5. ✅ Test with social media debug tools

## Files Modified/Created

- `index.html` - Updated with social media meta tags
- `site-config.js` - Configuration for domain and social settings
- `test-social-sharing.html` - Testing tool for meta tags
- `verify-social-sharing.py` - Automated verification script
- `robots.txt` - Allows social media crawlers
- `README-social-sharing.md` - This documentation

## Support

Your website should now consistently show `playtest.png` as the cover image when shared on any social media platform or messaging app. The setup is automatic and works for all pages including blog posts and documentation.
