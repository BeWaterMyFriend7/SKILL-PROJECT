---
type: agent-memory-index
dashboard_version: 7
created: "{{timestamp}}"
updated: "{{timestamp}}"
---

# {{name}}

> 仪表盘数据由 Obsidian 社区插件 **Dataview** 渲染，请在设置 → 第三方插件中启用（含 JS 查询）。未启用时，可查看 [任务索引](Tasks/_index.md) 与 [知识索引](Knowledge/_index.md)。
> [[{{name}}.canvas|打开白板入口]]

## 概览

```dataviewjs
const toArray = (value) => {
  if (value == null) return [];
  if (Array.isArray(value)) return value;
  if (typeof value.array === "function") return value.array();
  if (typeof value.values === "function") return Array.from(value.values());
  if (typeof value === "string") return [value];
  try { return Array.from(value); } catch (_) { return [value]; }
};

const normalizeTags = (page) =>
  toArray(page.file?.tags ?? page.tags)
    .map(tag => String(tag).replace(/^#/, "").trim())
    .filter(Boolean);

const card = (icon, label, value) =>
  `<div style="flex:1;min-width:110px;padding:12px 8px;border-radius:10px;background:#f4f6f8;border:1px solid #e3e6ea;text-align:center">
     <div style="font-size:13px;color:#8a919c">${icon} ${label}</div>
     <div style="font-size:26px;font-weight:700;margin-top:2px;color:#2f343d">${value}</div>
   </div>`;

const memoryFolder = String(dv.current()?.file?.path ?? '')
  .split('/')
  .slice(0, -1)
  .join('/');
const pagesIn = (directory) => {
  const path = [memoryFolder, directory].filter(Boolean).join('/');
  return dv.pages(`"${path}"`);
};
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  const directoryPrefix = `${[memoryFolder, directory].filter(Boolean).join('/')}/`;
  return path.startsWith(directoryPrefix) &&
    name !== '_index' &&
    (!type || type === expectedType);
};
const isDailySummary = (page) =>
  pageType(page) === 'agent-daily' ||
  /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name ?? ''));

const tasks = pagesIn('Tasks')
  .where(p => isMemoryRecord(p, 'Tasks', 'agent-task'))
  .array();
const knowledge = pagesIn('Knowledge')
  .where(p => isMemoryRecord(p, 'Knowledge', 'agent-knowledge'))
  .array();
const dailies = pagesIn('Daily')
  .where(isDailySummary)
  .array();
const tagSet = new Set(knowledge.flatMap(normalizeTags));

dv.paragraph(
  '<div style="display:flex;gap:10px;flex-wrap:wrap">' +
    card('📋', '任务数', tasks.length) +
    card('📚', '知识数', knowledge.length) +
    card('📅', '每日总结数', dailies.length) +
    card('🏷️', '标签数', tagSet.size) +
  '</div>'
);
```

```dataviewjs
const memoryFolder = String(dv.current()?.file?.path ?? '')
  .split('/')
  .slice(0, -1)
  .join('/');
const pagesIn = (directory) => {
  const path = [memoryFolder, directory].filter(Boolean).join('/');
  return dv.pages(`"${path}"`);
};
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  const directoryPrefix = `${[memoryFolder, directory].filter(Boolean).join('/')}/`;
  return path.startsWith(directoryPrefix) &&
    name !== '_index' &&
    (!type || type === expectedType);
};
const dailyPages = pagesIn('Daily')
  .where(p =>
    pageType(p) === 'agent-daily' ||
    /^\d{4}-\d{2}-\d{2}$/.test(String(p.file?.name ?? ''))
  )
  .array();
const dailyKey = (page) => {
  if (page.file?.day && typeof page.file.day.toFormat === 'function') {
    return page.file.day.toFormat('yyyy-MM-dd');
  }
  const match = String(page.file?.name ?? '').match(/^(\d{4}-\d{2}-\d{2})$/);
  return match ? match[1] : null;
};
const lines = [];

for (let i = 6; i >= 0; i--) {
  const day = dv.date('today').minus({ days: i });
  const key = day.toFormat('yyyy-MM-dd');
  const count = dailyPages.filter(p => dailyKey(p) === key).length;
  lines.push(`${day.toFormat('MM-dd')} ${'█'.repeat(Math.min(count, 12))} ${count}`);
}

dv.paragraph('**近 7 天每日总结**\n\n' + lines.join('\n'));
```

## 任务与动态

