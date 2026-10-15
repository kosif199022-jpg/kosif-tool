import test from 'node:test';
import assert from 'node:assert/strict';
import { renderMarkdown } from '../web/md.js';

test('renders headings, lists, tables, code and escapes html', () => {
  const { html, toc } = renderMarkdown('# Title — عنوان\n\nPara with **bold** and `code` and [link](https://x.y).\n\n## Section\n\n- a\n- b <script>\n\n| h1 | h2 |\n|---|---|\n| 1 | 2 |\n\n```js\nconst x = 1 < 2;\n```\n');
  assert.ok(html.includes('<h1 id="title-عنوان-0">'));
  assert.ok(html.includes('<strong>bold</strong>'));
  assert.ok(html.includes('<code>code</code>'));
  assert.ok(html.includes('target="_blank"'));
  assert.ok(html.includes('&lt;script&gt;'));
  assert.ok(html.includes('<table>'));
  assert.ok(html.includes('const x = 1 &lt; 2;'));
  assert.equal(toc.length, 2);
});
