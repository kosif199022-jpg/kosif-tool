// Minimal, dependency-free Markdown renderer for the repository's own playbooks and briefs.
// Supports: headings, paragraphs, bold/italic/code, links, ordered/unordered lists,
// fenced code blocks, blockquotes, tables, horizontal rules. Everything is HTML-escaped.
function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function slug(s) {
  return s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'section';
}
function inline(s) {
  let out = esc(s);
  out = out.replace(/`([^`]+)`/g, (m, c) => `<code>${c}</code>`);
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<em>$2</em>');
  out = out.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+|[^)\s]+\.md[^)\s]*|#[^)\s]*)\)/g, (m, text, href) => {
    const safe = href.startsWith('http') || href.startsWith('#') ? href : href;
    const ext = href.startsWith('http') ? ' target="_blank" rel="noopener noreferrer"' : '';
    return `<a href="${esc(safe)}"${ext}>${text}</a>`;
  });
  return out;
}
export function renderMarkdown(md, { linkBase = '' } = {}) {
  const lines = md.replace(/\r\n?/g, '\n').split('\n');
  const html = [];
  const toc = [];
  let i = 0;
  const isTableRow = l => /^\s*\|.*\|\s*$/.test(l);
  const isSep = l => /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(l);
  while (i < lines.length) {
    const line = lines[i];
    if (/^\s*$/.test(line)) { i++; continue; }
    const fence = line.match(/^```(\w*)/);
    if (fence) {
      const buf = []; i++;
      while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++;
      html.push(`<pre dir="ltr"><code class="lang-${esc(fence[1] || 'text')}">${esc(buf.join('\n'))}</code></pre>`);
      continue;
    }
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const level = h[1].length; const text = h[2].trim(); const id = slug(text) + '-' + toc.length;
      if (level <= 3) toc.push({ level, text, id });
      html.push(`<h${level} id="${id}">${inline(text)}</h${level}>`);
      i++; continue;
    }
    if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { html.push('<hr>'); i++; continue; }
    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) { buf.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
      html.push(`<blockquote>${renderMarkdown(buf.join('\n')).html}</blockquote>`);
      continue;
    }
    if (isTableRow(line) && i + 1 < lines.length && isSep(lines[i + 1])) {
      const cells = l => l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
      const head = cells(line); i += 2; const rows = [];
      while (i < lines.length && isTableRow(lines[i])) { rows.push(cells(lines[i])); i++; }
      html.push('<div class="table-wrap"><table><thead><tr>' + head.map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>' +
        rows.map(r => '<tr>' + r.map(c => `<td>${inline(c)}</td>`).join('') + '</tr>').join('') + '</tbody></table></div>');
      continue;
    }
    const li = line.match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
    if (li) {
      const ordered = /\d/.test(li[2]); const items = [];
      while (i < lines.length) {
        const m = lines[i].match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
        if (!m) {
          if (/^\s{2,}\S/.test(lines[i]) && items.length) { items[items.length - 1] += ' ' + lines[i].trim(); i++; continue; }
          break;
        }
        items.push(m[3]); i++;
      }
      const tag = ordered ? 'ol' : 'ul';
      html.push(`<${tag}>` + items.map(x => `<li>${inline(x)}</li>`).join('') + `</${tag}>`);
      continue;
    }
    const buf = [];
    while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,6}\s|```|\s*>|\s*([-*+]|\d+[.)])\s)/.test(lines[i]) && !(isTableRow(lines[i]) && i + 1 < lines.length && isSep(lines[i + 1]))) { buf.push(lines[i]); i++; }
    if (buf.length) html.push(`<p>${inline(buf.join(' '))}</p>`);
  }
  return { html: html.join('\n'), toc };
}