```dataviewjs
const root = dv.container;
root.innerHTML = '';
root.style.display = 'grid';
root.style.gridTemplateColumns = 'minmax(0, 1.1fr) minmax(280px, 0.9fr)';
root.style.gap = '20px';
root.style.alignItems = 'start';

const toArray = (value) => {
  if (value == null) return [];
  if (Array.isArray(value)) return value;
  if (typeof value.array === 'function') return value.array();
  if (typeof value.values === 'function') return Array.from(value.values());
  if (typeof value === 'string') return [value];
  try { return Array.from(value); } catch (_) { return [value]; }
};

const textValue = (value, fallback = '—') => {
  if (value == null || value === '') return fallback;
  return String(value);
};

const formatDate = (value) => {
  if (!value) return '—';
  if (typeof value.toFormat === 'function') return value.toFormat('yyyy-MM-dd HH:mm');
  return textValue(value);
};

const addHeading = (container, text) => {
  const heading = document.createElement('h3');
  heading.textContent = text;
  heading.style.marginTop = '0.8em';
  container.appendChild(heading);
};

const addLink = (container, page, label) => {
  const link = document.createElement('a');
  link.className = 'internal-link';
  link.dataset.href = page.file.path;
  link.textContent = label || page.file.name;
  link.href = '#';
  link.addEventListener('click', (event) => {
    event.preventDefault();
    app.workspace.openLinkText(page.file.path, dv.current().file.path, false);
  });
  container.appendChild(link);
};

const addTable = (container, headers, rows) => {
  const table = document.createElement('table');
  table.className = 'table-view-table';
  table.style.width = '100%';
  table.style.fontSize = '0.9em';

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headers.forEach(header => {
    const cell = document.createElement('th');
    cell.textContent = header;
    headerRow.appendChild(cell);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  rows.forEach(row => {
    const tableRow = document.createElement('tr');
    row.forEach((value, index) => {
      const cell = document.createElement('td');
      if (index === 0 && value?.page) {
        addLink(cell, value.page, value.label);
      } else {
        cell.textContent = textValue(value);
      }
      tableRow.appendChild(cell);
    });
    tbody.appendChild(tableRow);
  });
  table.appendChild(tbody);
  container.appendChild(table);
};

const memoryFolder = String(dv.current()?.file?.path ?? '')
  .split('/')
  .slice(0, -1)
  .join('/');
const pagesIn = (directory) => {
  const path = [memoryFolder, directory].filter(Boolean).join('/');
  return dv.pages(`"${path}"`);
};
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  const directoryPrefix = `${[memoryFolder, directory].filter(Boolean).join('/')}/`;
  return path.startsWith(directoryPrefix) &&
    name !== '_index' &&
    (!type || type === expectedType);
};
const isDailySummary = (page) =>
  pageType(page) === 'agent-daily' ||
  /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name ?? ''));

const taskPages = pagesIn('Tasks')
  .where(p => isMemoryRecord(p, 'Tasks', 'agent-task'))
  .sort(p => p.file.mtime, 'desc')
  .array()
  .slice(0, 15);

const allKnowledgePages = pagesIn('Knowledge')
  .where(p => isMemoryRecord(p, 'Knowledge', 'agent-knowledge'))
  .sort(p => p.file.mtime, 'desc')
  .array();
const knowledgePages = allKnowledgePages.slice(0, 8);

const dailyPages = pagesIn('Daily')
  .where(isDailySummary)
  .sort(p => p.file.name, 'desc')
  .array()
  .slice(0, 8);

const left = document.createElement('div');
const right = document.createElement('div');
root.appendChild(left);
root.appendChild(right);

addHeading(left, '任务表');
addTable(left, ['任务', '状态', '更新时间'], taskPages.map(page => [
  { page, label: page.file.name },
  textValue(page.status, 'active'),
  formatDate(page.file.mtime)
]));

addHeading(right, '最近知识');
addTable(right, ['知识', '更新时间'], knowledgePages.map(page => [
  { page, label: page.file.name },
  formatDate(page.file.mtime)
]));

addHeading(right, '最近总结');
addTable(right, ['日期'], dailyPages.map(page => [
  { page, label: page.file.name }
]));

addHeading(right, '标签统计');
const counts = {};
allKnowledgePages.forEach(page => {
  toArray(page.file?.tags ?? page.tags)
    .map(tag => String(tag).replace(/^#/, '').trim())
    .filter(Boolean)
    .forEach(tag => { counts[tag] = (counts[tag] || 0) + 1; });
});

const topTags = Object.entries(counts).sort((a, b) => b[1] - a[1]);
const tagText = topTags.length
  ? topTags.map(([tag, count]) => `#${tag} × ${count}`).join('　')
  : '（暂无标签）';
const tagParagraph = document.createElement('p');
tagParagraph.textContent = tagText;
right.appendChild(tagParagraph);

const mediaQuery = window.matchMedia('(max-width: 700px)');
const applyResponsiveLayout = () => {
  root.style.gridTemplateColumns = mediaQuery.matches
    ? 'minmax(0, 1fr)'
    : 'minmax(0, 1.1fr) minmax(280px, 0.9fr)';
};
applyResponsiveLayout();
if (mediaQuery.addEventListener) mediaQuery.addEventListener('change', applyResponsiveLayout);
```

---

写入原则：仅显式调用 `agent-offline-mermory` 时写入，所有内容均限制在记忆根目录内。
