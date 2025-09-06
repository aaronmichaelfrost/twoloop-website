// Image loading handlers
function handleImageLoad(img) {
    img.classList.add('loaded');
    const loadingElement = img.parentElement.querySelector('.image-loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

function handleImageError(img) {
    const container = img.parentElement;
    const loadingElement = container.querySelector('.image-loading');
    if (loadingElement) {
        loadingElement.innerHTML = '<span style="color: rgba(255,255,255,0.4);">Failed to load image</span>';
    }
    img.style.display = 'none';
}

// Simple markdown parser for blog posts
class MarkdownParser {
    constructor() {
        this.posts = [];
    }

    // Parse frontmatter (YAML-like metadata at the top of markdown files)
    parseFrontmatter(content) {
        const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
        const match = content.match(frontmatterRegex);
        
        if (!match) {
            return { metadata: {}, content: content };
        }

        const frontmatterStr = match[1];
        const markdownContent = match[2];
        const metadata = {};

        // Parse YAML-like frontmatter
        frontmatterStr.split('\n').forEach(line => {
            const colonIndex = line.indexOf(':');
            if (colonIndex > -1) {
                const key = line.substring(0, colonIndex).trim();
                const value = line.substring(colonIndex + 1).trim();
                metadata[key] = value;
            }
        });

        return { metadata, content: markdownContent };
    }

    // Simple markdown to HTML conversion
    markdownToHtml(markdown) {
        let html = markdown;

        // Store code blocks temporarily to protect them
        const codeBlocks = [];
        html = html.replace(/```[\s\S]*?```/g, (match) => {
            const code = match.replace(/```/g, '').trim();
            const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
            codeBlocks.push(`<pre><code>${code}</code></pre>`);
            return placeholder;
        });

        // Images
        html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<div class="blog-content-image"><img src="$2" alt="$1"></div>');

        // Author attribution inline with headers (e.g., ## Title *by Author*)
        html = html.replace(/^(#{1,4})\s+(.+?)\s+\*by ([^*]+)\*$/gm, '$1 $2<span class="author-attribution">by $3</span>');

        // Headers
        html = html.replace(/^#### (.*$)/gm, '<h4>$1</h4>');
        html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

        // Bold and italic
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Inline code
        html = html.replace(/`(.+?)`/g, '<code>$1</code>');

        // Lists
        html = html.replace(/^\* (.+$)/gm, '<li>$1</li>');
        html = html.replace(/^(\d+)\. (.+$)/gm, '<li>$2</li>');
        
        // Wrap consecutive list items in ul/ol tags
        html = html.replace(/(<li>.*<\/li>)\s*(<li>.*<\/li>)/g, '$1\n$2');
        html = html.replace(/(<li>.*?<\/li>(?:\s*<li>.*?<\/li>)*)/gs, '<ul>$1</ul>');

        // Paragraphs
        html = html.replace(/^(?!<[hup]|<li|<\/[uo]|<pre|<code|<div class="blog-content-image|<div class="author-attribution|__CODE_BLOCK_)(.+$)/gm, '<p>$1</p>');

        // Clean up empty paragraphs
        html = html.replace(/<p>\s*<\/p>/g, '');

        // Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

        // Restore code blocks
        codeBlocks.forEach((block, index) => {
            html = html.replace(`__CODE_BLOCK_${index}__`, block);
        });

        return html;
    }

    // Load and parse all blog posts
    async loadBlogPosts() {
        console.log('Loading blog posts...');
        const blogPosts = [
            'the-journey-begins.md',
            'devblog-1.md',
            'fractal-rendering.md',
            'community-feedback.md'
        ];

        this.posts = [];

        for (const filename of blogPosts) {
            try {
                console.log(`Fetching ${filename}...`);
                const response = await fetch(`blog-posts/${filename}`);
                console.log(`Response for ${filename}:`, response.status, response.ok);
                
                if (response.ok) {
                    const content = await response.text();
                    console.log(`Content length for ${filename}:`, content.length);
                    const { metadata, content: markdownContent } = this.parseFrontmatter(content);
                    const htmlContent = this.markdownToHtml(markdownContent);
                    
                    this.posts.push({
                        filename: filename.replace('.md', ''),
                        metadata,
                        content: htmlContent,
                        slug: filename.replace('.md', '')
                    });
                    console.log(`Successfully loaded ${filename}`);
                } else {
                    console.error(`Failed to fetch ${filename}: ${response.status} ${response.statusText}`);
                }
            } catch (error) {
                console.error(`Error loading ${filename}:`, error);
            }
        }

        // Sort posts by date (newest first)
        this.posts.sort((a, b) => new Date(b.metadata.date) - new Date(a.metadata.date));
        return this.posts;
    }

    // Format date for display
    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }

    // Generate blog list HTML
    generateBlogList() {
        console.log('Generating blog list, posts count:', this.posts.length);
        if (this.posts.length === 0) {
            return '<p style="color: white; font-size: 1.2rem; text-align: center; padding: 2rem;">No blog posts found. Loading...</p>';
        }
        
        const blogListHtml = this.posts.map(post => `
            <div class="blog-post" onclick="showBlogPost('${post.slug}')">
                <div class="blog-post-meta">${this.formatDate(post.metadata.date)}</div>
                <div class="blog-png-container">
                    ${post.metadata['cover-image'] ? 
                        `<div class="image-loading" style="display: flex; align-items: center; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
                            <div class="loading-spinner"></div>
                            Loading...
                        </div>
                        <img src="${post.metadata['cover-image']}" alt="${post.metadata.title}" onload="handleImageLoad(this)" onerror="handleImageError(this)">` : 
                        '<div class="blog-png-placeholder">No cover image</div>'
                    }
                </div>
                <h3>${post.metadata.title}</h3>
                <p>${post.metadata.description}</p>
            </div>
        `).join('');
        
        console.log('Generated blog list HTML length:', blogListHtml.length);
        return blogListHtml;
    }

    // Get a specific post by slug
    getPost(slug) {
        return this.posts.find(post => post.slug === slug);
    }
}

// Initialize the markdown parser
const markdownParser = new MarkdownParser();

// Blog functionality
let currentPage = 'about';

function showBlogPost(slug) {
    const post = markdownParser.getPost(slug);
    if (!post) {
        console.error('Post not found:', slug);
        return;
    }

    // Update the blog page content
    const blogContent = document.querySelector('.blog-content');
    const coverImage = post.metadata['cover-image'] ? 
        `<div class="blog-post-cover">
            <div class="image-loading" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; display: flex; align-items: center; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
                <div class="loading-spinner"></div>
                Loading...
            </div>
            <img src="${post.metadata['cover-image']}" alt="${post.metadata.title}" onload="handleImageLoad(this)" onerror="handleImageError(this)">
        </div>` : 
        '';

    blogContent.innerHTML = `
        <div class="blog-post-header">
            <button class="back-to-blog" onclick="showBlogList()">← go back</button>
            <div class="blog-post-meta">${markdownParser.formatDate(post.metadata.date)}</div>
            ${coverImage}
            <h1>${post.metadata.title}</h1>
        </div>
        <div class="blog-post-content">
            ${post.content}
        </div>
    `;

    // Update background for individual post
    const backgroundContainer = document.querySelector('.background-container');
    if (post.metadata['cover-image']) {
        backgroundContainer.style.background = "";
        backgroundContainer.style.backgroundImage = `url('${post.metadata['cover-image']}')`;
        backgroundContainer.style.backgroundSize = "cover";
        backgroundContainer.style.backgroundPosition = "center";
        backgroundContainer.style.backgroundRepeat = "no-repeat";
        backgroundContainer.style.backgroundAttachment = "fixed";
        backgroundContainer.style.filter = "blur(25px) grayscale(0%) saturate(100%)";
        backgroundContainer.style.transform = "scale(1.1)";
    } else {
        // Fallback to rload3 if no cover image
        backgroundContainer.style.backgroundImage = "url('rload3.png')";
        backgroundContainer.style.background = "";
        backgroundContainer.style.backgroundSize = "cover";
        backgroundContainer.style.backgroundPosition = "center";
        backgroundContainer.style.backgroundRepeat = "no-repeat";
        backgroundContainer.style.backgroundAttachment = "fixed";
        backgroundContainer.style.filter = "blur(25px) grayscale(0%) saturate(100%)";
        backgroundContainer.style.transform = "scale(1.1)";
    }
}

function showBlogList() {
    console.log('showBlogList called, posts count:', markdownParser.posts.length);
    
    // Ensure posts are loaded first
    ensureBlogPostsLoaded();
    
    const blogContent = document.querySelector('.blog-content');
    blogContent.innerHTML = `
        <h1>Blog</h1>
        <div class="blog-posts-container">
            ${markdownParser.generateBlogList()}
        </div>
    `;

    // Preload all blog post images
    markdownParser.posts.forEach(post => {
        if (post.metadata['cover-image']) {
            const img = new Image();
            img.src = post.metadata['cover-image'];
        }
    });

    // Set dload2 background with blur for blog list
    const backgroundContainer = document.querySelector('.background-container');
    backgroundContainer.style.backgroundImage = "url('dload2.png')";
    backgroundContainer.style.background = "";
    backgroundContainer.style.backgroundSize = "cover";
    backgroundContainer.style.backgroundPosition = "center";
    backgroundContainer.style.backgroundRepeat = "no-repeat";
    backgroundContainer.style.backgroundAttachment = "fixed";
    backgroundContainer.style.filter = "blur(25px) grayscale(0%) saturate(100%)";
    backgroundContainer.style.transform = "scale(1.1)";

    // Animate blog header
    const blogHeader = document.querySelector('.blog-content h1');
    if (blogHeader) {
        blogHeader.classList.remove('animate-in');
        setTimeout(() => {
            blogHeader.classList.add('animate-in');
        }, 100);
    }
}

// Initialize blog posts when the page loads
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, initializing blog...');
    try {
        await markdownParser.loadBlogPosts();
        console.log('Blog posts loaded successfully:', markdownParser.posts.length);
        
        // If we're currently on the blog page, refresh the content
        if (document.body.classList.contains('blog-active')) {
            console.log('Currently on blog page, refreshing content...');
            showBlogList();
        }
    } catch (error) {
        console.error('Error loading blog posts:', error);
    }
});

// Also try to load when the blog page is shown
function ensureBlogPostsLoaded() {
    console.log('Ensuring blog posts are loaded...');
    if (markdownParser.posts.length === 0) {
        console.log('No posts found, loading...');
        markdownParser.loadBlogPosts().then(() => {
            console.log('Posts loaded, refreshing blog list...');
            if (document.body.classList.contains('blog-active')) {
                showBlogList();
            }
        }).catch(error => {
            console.error('Failed to load blog posts:', error);
        });
    }
}
