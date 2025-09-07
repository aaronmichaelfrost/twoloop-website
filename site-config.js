// Site configuration for twoloop website
const SITE_CONFIG = {
    // Update this to match your actual domain
    domain: 'https://twoloop.net',
    
    // Default social media image (should be 1200x630 for best results)
    defaultSocialImage: '/playtest.png',
    
    // Site metadata
    siteName: 'twoloop',
    defaultTitle: 'twoloop',
    defaultDescription: 'twoloop games - Fractium development',
    
    // Social media handles
    twitter: '@twoloop',
    
    // Get the full URL for the social image
    getSocialImageUrl() {
        return this.domain + this.defaultSocialImage;
    },
    
    // Get the canonical URL for a page
    getCanonicalUrl(path = '') {
        return this.domain + (path.startsWith('/') ? path : '/' + path);
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SITE_CONFIG;
}

// Make available globally in browser
if (typeof window !== 'undefined') {
    window.SITE_CONFIG = SITE_CONFIG;
}
