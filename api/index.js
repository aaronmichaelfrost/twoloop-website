const fs = require('fs');
const path = require('path');

// Only allow safe slug characters to prevent path traversal
const SAFE_SLUG_RE = /^[a-zA-Z0-9_-]+$/;

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function parseFrontmatter(content) {
    const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!match) return {};
    const metadata = {};
    for (const line of match[1].split('\n')) {
        const colonIdx = line.indexOf(':');
        if (colonIdx > -1) {
            metadata[line.slice(0, colonIdx).trim()] = line.slice(colonIdx + 1).trim();
        }
    }
    return metadata;
}

module.exports = (req, res) => {
    const urlObj = new URL(req.url, 'https://twoloop.net');
    const page = urlObj.searchParams.get('page') || 'about';
    const post = urlObj.searchParams.get('post');

    const htmlPath = path.join(process.cwd(), 'index.html');
    let html;
    try {
        html = fs.readFileSync(htmlPath, 'utf8');
    } catch {
        res.status(500).send('Internal Server Error');
        return;
    }

    const baseUrl = 'https://twoloop.net';
    let title = 'twoloop';
    let description = 'twoloop games - Fractium development';
    let image = `${baseUrl}/playtest.png`;
    let ogUrl = baseUrl;

    if (page === 'blog' && post && SAFE_SLUG_RE.test(post)) {
        const mdPath = path.join(process.cwd(), 'blog-posts', `${post}.md`);
        if (fs.existsSync(mdPath)) {
            const metadata = parseFrontmatter(fs.readFileSync(mdPath, 'utf8'));
            if (metadata.title) {
                title = `${metadata.title} - twoloop`;
                description = metadata.description || 'twoloop games blog post';
                const coverImage = metadata['cover-image'];
                if (coverImage) {
                    image = (coverImage.startsWith('http') || coverImage.startsWith('//'))
                        ? coverImage
                        : `${baseUrl}/blog-posts/${coverImage}`;
                }
                ogUrl = `${baseUrl}/?page=blog&post=${encodeURIComponent(post)}`;
            }
        }
    } else if (page === 'blog') {
        title = 'Blog - twoloop';
        description = 'twoloop games development blog';
        ogUrl = `${baseUrl}/?page=blog`;
    }

    // Escape values before injecting into HTML attributes
    const safeTitle = escapeHtml(title);
    const safeDescription = escapeHtml(description);
    const safeImage = escapeHtml(image);
    const safeUrl = escapeHtml(ogUrl);

    html = html
        .replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${safeTitle}">`)
        .replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${safeDescription}">`)
        .replace(/<meta property="og:image" content="[^"]*">/, `<meta property="og:image" content="${safeImage}">`)
        .replace(/<meta property="og:image:secure_url" content="[^"]*">/, `<meta property="og:image:secure_url" content="${safeImage}">`)
        .replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${safeUrl}">`)
        .replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${safeTitle}">`)
        .replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${safeDescription}">`)
        .replace(/<meta name="twitter:image" content="[^"]*">/, `<meta name="twitter:image" content="${safeImage}">`)
        .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${safeDescription}">`)
        .replace(/<title>[^<]*<\/title>/, `<title>${safeTitle}</title>`);

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200).send(html);
};
