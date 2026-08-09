---
type: agent-memory-index
dashboard_version: 8
created: "{{timestamp}}"
updated: "{{timestamp}}"
---

# {{name}}

> 仪表盘数据由 Obsidian 社区插件 **Dataview** 渲染，请在设置 → 第三方插件中启用（含 JS 查询）。
> [[{{name}}.canvas|打开白板入口]]

```dataviewjs
const ensureStyles = () => {
  if (document.getElementById('agent-memory-dashboard-styles')) return;
  const style = document.createElement('style');
  style.id = 'agent-memory-dashboard-styles';
  style.textContent = `
    .am-block { margin: 0.5rem 0 1.25rem; }
    .am-shell { color: var(--text-normal); }
    .am-hero {
      padding: clamp(1.25rem, 3vw, 2rem);
      border: 1px solid var(--background-modifier-border);
      border-radius: 24px;
      background:
        radial-gradient(circle at 100% 0%, rgba(124, 92, 255, 0.18), transparent 34%),
        linear-gradient(135deg, var(--background-secondary), var(--background-primary));
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.12);
    }
    .am-hero-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
    }
    .am-eyebrow {
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }
    .am-title {
      margin: 0.35rem 0 0;
      color: var(--text-normal);
      font-size: clamp(2rem, 5vw, 3.8rem);
      letter-spacing: -0.045em;
      line-height: 1;
    }
    .am-subtitle {
      max-width: 42rem;
      margin: 0.85rem 0 0;
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .am-clock {
      min-width: 8.5rem;
      padding: 0.8rem 1rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 16px;
      background: var(--background-primary-alt);
      text-align: right;
    }
    .am-clock span, .am-clock small {
      display: block;
      color: var(--text-muted);
      font-size: 0.72rem;
    }
    .am-clock strong {
      display: block;
      margin: 0.15rem 0;
      color: var(--text-normal);
      font-size: 1.8rem;
      letter-spacing: -0.05em;
      line-height: 1;
    }
    .am-search-row {
      display: flex;
      gap: 0.7rem;
      align-items: center;
      margin-top: 1.5rem;
    }
    .am-search {
      display: flex;
      flex: 1;
      align-items: center;
      gap: 0.65rem;
      min-width: 0;
      padding: 0.75rem 1rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 14px;
      background: var(--background-primary);
    }
    .am-search-icon { color: var(--text-muted); font-size: 1.1rem; }
    .am-search input {
      width: 100%;
      border: 0;
      outline: 0;
      background: transparent;
      color: var(--text-normal);
      font: inherit;
    }
    .am-search-hint {
      flex: 0 0 auto;
      color: var(--text-faint);
      font-size: 0.72rem;
      white-space: nowrap;
    }
    .am-button, .am-action {
      cursor: pointer;
      border: 1px solid var(--background-modifier-border);
      border-radius: 12px;
      background: var(--background-primary);
      color: var(--text-normal);
      font: inherit;
      transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
    }
    .am-button:hover, .am-action:hover {
      transform: translateY(-1px);
      border-color: var(--interactive-accent);
      background: var(--background-primary-alt);
    }
    .am-button {
      flex: 0 0 auto;
      padding: 0.78rem 1rem;
      font-weight: 700;
    }
    .am-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      margin-top: 0.9rem;
    }
    .am-action {
      padding: 0.5rem 0.75rem;
      color: var(--text-muted);
      font-size: 0.82rem;
    }
    .am-action-icon { margin-right: 0.35rem; }
    .am-stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.75rem;
      margin-top: 0.85rem;
    }
    .am-stat {
      padding: 1rem 1.05rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 18px;
      background: var(--background-secondary);
    }
    .am-stat-label {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      color: var(--text-muted);
      font-size: 0.8rem;
    }
    .am-stat-value {
      margin-top: 0.2rem;
      color: var(--text-normal);
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.05em;
    }
    .am-stat-note {
      margin-top: 0.15rem;
      color: var(--text-faint);
      font-size: 0.72rem;
    }
    .am-panel-grid {
      display: grid;
      grid-template-columns: minmax(230px, 0.78fr) minmax(0, 1.22fr);
      gap: 0.85rem;
    }
    .am-panel {
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--background-modifier-border);
      border-radius: 18px;
      background: var(--background-secondary);
    }
    .am-panel-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      padding: 0.9rem 1rem;
      border-bottom: 1px solid var(--background-modifier-border);
    }
    .am-panel-title {
      color: var(--text-normal);
      font-size: 0.95rem;
      font-weight: 800;
    }
    .am-panel-meta {
      color: var(--text-muted);
      font-size: 0.72rem;
    }
    .am-panel-body { padding: 1rem; }
    .am-calendar-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.85rem;
    }
    .am-calendar-month { font-size: 1.05rem; font-weight: 800; }
    .am-today-chip {
      padding: 0.25rem 0.5rem;
      border-radius: 999px;
      background: var(--interactive-accent);
      color: var(--text-on-accent);
      font-size: 0.68rem;
      font-weight: 700;
    }
    .am-calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 0.25rem;
    }
    .am-calendar-weekday {
      padding: 0.2rem 0;
      color: var(--text-faint);
      font-size: 0.68rem;
      text-align: center;
    }
    .am-calendar-day {
      position: relative;
      min-height: 2rem;
      padding: 0.45rem 0.2rem;
      border: 1px solid transparent;
      border-radius: 9px;
      color: var(--text-muted);
      font-size: 0.78rem;
      text-align: center;
    }
    .am-calendar-day.is-today {
      border-color: var(--interactive-accent);
      color: var(--text-normal);
      font-weight: 800;
    }
    .am-calendar-day.has-record { color: var(--text-normal); }
    .am-calendar-dot {
      position: absolute;
      right: 0.25rem;
      bottom: 0.22rem;
      width: 0.28rem;
      height: 0.28rem;
      border-radius: 50%;
      background: var(--interactive-accent);
    }
    .am-recent-list, .am-link-list { display: grid; gap: 0.45rem; }
    .am-recent-item, .am-link-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      min-width: 0;
      padding: 0.65rem 0.7rem;
      border-radius: 10px;
      color: var(--text-normal);
      text-decoration: none;
    }
    .am-recent-item:hover, .am-link-item:hover {
      background: var(--background-primary-alt);
      text-decoration: none;
    }
    .am-item-main {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .am-item-kind, .am-item-time {
      flex: 0 0 auto;
      color: var(--text-faint);
      font-size: 0.7rem;
    }
    .am-item-kind { color: var(--interactive-accent); }
    .am-main-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr);
      gap: 0.85rem;
    }
    .am-table-wrap { overflow-x: auto; }
    .am-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }
    .am-table th {
      padding: 0.65rem 0.75rem;
      color: var(--text-faint);
      font-size: 0.7rem;
      font-weight: 700;
      text-align: left;
      white-space: nowrap;
    }
    .am-table td {
      padding: 0.7rem 0.75rem;
      border-top: 1px solid var(--background-modifier-border);
      vertical-align: middle;
    }
    .am-table a { color: var(--text-normal); text-decoration: none; }
    .am-table a:hover { color: var(--interactive-accent); }
    .am-task-name {
      display: block;
      max-width: 28rem;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .am-status {
      display: inline-block;
      padding: 0.2rem 0.45rem;
      border-radius: 999px;
      background: var(--background-primary-alt);
      color: var(--text-muted);
      font-size: 0.68rem;
      white-space: nowrap;
    }
    .am-side-stack { display: grid; gap: 0.85rem; align-content: start; }
    .am-tag-cloud { display: flex; flex-wrap: wrap; gap: 0.45rem; }
    .am-tag {
      padding: 0.35rem 0.55rem;
      border-radius: 999px;
      background: var(--background-primary-alt);
      color: var(--text-muted);
      font-size: 0.72rem;
    }
    .am-empty {
      padding: 1.2rem 0.75rem;
      color: var(--text-faint);
      font-size: 0.82rem;
      text-align: center;
    }
    .am-quick-panel { grid-column: 1 / -1; }
    .am-quick-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.6rem;
    }
    .am-quick-action {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.8rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 13px;
      background: var(--background-primary);
      color: var(--text-normal);
      cursor: pointer;
      font: inherit;
      text-align: left;
    }
    .am-quick-action:hover {
      border-color: var(--interactive-accent);
      background: var(--background-primary-alt);
    }
    .am-quick-icon { font-size: 1.1rem; }
    .am-quick-label { font-size: 0.8rem; font-weight: 700; }
    .am-quick-note { color: var(--text-faint); font-size: 0.68rem; }
    @media (max-width: 800px) {
      .am-hero-top, .am-search-row { flex-direction: column; align-items: stretch; }
      .am-clock { text-align: left; }
      .am-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .am-panel-grid, .am-main-grid { grid-template-columns: 1fr; }
      .am-quick-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 480px) {
      .am-stats, .am-quick-grid { grid-template-columns: 1fr; }
      .am-search-hint { display: none; }
    }
  `;
  document.head.appendChild(style);
};

const toArray = (value) => {
  if (value == null) return [];
  if (Array.isArray(value)) return value;
  if (typeof value.array === 'function') return value.array();
  if (typeof value.values === 'function') return Array.from(value.values());
  if (typeof value === 'string') return [value];
  try { return Array.from(value); } catch (_) { return [value]; }
};

const escapeHtml = (value) =>
  String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

const normalizeTags = (page) =>
  toArray(page.file?.tags ?? page.tags)
    .map(tag => String(tag).replace(/^#/, '').trim())
    .filter(Boolean);

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
  .where(page => isMemoryRecord(page, 'Tasks', 'agent-task'))
  .sort(page => page.file.mtime, 'desc')
  .array();
const knowledge = pagesIn('Knowledge')
  .where(page => isMemoryRecord(page, 'Knowledge', 'agent-knowledge'))
  .sort(page => page.file.mtime, 'desc')
  .array();
const dailies = pagesIn('Daily')
  .where(isDailySummary)
  .sort(page => page.file.name, 'desc')
  .array();
const tagSet = new Set(knowledge.flatMap(normalizeTags));
const now = new Date();
const currentTitle = String(dv.current()?.file?.name ?? '{{name}}');
const indexPath = (directory) =>
  [memoryFolder, directory, '_index.md'].filter(Boolean).join('/');
const dailyPath = [memoryFolder, 'Daily', 'Daily.md'].filter(Boolean).join('/');
const canvasPath = [memoryFolder, `${currentTitle}.canvas`].filter(Boolean).join('/');

ensureStyles();
const root = dv.container;
root.className = 'am-block';
root.innerHTML = `
  <div class="am-shell">
    <section class="am-hero">
      <div class="am-hero-top">
        <div>
          <div class="am-eyebrow">LOCAL MEMORY · OBSIDIAN</div>
          <h1 class="am-title">🏠 ${escapeHtml(currentTitle)}</h1>
          <p class="am-subtitle">任务、知识和每日总结，都从这里开始。</p>
        </div>
        <div class="am-clock">
          <span>现在</span>
          <strong>${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}</strong>
          <small>${now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}</small>
        </div>
      </div>
      <div class="am-search-row">
        <label class="am-search">
          <span class="am-search-icon">⌕</span>
          <input data-am-search type="search" placeholder="搜索首页中的任务、知识和总结">
          <span class="am-search-hint">实时过滤</span>
        </label>
        <button class="am-button" data-am-path="${escapeHtml(dailyPath)}">＋ 手动记录</button>
      </div>
      <div class="am-actions">
        <button class="am-action" data-am-path="${escapeHtml(indexPath('Tasks'))}"><span class="am-action-icon">☑</span>任务表</button>
        <button class="am-action" data-am-path="${escapeHtml(indexPath('Knowledge'))}"><span class="am-action-icon">◇</span>知识索引</button>
        <button class="am-action" data-am-path="${escapeHtml(dailyPath)}"><span class="am-action-icon">◷</span>每日总结</button>
        <button class="am-action" data-am-path="${escapeHtml(canvasPath)}"><span class="am-action-icon">▦</span>打开白板</button>
      </div>
    </section>
    <section class="am-stats">
      <div class="am-stat"><div class="am-stat-label">📋 任务数</div><div class="am-stat-value">${tasks.length}</div><div class="am-stat-note">全部任务记录</div></div>
      <div class="am-stat"><div class="am-stat-label">📚 知识数</div><div class="am-stat-value">${knowledge.length}</div><div class="am-stat-note">可复用知识记录</div></div>
      <div class="am-stat"><div class="am-stat-label">📅 每日总结数</div><div class="am-stat-value">${dailies.length}</div><div class="am-stat-note">按日期识别的总结</div></div>
      <div class="am-stat"><div class="am-stat-label">🏷️ 标签数</div><div class="am-stat-value">${tagSet.size}</div><div class="am-stat-note">知识中的唯一标签</div></div>
    </section>
  </div>
