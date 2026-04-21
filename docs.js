class DocsSystem {
    constructor() {
        this.currentDoc = null;
        this.docs = [];
        this.init();
    }

    async init() {
        console.log('Initializing docs system...');
        await this.loadDocsList();
        this.setupEventListeners();
        
        // Check URL parameters for direct doc access
        const urlParams = new URLSearchParams(window.location.search);
        const docParam = urlParams.get('doc');
        
        if (docParam && this.docs.find(doc => doc.slug === docParam)) {
            // Load the requested doc
            await this.loadDoc(docParam);
            // Set the requested doc link as active
            setTimeout(() => {
                const requestedLink = document.querySelector('.docs-nav-link[data-slug="' + docParam + '"]');
                if (requestedLink) {
                    this.setActiveNavItem(requestedLink);
                }
            }, 100);
        } else if (this.docs.length > 0) {
            // Load first doc by default
            await this.loadDoc(this.docs[0].slug);
            // Set the first doc link as active
            setTimeout(() => {
                const firstLink = document.querySelector('.docs-nav-link[data-slug="' + this.docs[0].slug + '"]');
                if (firstLink) {
                    this.setActiveNavItem(firstLink);
                }
            }, 100);
        }
    }

    async loadDocsList() {
        const docFiles = [
            { title: 'Game Hosting', slug: 'dedicated-servers', order: 1 },
            { title: 'Console Commands', slug: 'console-commands', order: 2 },
            { title: 'Item Wiki', slug: 'item-wiki', order: 3 }
        ];

        this.docs = docFiles.sort((a, b) => a.order - b.order);
        this.renderDocsList();
    }

    renderDocsList() {
        const sidebar = document.getElementById('docsSidebar');
        if (!sidebar) return;

        const docsListHtml = this.docs.map(doc => `
            <li class="docs-nav-item">
                <a href="#" class="docs-nav-link" data-slug="${doc.slug}">
                    ${doc.title}
                </a>
            </li>
        `).join('');

        sidebar.innerHTML = `
            <div class="docs-sidebar-content">
                <div class="docs-sidebar-header">Docs (placeholder)</div>
                <ul class="docs-nav-list">
                    ${docsListHtml}
                </ul>
            </div>
        `;
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.docs-nav-link')) {
                e.preventDefault();
                const slug = e.target.dataset.slug;
                this.loadDoc(slug);
                this.setActiveNavItem(e.target);
                
                // Update URL to include the doc parameter
                if (window.updateUrl) {
                    window.updateUrl('docs', slug);
                }
                
                // Update meta tags for the specific doc
                if (window.updateMetaTags) {
                    setTimeout(() => window.updateMetaTags('docs', slug), 100);
                }
            }
        });
    }

    setActiveNavItem(activeLink) {
        document.querySelectorAll('.docs-nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    async loadDoc(slug) {
        // Show loading spinner
        this.renderLoading();
        
        try {
            console.log(`Loading doc: ${slug}`);
            const response = await fetch(`docs/${slug}.md`);
            
            if (!response.ok) {
                throw new Error(`Failed to load doc: ${response.status}`);
            }

            const markdown = await response.text();
            const { frontmatter, content } = this.parseFrontmatter(markdown);
            
            this.currentDoc = {
                slug,
                title: frontmatter.title || slug,
                lastUpdated: frontmatter.last_updated || null,
                content: content
            };

            this.renderDoc();
            
            // Set the active navigation item for this doc
            setTimeout(() => {
                const activeLink = document.querySelector('.docs-nav-link[data-slug="' + slug + '"]');
                if (activeLink) {
                    this.setActiveNavItem(activeLink);
                }
            }, 100);
            
        } catch (error) {
            console.error('Error loading doc:', error);
            this.renderError(`Failed to load documentation: ${slug}`);
        }
    }

    parseFrontmatter(markdown) {
        const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
        const match = markdown.match(frontmatterRegex);
        
        if (!match) {
            return { frontmatter: {}, content: markdown };
        }

        const frontmatterText = match[1];
        const content = match[2];
        
        const frontmatter = {};
        frontmatterText.split('\n').forEach(line => {
            const colonIndex = line.indexOf(':');
            if (colonIndex > 0) {
                const key = line.substring(0, colonIndex).trim();
                const value = line.substring(colonIndex + 1).trim().replace(/^["']|["']$/g, '');
                if (key && value) {
                    frontmatter[key] = value;
                }
            }
        });

        return { frontmatter, content };
    }

    renderLoading() {
        const content = document.getElementById('docsContent');
        if (!content) return;

        content.innerHTML = `
            <div class="docs-loading">
                <div class="docs-spinner"></div>
                <span>Loading documentation...</span>
            </div>
        `;
    }

    renderDoc() {
        const content = document.getElementById('docsContent');
        if (!content) return;

        const htmlContent = this.markdownToHtml(this.currentDoc.content);
        const lastUpdatedHtml = this.currentDoc.lastUpdated
            ? `<p class="docs-last-updated">Last updated: ${this.currentDoc.lastUpdated}</p>`
            : '';
        // Inject last-updated immediately after the first <h1>
        const htmlWithTimestamp = htmlContent.replace(/(<h1[^>]*>.*?<\/h1>)/, `$1${lastUpdatedHtml}`);
        content.innerHTML = `
            <div class="docs-content-wrapper">
                <article class="docs-article">
                    ${htmlWithTimestamp}
                </article>
            </div>
        `;

        // Scroll to top
        content.scrollTop = 0;
    }

    renderError(message) {
        const content = document.getElementById('docsContent');
        if (!content) return;

        content.innerHTML = `
            <div class="docs-error">
                <h2>Error</h2>
                <p>${message}</p>
                <p>Please try again or contact support if the problem persists.</p>
            </div>
        `;
    }

    markdownToHtml(markdown) {
        // Simple markdown parser - enhanced version of blog parser
        let html = markdown;

        // Store code blocks temporarily to protect them from all processing
        const codeBlocks = [];
        html = html.replace(/```(\w+)?\s*\n([\s\S]*?)\n```/g, (match, lang, code) => {
            const language = lang || '';
            const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
            codeBlocks.push(`<div class="code-block"><pre><code class="language-${language}">${this.escapeHtml(code)}</code></pre></div>`);
            return placeholder;
        });

        // Horizontal rules (must be processed before paragraphs)
        html = html.replace(/^---$/gm, '<hr>');

        // Tables
        html = this.parseMarkdownTables(html);

        // Lists (process before headers to avoid header/list conflicts)
        html = html.replace(/^\- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/^• (.+)$/gm, '<li>$1</li>'); // Support filled bullet character
        html = html.replace(/^◦ (.+)$/gm, '<li>$1</li>'); // Support hollow bullet character
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
        
        // Group consecutive list items into ul/ol tags
        html = this.groupListItems(html);

        // Headers - trim leading whitespace (process after lists)
        html = html.replace(/^\s*#### (.*$)/gm, '<h4>$1</h4>');
        html = html.replace(/^\s*### (.*$)/gm, '<h3>$1</h3>');
        html = html.replace(/^\s*## (.*$)/gm, '<h2>$1</h2>');
        html = html.replace(/^\s*# (.*$)/gm, '<h1>$1</h1>');

        // Inline code
        html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');

        // Bold and italic
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Paragraphs
        html = html.split('\n\n').map(paragraph => {
            paragraph = paragraph.trim();
            if (paragraph && 
                !paragraph.includes('<h') && 
                !paragraph.includes('<ul') && 
                !paragraph.includes('<ol') && 
                !paragraph.includes('<div') &&
                !paragraph.includes('<table') &&
                !paragraph.includes('__CODE_BLOCK_')) {
                return `<p>${paragraph}</p>`;
            }
            return paragraph;
        }).join('\n\n');

        // Post-process to identify paragraphs that precede headers and mark them
        html = this.markPreHeaderText(html);

        // Restore code blocks
        codeBlocks.forEach((block, index) => {
            html = html.replace(`__CODE_BLOCK_${index}__`, block);
        });

        return html;
    }

    groupListItems(html) {
        const lines = html.split('\n');
        const result = [];
        let inList = false;
        let listItems = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (line.startsWith('<li>') && line.endsWith('</li>')) {
                // This is a list item
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(line);
            } else {
                // This is not a list item
                if (inList) {
                    // Close the current list
                    result.push('<ul>');
                    result.push(...listItems);
                    result.push('</ul>');
                    listItems = [];
                    inList = false;
                }
                // Only add non-empty lines
                if (line || lines[i] !== '') {
                    result.push(lines[i]);
                }
            }
        }
        
        // Handle case where file ends with a list
        if (inList && listItems.length > 0) {
            result.push('<ul>');
            result.push(...listItems);
            result.push('</ul>');
        }
        
        return result.join('\n');
    }

    // Mark the first paragraph that comes immediately after a title header as pre-header text
    markPreHeaderText(html) {
        // Split into lines for processing
        const lines = html.split('\n');
        const result = [];
        let lastWasH1 = false;
        let hasSeenContentAfterH1 = false;
        
        for (let i = 0; i < lines.length; i++) {
            const currentLine = lines[i].trim();
            
            // Reset flags when we see an H1
            if (currentLine.match(/^<h1/)) {
                lastWasH1 = true;
                hasSeenContentAfterH1 = false;
                result.push(lines[i]);
            }
            // Check if current line is a paragraph
            else if (currentLine.startsWith('<p>')) {
                // Only apply styling if this is the first paragraph after an H1 and we haven't seen other content
                if (lastWasH1 && !hasSeenContentAfterH1) {
                    const modifiedLine = currentLine.replace('<p>', '<p class="pre-header-text">');
                    result.push(modifiedLine);
                    hasSeenContentAfterH1 = true; // Mark that we've seen content after H1
                } else {
                    result.push(lines[i]);
                }
            }
            // Any other content (headers, lists, images, etc.) resets our tracking
            else if (currentLine && !currentLine.match(/^<h1/)) {
                if (currentLine.match(/^<h[2-4]/)) {
                    lastWasH1 = false; // We've moved past the H1 section
                }
                hasSeenContentAfterH1 = true;
                result.push(lines[i]);
            }
            // Empty lines don't affect our tracking
            else {
                result.push(lines[i]);
            }
        }
        
        return result.join('\n');
    }

    parseMarkdownTables(html) {
        // Match markdown tables with the pattern: |header|header| followed by |---|---| followed by data rows
        const lines = html.split('\n');
        let result = [];
        let i = 0;

        while (i < lines.length) {
            const line = lines[i];
            
            // Check if this line looks like a table header (starts and ends with |)
            if (line.trim().startsWith('|') && line.trim().endsWith('|') && line.includes('|')) {
                // Check if the next line is a separator line
                if (i + 1 < lines.length) {
                    const nextLine = lines[i + 1];
                    if (nextLine.trim().match(/^\|[\s\-:|]+\|$/)) {
                        // This is a table, parse it
                        const tableLines = [line, nextLine];
                        let j = i + 2;
                        
                        // Collect all table rows
                        while (j < lines.length && lines[j].trim().startsWith('|') && lines[j].trim().endsWith('|')) {
                            tableLines.push(lines[j]);
                            j++;
                        }
                        
                        // Convert table lines to HTML
                        const tableHtml = this.convertTableToHtml(tableLines);
                        result.push(tableHtml);
                        
                        // Skip the processed lines
                        i = j;
                        continue;
                    }
                }
            }
            
            result.push(line);
            i++;
        }
        
        return result.join('\n');
    }

    convertTableToHtml(tableLines) {
        if (tableLines.length < 3) return tableLines.join('\n');
        
        const headerLine = tableLines[0];
        const dataLines = tableLines.slice(2);
        
        // Parse header
        const headers = headerLine.split('|').slice(1, -1).map(h => h.trim());
        
        // Parse data rows
        const rows = dataLines.map(line => 
            line.split('|').slice(1, -1).map(cell => cell.trim())
        );

        let tableHtml = '<div class="table-container"><table class="docs-table">\n';
        tableHtml += '<thead><tr>';
        headers.forEach(header => {
            tableHtml += `<th>${header}</th>`;
        });
        tableHtml += '</tr></thead>\n<tbody>';
        
        rows.forEach(row => {
            tableHtml += '<tr>';
            row.forEach(cell => {
                tableHtml += `<td>${cell}</td>`;
            });
            tableHtml += '</tr>';
        });
        
        tableHtml += '</tbody></table></div>';
        return tableHtml;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize docs system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('docsContainer')) {
        window.docsSystem = new DocsSystem();
    }
});
