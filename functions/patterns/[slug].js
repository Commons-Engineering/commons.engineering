/**
 * Cloudflare Pages Function — Dynamic Pattern Router
 *
 * This function handles /patterns/<slug>/ requests that aren't
 * served by static Hugo pages. It fetches the pattern markdown
 * from R2 and renders it dynamically.
 *
 * To use this, you need:
 *   1. An R2 bucket named "commons-patterns" bound as PATTERNS_BUCKET
 *   2. Patterns uploaded to R2 via scripts/upload_to_r2.sh
 *
 * Binding configuration in wrangler.toml or Cloudflare dashboard:
 *   [[r2_buckets]]
 *   binding = "PATTERNS_BUCKET"
 *   bucket_name = "commons-patterns"
 */

// ─── Frontmatter Parser ─────────────────────────────────────────
function parseFrontmatter(text) {
  if (!text.startsWith('---')) return { meta: {}, body: text };
  const end = text.indexOf('\n---', 3);
  if (end === -1) return { meta: {}, body: text };

  const yamlStr = text.slice(3, end).trim();
  const body = text.slice(end + 4).trim();

  const meta = {};
  let currentKey = null;

  for (const line of yamlStr.split('\n')) {
    const trimmed = line.trimEnd();
    if (!trimmed || trimmed.startsWith('#')) continue;

    if (trimmed.startsWith('  ') && currentKey) {
      const match = trimmed.match(/^\s+(\w[\w_]*):\s*(.*)$/);
      if (match) {
        if (typeof meta[currentKey] !== 'object' || Array.isArray(meta[currentKey])) {
          meta[currentKey] = {};
        }
        let val = match[2].trim();
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
        meta[currentKey][match[1]] = val;
        continue;
      }
      const arrMatch = trimmed.match(/^\s+-\s+(.*)$/);
      if (arrMatch) {
        if (!Array.isArray(meta[currentKey])) meta[currentKey] = [];
        let val = arrMatch[1].trim();
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
        meta[currentKey].push(val);
        continue;
      }
    }

    const topMatch = trimmed.match(/^(\w[\w_]*):\s*(.*)$/);
    if (topMatch) {
      currentKey = topMatch[1];
      let val = topMatch[2].trim();
      if (val === '' || val === '|' || val === '>') {
        meta[currentKey] = '';
        continue;
      }
      if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
      meta[currentKey] = val;
    }
  }

  return { meta, body };
}

// ─── Markdown to HTML ────────────────────────────────────────────
function markdownToHtml(md) {
  let html = md;
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  const lines = html.split('\n');
  const result = [];
  let inP = false;
  for (const line of lines) {
    const t = line.trim();
    if (!t) { if (inP) { result.push('</p>'); inP = false; } continue; }
    if (t.startsWith('<h') || t.startsWith('<ul') || t.startsWith('<li') ||
        t.startsWith('<blockquote') || t.startsWith('</ul') || t.startsWith('<ol')) {
      if (inP) { result.push('</p>'); inP = false; }
      result.push(t);
      continue;
    }
    if (!inP) { result.push('<p>'); inP = true; }
    result.push(t);
  }
  if (inP) result.push('</p>');
  return result.join('\n');
}