`;

const bindLinks = (container) => {
  container.querySelectorAll('[data-am-path]').forEach(element => {
    element.addEventListener('click', event => {
      event.preventDefault();
      app.workspace.openLinkText(element.dataset.amPath, dv.current().file.path, false);
    });
  });
};
bindLinks(root);

const searchInput = root.querySelector('[data-am-search]');
searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLowerCase();
  document.querySelectorAll('.am-filterable').forEach(element => {
    element.style.display = !query || element.textContent.toLowerCase().includes(query) ? '' : 'none';
  });
});
```

```dataviewjs
const ensureStyles = () => {
  if (document.getElementById('agent-memory-dashboard-styles')) return;
  const style = document.createElement('style');
  style.id = 'agent-memory-dashboard-styles';
  style.textContent = '.am-block{margin:.5rem 0 1.25rem}.am-panel-grid{display:grid;grid-template-columns:minmax(230px,.78fr) minmax(0,1.22fr);gap:.85rem}.am-panel{min-width:0;overflow:hidden;border:1px solid var(--background-modifier-border);border-radius:18px;background:var(--background-secondary)}.am-panel-header{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.9rem 1rem;border-bottom:1px solid var(--background-modifier-border)}.am-panel-title{color:var(--text-normal);font-size:.95rem;font-weight:800}.am-panel-meta{color:var(--text-muted);font-size:.72rem}.am-panel-body{padding:1rem}.am-calendar-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:.85rem}.am-calendar-month{font-size:1.05rem;font-weight:800}.am-today-chip{padding:.25rem .5rem;border-radius:999px;background:var(--interactive-accent);color:var(--text-on-accent);font-size:.68rem;font-weight:700}.am-calendar-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:.25rem}.am-calendar-weekday{padding:.2rem 0;color:var(--text-faint);font-size:.68rem;text-align:center}.am-calendar-day{position:relative;min-height:2rem;padding:.45rem .2rem;border:1px solid transparent;border-radius:9px;color:var(--text-muted);font-size:.78rem;text-align:center}.am-calendar-day.is-today{border-color:var(--interactive-accent);color:var(--text-normal);font-weight:800}.am-calendar-day.has-record{color:var(--text-normal)}.am-calendar-dot{position:absolute;right:.25rem;bottom:.22rem;width:.28rem;height:.28rem;border-radius:50%;background:var(--interactive-accent)}.am-recent-list{display:grid;gap:.45rem}.am-recent-item{display:flex;align-items:center;justify-content:space-between;gap:.75rem;min-width:0;padding:.65rem .7rem;border-radius:10px;color:var(--text-normal);text-decoration:none}.am-recent-item:hover{background:var(--background-primary-alt);text-decoration:none}.am-item-main{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.am-item-kind,.am-item-time{flex:0 0 auto;color:var(--text-faint);font-size:.7rem}.am-item-kind{color:var(--interactive-accent)}.am-empty{padding:1.2rem .75rem;color:var(--text-faint);font-size:.82rem;text-align:center}@media(max-width:800px){.am-panel-grid{grid-template-columns:1fr}}';
  document.head.appendChild(style);
};

const memoryFolder = String(dv.current()?.file?.path ?? '').split('/').slice(0, -1).join('/');
const pagesIn = (directory) => dv.pages(`"${[memoryFolder, directory].filter(Boolean).join('/')}"`);
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  const prefix = `${[memoryFolder, directory].filter(Boolean).join('/')}/`;
  return path.startsWith(prefix) && name !== '_index' && (!type || type === expectedType);
};
const isDailySummary = (page) =>
  pageType(page) === 'agent-daily' ||
  /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name ?? ''));
const escapeHtml = (value) => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
const millis = (page) => {
  const value = page.file?.mtime;
  if (value && typeof value.toMillis === 'function') return value.toMillis();
  const parsed = Date.parse(String(value ?? ''));
  return Number.isNaN(parsed) ? 0 : parsed;
};
const formatDate = (value) => {
  if (value && typeof value.toFormat === 'function') return value.toFormat('MM-dd HH:mm');
  const parsed = new Date(String(value ?? ''));
  return Number.isNaN(parsed.getTime()) ? '—' : parsed.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
};
const dailyKey = (page) => {
  if (page.file?.day && typeof page.file.day.toFormat === 'function') return page.file.day.toFormat('yyyy-MM-dd');
  const match = String(page.file?.name ?? '').match(/^(\d{4}-\d{2}-\d{2})$/);
  return match ? match[1] : null;
};

const tasks = pagesIn('Tasks').where(page => isMemoryRecord(page, 'Tasks', 'agent-task')).array();
const knowledge = pagesIn('Knowledge').where(page => isMemoryRecord(page, 'Knowledge', 'agent-knowledge')).array();
const dailies = pagesIn('Daily').where(isDailySummary).array();
const today = new Date();
const year = today.getFullYear();
const month = today.getMonth();
const monthName = `${year}年${month + 1}月`;
const todayKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
const dailyCounts = {};
dailies.forEach(page => {
  const key = dailyKey(page);
  if (key) dailyCounts[key] = (dailyCounts[key] || 0) + 1;
});
const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
const firstOffset = new Date(year, month, 1).getDay();
const daysInMonth = new Date(year, month + 1, 0).getDate();
const calendarCells = weekdays.map(day => `<div class="am-calendar-weekday">${day}</div>`);
for (let i = 0; i < firstOffset; i++) calendarCells.push('<div></div>');
for (let day = 1; day <= daysInMonth; day++) {
  const key = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  const count = dailyCounts[key] || 0;
  const classes = ['am-calendar-day'];
  if (key === todayKey) classes.push('is-today');
  if (count) classes.push('has-record');
  calendarCells.push(`<div class="${classes.join(' ')}">${day}${count ? '<span class="am-calendar-dot"></span>' : ''}</div>`);
}

const recent = [
  ...tasks.map(page => ({ page, kind: '任务' })),
  ...knowledge.map(page => ({ page, kind: '知识' })),
  ...dailies.map(page => ({ page, kind: '总结' }))
].sort((a, b) => millis(b.page) - millis(a.page)).slice(0, 8);
const currentPath = dv.current().file.path;
const root = dv.container;
ensureStyles();
root.className = 'am-block';
root.innerHTML = `
  <div class="am-panel-grid">
    <section class="am-panel">
      <div class="am-panel-header"><span class="am-panel-title">本月日历</span><span class="am-panel-meta">${dailies.length} 条总结</span></div>
      <div class="am-panel-body">
        <div class="am-calendar-head"><span class="am-calendar-month">${monthName}</span><span class="am-today-chip">今天</span></div>
        <div class="am-calendar-grid">${calendarCells.join('')}</div>
      </div>
    </section>
    <section class="am-panel">
      <div class="am-panel-header"><span class="am-panel-title">最近更新</span><span class="am-panel-meta">按更新时间</span></div>
      <div class="am-panel-body">
        <div class="am-recent-list">
          ${recent.length ? recent.map(({ page, kind }) => `
            <a href="#" class="am-recent-item am-filterable" data-am-path="${escapeHtml(page.file.path)}">
              <span class="am-item-main">${escapeHtml(page.file.name)}</span>
              <span class="am-item-kind">${kind}</span>
              <span class="am-item-time">${formatDate(page.file.mtime)}</span>
            </a>
          `).join('') : '<div class="am-empty">还没有可展示的记录</div>'}
        </div>
      </div>
    </section>
  </div>
