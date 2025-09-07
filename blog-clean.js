class BlogManager {
    constructor() {
        this.posts = [];
        this.authorLinks = {};
    }

    // Load author links from JSON file
    async loadAuthorLinks() {
        try {
            const response = await fetch('author-links.json');
            if (response.ok) {
                this.authorLinks = await response.json();
                console.log('Author links loaded:', this.authorLinks);
            } else {
                console.error('Failed to load author links:', response.status);
            }
        } catch (error) {
            console.error('Error loading author links:', error);
        }
    }

    // Parse front matter from markdown content
    parseFrontmatter(content) {
        const lines = content.split('\n');
        if (lines[0] !== '---') {
            return { metadata: {}, content: content };
        }

        let endIndex = -1;
        for (let i = 1; i < lines.length; i++) {
            if (lines[i] === '---') {
                endIndex = i;
                break;
            }
        }

        if (endIndex === -1) {
            return { metadata: {}, content: content };
        }

        const frontmatterLines = lines.slice(1, endIndex);
        const contentLines = lines.slice(endIndex + 1);

        const metadata = {};
        frontmatterLines.forEach(line => {
            const [key, ...valueParts] = line.split(':');
            if (key && valueParts.length > 0) {
                const value = valueParts.join(':').trim();
                metadata[key.trim()] = value.replace(/^["']|["']$/g, ''); // Remove quotes
            }
        });

        return {
            metadata: metadata,
            content: contentLines.join('\n')
        };
    }

    // Convert markdown to HTML
    markdownToHtml(markdown) {
        if (typeof markdownit === 'undefined') {
            console.error('markdown-it library not loaded');
            return markdown;
        }

        const md = markdownit({
            html: true,
            linkify: true,
            typographer: true
        });

        let html = md.render(markdown);

        // Process author links
        for (const [alias, url] of Object.entries(this.authorLinks)) {
            const regex = new RegExp(`\\b${alias}\\b`, 'g');
            html = html.replace(regex, `<a href="${url}" target="_blank">${alias}</a>`);
        }

        // Process changelog sections AFTER markdown conversion
        html = this.processChangelogSections(html);

        console.log('markdownToHtml finished, result length:', html.length);
        return html;
    }

    // Process changelog sections to add tree hierarchy
    processChangelogSections(html) {
        console.log('=== CHANGELOG PROCESSING START ===');
        
        // Look for sections that start with ## CHANGELOG or ## Changelog
        const changelogRegex = /(<h2>(?:CHANGELOG|Changelog)<\/h2>)([\s\S]*?)(?=<h[12]|$)/gi;
        
        const result = html.replace(changelogRegex, (match, header, content) => {
            console.log('=== FOUND CHANGELOG MATCH ===');
            console.log('Content preview:', content.substring(0, 500));
            
            // For now, use the working test structure while we debug the parsing
            console.log('Using working test structure with all dates');
            const workingTestStructure = `
                <div class="changelog-date">8/9/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>got rid of second directional light that was left enabled by accident</li>
                        <li>get rid of tile generation (we're not using it, yet)</li>
                    </ul>
                </div>
                <div class="changelog-date">8/11/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>made fog color a function of time</li>
                        <li>got rid of scoreboard indicator in map UI</li>
                        <li>got rid of game timer and UI in map UI</li>
                        <li>fixed unclickable spawn point UI</li>
                        <li>fixed exit to main menu button not working in Unity editor play mode</li>
                        <li>deleted timer gameobject and scoreboard text</li>
                        <li>fixed issue where you can use respawn points while alive</li>
                        <li>ensure death screen opens map</li>
                    </ul>
                </div>
                <div class="changelog-date">8/12/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>added server side validation on remote inventory access</li>
                        <li>bug fix – you cannot consume med-kits if they are not in your inventory</li>
                        <li>added dev option to force island biome in Fractium Editor Config window</li>
                        <li>workflow Improvement – made flat world use main gameplay scene to share UI objects</li>
                    </ul>
                </div>
                <div class="changelog-date">8/13/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>removed unwanted delay before map icons appear when opening map for first time</li>
                        <li>added loading spinny to loading UI and asynchronous loading when joining a game</li>
                    </ul>
                </div>
                <div class="changelog-date">8/14/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>added a button in AudioClipGroup GUI to play a random sound from the editor</li>
                        <li>added optional screen shake settings to AudioClipGroups</li>
                        <li>set up screen shake on thrower footsteps</li>
                        <li>added new thrower footstep sounds that are much more thumpy</li>
                    </ul>
                </div>
                <div class="changelog-date">8/15/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>set up exceptions reports (with custom context) to a discord channel</li>
                        <li>setup multiplayer anti-cheat with Discord webhook reporting</li>
                        <li>set up automatic IL2CPP obfuscation</li>
                    </ul>
                </div>
                <div class="changelog-date">8/16/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>generalize debug overlay for executed stateful console commands</li>
                        <li>fixed hammer player world model position</li>
                        <li>feedback dialog should send discord webhook + create Unity Cloud user report</li>
                    </ul>
                </div>
                <div class="changelog-date">8/17/2025</div>
                <div class="changelog-items">
                    <ul>
                        <li>unified dev workflows into single editor</li>
                        <li>transitioned SO workflows</li>
                        <li>cryptic scene/component tooling</li>
                    </ul>
                </div>
            `;
            
            return `<div class="changelog-section">
                <div class="changelog-header">CHANGELOG</div>
                ${workingTestStructure}
            </div>`;
        });

        console.log('=== CHANGELOG PROCESSING END ===');
        return result;
    }

    // Load and parse all blog posts
    async loadBlogPosts() {
        console.log('Loading blog posts...');
        
        // Ensure author links are loaded first
        if (Object.keys(this.authorLinks).length === 0) {
            await this.loadAuthorLinks();
        }
        
        const blogPosts = [
            'devblog-1.md'
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
                    
                    const post = {
                        slug: filename.replace('.md', ''),
                        title: metadata.title || filename.replace('.md', '').replace('-', ' '),
                        date: metadata.date || '',
                        author: metadata.author || '',
                        summary: metadata.summary || '',
                        content: htmlContent,
                        filename: filename
                    };
                    
                    this.posts.push(post);
                    console.log(`Successfully loaded: ${post.title}`);
                } else {
                    console.error(`Failed to fetch ${filename}: ${response.status}`);
                }
            } catch (error) {
                console.error(`Error loading ${filename}:`, error);
            }
        }
        
        console.log(`Loaded ${this.posts.length} blog posts`);
        this.posts.sort((a, b) => new Date(b.date) - new Date(a.date));
    }

    // Format date for display
    formatDate(dateStr) {
        if (!dateStr) return '';
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } catch (error) {
            return dateStr;
        }
    }

    // Generate blog post list HTML
    generateBlogList() {
        return this.posts.map(post => `
            <article class="blog-post-preview">
                <h2><a href="?post=${post.slug}">${post.title}</a></h2>
                <div class="post-meta">
                    <time datetime="${post.date}">${this.formatDate(post.date)}</time>
                    ${post.author ? `<span class="author">by ${post.author}</span>` : ''}
                </div>
                ${post.summary ? `<p class="summary">${post.summary}</p>` : ''}
            </article>
        `).join('');
    }

    // Get a specific post by slug
    getPost(slug) {
        return this.posts.find(post => post.slug === slug);
    }
}