function esc(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ─── HTML Template ───────────────────────────────────────────────
function renderPage(meta, bodyHtml, slug) {
  const title = meta.title || slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const summary = meta.summary || '';
  const domain = meta.commons_domain || meta.domain || '';

  let badges = '';
  if (domain) badges += `<span class="badge badge-domain">${esc(domain)}</span>`;

  const aliasHtml = Array.isArray(meta.aliases)
    ? `<p class="aliases">Also known as: ${meta.aliases.map(esc).join(', ')}</p>` : '';
  const summaryBlock = summary
    ? `<blockquote class="pattern-summary">${esc(summary)}</blockquote>` : '';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(title)} — Commons Engineering</title>
  <meta name="description" content="${esc(summary || title)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"><\/script>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;line-height:1.6;color:#333;background:#fafafa}
    .nav{background:#fff;border-bottom:1px solid #e8e8e8;padding:0 20px;position:sticky;top:0;z-index:1000;box-shadow:0 2px 10px rgba(0,0,0,.03)}
    .nav-container{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:65px}
    .nav-brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:600;font-size:1.2em;color:#333}
    .nav-brand .logo-icon{width:36px;height:36px;background:linear-gradient(135deg,#5BC0DE,#3AAADC);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff}
    .nav-brand span{color:#3AAADC}
    .nav-links{display:flex;align-items:center;gap:8px}
    .nav-link{padding:8px 16px;text-decoration:none;color:#555;font-weight:500;font-size:.95em;border-radius:8px;transition:all .2s}
    .nav-link:hover{background:#EBF6FB;color:#3AAADC}
    .nav-cta{padding:10px 20px;background:linear-gradient(135deg,#3AAADC,#2E94BD);color:#fff;text-decoration:none;border-radius:25px;font-weight:500;font-size:.9em;transition:all .2s;margin-left:15px}
    .pattern-page{max-width:800px;margin:0 auto;padding:40px 24px}
    .back-link{display:inline-flex;align-items:center;gap:6px;color:#3AAADC;text-decoration:none;font-weight:500;font-size:.95em;margin-bottom:20px}
    .pattern-header{margin-bottom:2rem;padding-bottom:1rem;border-bottom:2px solid #e6e9ed}
    .pattern-meta{margin-bottom:1rem;display:flex;gap:8px;flex-wrap:wrap}
    .badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.8em;font-weight:500;background:#f1f5f9;color:#475569}
    .badge-domain{background:#e3f2fd;color:#1565c0}
    .badge-vitality{background:#ecfdf5;color:#065f46}
    .badge-orbital{background:#ede9fe;color:#5b21b6}
    .pattern-header h1{font-size:2rem;color:#2c3e50;margin:0 0 10px;border:none;padding:0}
    .aliases{color:#5a738e;font-style:italic;font-size:.95em;margin-bottom:10px}
    .pattern-summary{font-size:1.05rem;border-left:4px solid #3AAADC;padding:.75rem 1rem;margin:1rem 0;background:#f8fafc;color:#334155;line-height:1.7}
    .pattern-content{line-height:1.8;color:#475569}
    .pattern-content h2{font-size:1.4rem;color:#2c3e50;margin-top:2rem;margin-bottom:.75rem;border-bottom:2px solid #e8e8e8;padding-bottom:.5rem}
    .pattern-content h3{font-size:1.15rem;color:#2c3e50;margin-top:1.5rem}
    .pattern-content p{margin-bottom:1rem;color:#475569}
    .pattern-content ul,.pattern-content ol{margin:1rem 0;padding-left:2rem}
    .pattern-content li{margin-bottom:.5rem;color:#475569}
    .pattern-content blockquote{border-left:4px solid #3AAADC;padding-left:1rem;margin:1rem 0;color:#666}
    .pattern-content strong{color:#2c3e50}
    .pattern-footer{margin-top:3rem;padding-top:1rem;border-top:1px solid #e6e9ed;font-size:.875rem;color:#5a738e}
    .pattern-footer a{color:#3AAADC}
    .site-footer{text-align:center;padding:40px 20px;border-top:1px solid #e8e8e8;margin-top:60px;color:#888;font-size:.85em}
    .site-footer a{color:#3AAADC;text-decoration:none}
  </style>
</head>
<body>
  <nav class="nav"><div class="nav-container">
    <a href="/" class="nav-brand"><div class="logo-icon"><i data-lucide="hexagon" style="width:20px;height:20px"></i></div><span>Commons</span></a>
    <div class="nav-links">
      <a href="/context/" class="nav-link"><i data-lucide="search" style="width:16px;height:16px"></i> Context</a>
      <a href="/patterns/" class="nav-link"><i data-lucide="hexagon" style="width:16px;height:16px"></i> Pattern</a>
      <a href="/build/" class="nav-link"><i data-lucide="hammer" style="width:16px;height:16px"></i> Build</a>
      <a href="https://cloudsters.substack.com" class="nav-cta" target="_blank">Learn</a>
    </div>
  </div></nav>
  <main><div class="pattern-page">
    <a href="/patterns/" class="back-link">&larr; Back to Patterns</a>
    <header class="pattern-header">
      <div class="pattern-meta">${badges}</div>
      <h1>${esc(title)}</h1>
      ${aliasHtml}
      ${summaryBlock}
    </header>
    <div class="pattern-content">${bodyHtml}</div>
    <footer class="pattern-footer">
      <p><strong>License:</strong> CC-BY-SA-4.0</p>
      <p><a href="https://github.com/Commons-Engineering/pattern-engine">View source on GitHub</a></p>
    </footer>
  </div></main>
  <footer class="site-footer">
    <p>Commons Engineering — Building the infrastructure for shared prosperity</p>
    <p><a href="https://github.com/Commons-Engineering">GitHub</a> · <a href="https://cloudsters.substack.com">Newsletter</a></p>
  </footer>
  <script>lucide.createIcons()<\/script>
</body>
</html>`;
}

// ─── Domains to search ───────────────────────────────────────────
const DOMAINS = ['urban', 'life', 'business', 'ecology'];

export async function onRequest(context) {
  const { params, env } = context;
  const slug = params.slug;

  // Skip known static routes
  const staticRoutes = ['urban', 'life', 'business', 'ecology', 'commons-engineer', 'commons-blueprint'];
  if (staticRoutes.includes(slug)) {
    return context.next();
  }

  // Try R2 bucket if bound
  if (env.PATTERNS_BUCKET) {
    for (const domain of DOMAINS) {
      const key = `patterns/${domain}/${slug}.md`;
      const obj = await env.PATTERNS_BUCKET.get(key);
      if (obj) {
        const md = await obj.text();
        const { meta, body } = parseFrontmatter(md);
        const bodyHtml = markdownToHtml(body);
        const html = renderPage(meta, bodyHtml, slug);
        return new Response(html, {
          status: 200,
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=3600, s-maxage=86400',
            'X-Rendered-By': 'commons-pattern-worker',
          },
        });
      }
    }
  }

  // Fall back to static pages
  return context.next();
}
