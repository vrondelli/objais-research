// Render local SVG sources to PNG for reliable embedding in Markdown.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const panels = JSON.parse(fs.readFileSync(path.join(__dirname, 'panels.json'), 'utf8'));
const html = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Objais annotated formulas</title><style>body{margin:0;background:#f4f7f8;padding:24px}section{margin:0 0 24px;width:900px}svg{display:block;width:100%;height:auto}</style>' +
  panels.map(p => '<section id="' + p.id + '">' + fs.readFileSync(path.join(__dirname, p.id + '.svg'), 'utf8') + '</section>').join('') + '</html>';
fs.writeFileSync(path.join(__dirname, 'preview.html'), html);
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1000, height: 1100 }, deviceScaleFactor: 2 });
    await page.goto(pathToFileURL(path.join(__dirname, 'preview.html')).href);
    const checks = [];
    for (const panel of panels) {
      const clipping = await page.locator('#' + panel.id).evaluate(section => {
        const issues = [];
        for (const group of section.querySelectorAll('.callout')) {
          const box = group.querySelector('rect').getBBox();
          for (const t of group.querySelectorAll('text')) {
            const bounds = t.getBBox();
            if (bounds.x < box.x + 3 || bounds.x + bounds.width > box.x + box.width - 3 || bounds.y + bounds.height > box.y + box.height - 3) issues.push(t.textContent);
          }
        }
        for (const group of section.querySelectorAll('.annotation')) {
          const left = Number(group.dataset.minX), right = Number(group.dataset.maxX);
          for (const t of group.querySelectorAll('text')) {
            const b = t.getBBox();
            if (b.x < left + 2 || b.x + b.width > right - 2) issues.push(t.textContent);
          }
        }
        const svg = section.querySelector('svg');
        const limits = svg.viewBox.baseVal;
        for (const t of svg.querySelectorAll('text')) {
          const b = t.getBBox();
          if (b.x < 4 || b.x + b.width > limits.width - 4 || b.y < 0 || b.y + b.height > limits.height) issues.push('Panel bounds: ' + t.textContent);
        }
        return issues;
      });
      if (clipping.length) throw Error(panel.id + ': label overflow: ' + clipping.join(', '));
      await page.locator('#' + panel.id).screenshot({ path: path.join(__dirname, panel.id + '.png') });
      checks.push({ id: panel.id, label_bounds: 'pass', png: panel.id + '.png' });
    }
    fs.writeFileSync(path.join(__dirname, 'render-validation.json'), JSON.stringify({ status: 'pass', engine: 'Chrome via Playwright; local SVG; no network', panels: checks, native_markdown_preview: 'not inspected' }, null, 2) + '\n');
    console.log(JSON.stringify({ status: 'pass', panels: panels.length }));
  } finally { await browser.close(); }
})().catch(e => { console.error(String(e)); process.exitCode = 1; });