`;
root.querySelectorAll('[data-am-path]').forEach(element => {
  element.addEventListener('click', event => {
    event.preventDefault();
    app.workspace.openLinkText(element.dataset.amPath, currentPath, false);
  });
});
```

```dataviewjs
const ensureStyles = () => {
  if (document.getElementById('agent-memory-dashboard-styles')) return;
  const style = document.createElement('style');
  style.id = 'agent-memory-dashboard-styles';
  style.textContent = '.am-block{margin:.5rem 0 1.25rem}.am-main-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(260px,.85fr);gap:.85rem}.am-panel{min-width:0;overflow:hidden;border:1px solid var(--background-modifier-border);border-radius:18px;background:var(--background-secondary)}.am-panel-header{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.9rem 1rem;border-bottom:1px solid var(--background-modifier-border)}.am-panel-title{color:var(--text-normal);font-size:.95rem;font-weight:800}.am-panel-meta{color:var(--text-muted);font-size:.72rem}.am-panel-body{padding:1rem}.am-table-wrap{overflow-x:auto}.am-table{width:100%;border-collapse:collapse;font-size:.82rem}.am-table th{padding:.65rem .75rem;color:var(--text-faint);font-size:.7rem;font-weight:700;text-align:left;white-space:nowrap}.am-table td{padding:.7rem .75rem;border-top:1px solid var(--background-modifier-border);vertical-align:middle}.am-table a{color:var(--text-normal);text-decoration:none}.am-table a:hover{color:var(--interactive-accent)}.am-task-name{display:block;max-width:28rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.am-status{display:inline-block;padding:.2rem .45rem;border-radius:999px;background:var(--background-primary-alt);color:var(--text-muted);font-size:.68rem;white-space:nowrap}.am-side-stack{display:grid;gap:.85rem;align-content:start}.am-link-list{display:grid;gap:.45rem}.am-link-item{display:flex;align-items:center;justify-content:space-between;gap:.75rem;min-width:0;padding:.65rem .7rem;border-radius:10px;color:var(--text-normal);text-decoration:none}.am-link-item:hover{background:var(--background-primary-alt);text-decoration:none}.am-item-main{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.am-item-time{flex:0 0 auto;color:var(--text-faint);font-size:.7rem}.am-tag-cloud{display:flex;flex-wrap:wrap;gap:.45rem}.am-tag{padding:.35rem .55rem;border-radius:999px;background:var(--background-primary-alt);color:var(--text-muted);font-size:.72rem}.am-empty{padding:1.2rem .75rem;color:var(--text-faint);font-size:.82rem;text-align:center}.am-quick-panel{grid-column:1 / -1}.am-quick-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.6rem}.am-quick-action{display:flex;align-items:center;gap:.6rem;padding:.8rem;border:1px solid var(--background-modifier-border);border-radius:13px;background:var(--background-primary);color:var(--text-normal);cursor:pointer;font:inherit;text-align:left}.am-quick-action:hover{border-color:var(--interactive-accent);background:var(--background-primary-alt)}.am-quick-icon{font-size:1.1rem}.am-quick-label{font-size:.8rem;font-weight:700}.am-quick-note{color:var(--text-faint);font-size:.68rem}@media(max-width:800px){.am-main-grid{grid-template-columns:1fr}.am-quick-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:480px){.am-quick-grid{grid-template-columns:1fr}}';
  document.head.appendChild(style);
};

const toArray = (value) => {
  if (value == null) return [];
  if (Array.isArray(value)) return value;
  if (typeof value.array === 'function') return value.array();
  if (typeof value.values === 'function') return Array.from(value.values());
  if (typeof value === 'string') return [value];
  try { return Array.from(value); } catch (_) { return [value]; }
};
const escapeHtml = (value) => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
const memoryFolder = String(dv.current()?.file?.path ?? '').split('/').slice(0, -1).join('/');
const pagesIn = (directory) => dv.pages(`"${[memoryFolder, directory].filter(Boolean).join('/')}"`);
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  const prefix = `${[memoryFolder, directory].filter(Boolean).join('/')}/`;
  return path.startsWith(prefix) && name !== '_index' && (!type || type === expectedType);
};
const formatDate = (value) => {
  if (value && typeof value.toFormat === 'function') return value.toFormat('MM-dd HH:mm');
  const parsed = new Date(String(value ?? ''));
  return Number.isNaN(parsed.getTime()) ? '—' : parsed.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
};
const statusText = (value) => {
  const status = String(value ?? 'active').toLowerCase();
  return { active: '进行中', completed: '已完成', done: '已完成', blocked: '已阻塞', paused: '已暂停' }[status] || String(value || '进行中');
};
const tasks = pagesIn('Tasks').where(page => isMemoryRecord(page, 'Tasks', 'agent-task')).sort(page => page.file.mtime, 'desc').array();
const knowledge = pagesIn('Knowledge').where(page => isMemoryRecord(page, 'Knowledge', 'agent-knowledge')).sort(page => page.file.mtime, 'desc').array().slice(0, 8);
const dailies = pagesIn('Daily').where(page => pageType(page) === 'agent-daily' || /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name ?? ''))).sort(page => page.file.name, 'desc').array().slice(0, 8);
const allKnowledge = pagesIn('Knowledge').where(page => isMemoryRecord(page, 'Knowledge', 'agent-knowledge')).array();
const counts = {};
allKnowledge.forEach(page => toArray(page.file?.tags ?? page.tags).map(tag => String(tag).replace(/^#/, '').trim()).filter(Boolean).forEach(tag => { counts[tag] = (counts[tag] || 0) + 1; }));
const tags = Object.entries(counts).sort((a, b) => b[1] - a[1]);
const currentPath = dv.current().file.path;
const indexPath = (directory) => [memoryFolder, directory, '_index.md'].filter(Boolean).join('/');
const dailyPath = [memoryFolder, 'Daily', 'Daily.md'].filter(Boolean).join('/');
const canvasPath = [memoryFolder, `${dv.current().file.name}.canvas`].filter(Boolean).join('/');
const empty = '<div class="am-empty">暂无记录</div>';
const linkList = (items, kind) => items.length ? items.map(page => `<a href="#" class="am-link-item am-filterable" data-am-path="${escapeHtml(page.file.path)}"><span class="am-item-main">${escapeHtml(page.file.name)}</span><span class="am-item-time">${kind ? kind : formatDate(page.file.mtime)}</span></a>`).join('') : empty;
const root = dv.container;
ensureStyles();
root.className = 'am-block';
root.innerHTML = `
  <div class="am-main-grid">
    <section class="am-panel">
      <div class="am-panel-header"><span class="am-panel-title">任务表</span><span class="am-panel-meta">${tasks.length} 条任务</span></div>
      <div class="am-table-wrap">
        ${tasks.length ? `
          <table class="am-table">
            <thead><tr><th>任务</th><th>状态</th><th>更新</th></tr></thead>
            <tbody>
              ${tasks.map(page => `
                <tr class="am-filterable">
                  <td><a href="#" data-am-path="${escapeHtml(page.file.path)}" class="am-task-name">${escapeHtml(page.file.name)}</a></td>
                  <td><span class="am-status">${escapeHtml(statusText(page.status))}</span></td>
                  <td>${formatDate(page.file.mtime)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        ` : empty}
      </div>
    </section>
    <div class="am-side-stack">
      <section class="am-panel">
        <div class="am-panel-header"><span class="am-panel-title">最近知识</span><span class="am-panel-meta">${knowledge.length} 条</span></div>
        <div class="am-panel-body"><div class="am-link-list">${linkList(knowledge)}</div></div>
      </section>
      <section class="am-panel">
        <div class="am-panel-header"><span class="am-panel-title">最近总结</span><span class="am-panel-meta">${dailies.length} 条</span></div>
        <div class="am-panel-body"><div class="am-link-list">${linkList(dailies, '每日总结')}</div></div>
      </section>
      <section class="am-panel">
        <div class="am-panel-header"><span class="am-panel-title">标签统计</span><span class="am-panel-meta">${tags.length} 个标签</span></div>
        <div class="am-panel-body">
          ${tags.length ? `<div class="am-tag-cloud">${tags.map(([tag, count]) => `<span class="am-tag">#${escapeHtml(tag)} · ${count}</span>`).join('')}</div>` : empty}
        </div>
      </section>
    </div>
    <section class="am-panel am-quick-panel">
      <div class="am-panel-header"><span class="am-panel-title">快捷入口</span><span class="am-panel-meta">手动触发，按需打开</span></div>
      <div class="am-panel-body">
        <div class="am-quick-grid">
          <button class="am-quick-action" data-am-path="${escapeHtml(indexPath('Tasks'))}"><span class="am-quick-icon">☑</span><span><span class="am-quick-label">任务表</span><br><span class="am-quick-note">查看全部任务</span></span></button>
          <button class="am-quick-action" data-am-path="${escapeHtml(indexPath('Knowledge'))}"><span class="am-quick-icon">◇</span><span><span class="am-quick-label">知识索引</span><br><span class="am-quick-note">浏览可复用经验</span></span></button>
          <button class="am-quick-action" data-am-path="${escapeHtml(dailyPath)}"><span class="am-quick-icon">◷</span><span><span class="am-quick-label">每日总结</span><br><span class="am-quick-note">手动记录今天</span></span></button>
          <button class="am-quick-action" data-am-path="${escapeHtml(canvasPath)}"><span class="am-quick-icon">▦</span><span><span class="am-quick-label">白板入口</span><br><span class="am-quick-note">关系与结构视图</span></span></button>
        </div>
      </div>
    </section>
  </div>
`;
root.querySelectorAll('[data-am-path]').forEach(element => {
  element.addEventListener('click', event => {
    event.preventDefault();
    app.workspace.openLinkText(element.dataset.amPath, currentPath, false);
  });
});
```

---

写入原则：仅显式调用 `agent-offline-mermory` 时写入，所有内容均限制在记忆根目录内。
