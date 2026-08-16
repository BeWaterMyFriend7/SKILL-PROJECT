---
type: agent-memory-index
dashboard_version: 9
created: "{{timestamp}}"
updated: "{{timestamp}}"
---

# {{name}}

> 仪表盘数据由 Obsidian 社区插件 **Dataview** 渲染，请在设置 → 第三方插件中启用 Dataview 和 JavaScript 查询。

```dataviewjs
const STYLE_ID = 'agent-memory-dashboard-styles-v9';
document.getElementById('agent-memory-dashboard-styles')?.remove();

const ensureStyles = () => {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement('style');
  style.id = STYLE_ID;
  style.textContent = `
    .am-dashboard {
      max-width: 1180px;
      margin: 0.5rem auto 1.5rem;
      color: var(--text-normal);
    }
    .am-hero {
      padding: clamp(1.2rem, 3vw, 2rem);
      border: 1px solid var(--background-modifier-border);
      border-radius: 24px;
      background: radial-gradient(circle at 100% 0%, rgba(124, 92, 255, 0.18), transparent 34%), linear-gradient(135deg, var(--background-secondary), var(--background-primary));
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
      overflow: visible;
      color: var(--text-normal);
      font-size: clamp(2rem, 5vw, 3.8rem);
      letter-spacing: -0.045em;
      line-height: 1.05;
      white-space: normal;
    }
    .am-subtitle {
      max-width: 42rem;
      margin: 0.85rem 0 0;
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .am-clock {
      min-width: 9rem;
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
    .am-stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.75rem;
      margin-top: 1.25rem;
    }
    .am-stat {
      min-width: 0;
      padding: 0.9rem 1rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 17px;
      background: var(--background-primary);
    }
    .am-stat-label {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      color: var(--text-muted);
      font-size: 0.78rem;
      line-height: 1.35;
      white-space: normal;
    }
    .am-stat-value {
      margin-top: 0.2rem;
      color: var(--text-normal);
      font-size: 1.9rem;
      font-weight: 800;
      letter-spacing: -0.05em;
    }
    .am-stat-note {
      margin-top: 0.1rem;
      color: var(--text-faint);
      font-size: 0.68rem;
      line-height: 1.35;
    }
    .am-search-row {
      display: flex;
      align-items: center;
      gap: 0.7rem;
      margin-top: 0.9rem;
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
      min-width: 0;
      border: 0;
      outline: 0;
      background: transparent;
      color: var(--text-normal);
      font: inherit;
    }
    .am-search-hint {
      flex: 0 0 auto;
      color: var(--text-faint);
      font-size: 0.7rem;
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
      white-space: nowrap;
    }
    .am-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      margin-top: 0.8rem;
    }
    .am-action {
      padding: 0.5rem 0.75rem;
      color: var(--text-muted);
      font-size: 0.82rem;
    }
    .am-action-icon { margin-right: 0.35rem; }
    .am-main-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
      gap: 0.85rem;
      margin-top: 0.85rem;
      align-items: start;
    }
    .am-side-stack { display: grid; gap: 0.85rem; align-content: start; min-width: 0; }
    .am-panel {
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--background-modifier-border);
      border-radius: 18px;
      background: var(--background-secondary);
    }
    .am-panel-header {
      display: block;
      min-width: 0;
      padding: 0.9rem 1rem 0.8rem;
      border-bottom: 1px solid var(--background-modifier-border);
    }
    .am-panel-title {
      display: block !important;
      width: auto !important;
      min-width: 0;
      overflow: visible !important;
      color: var(--text-normal);
      font-size: 0.98rem;
      font-weight: 800;
      line-height: 1.35;
      text-overflow: clip !important;
      white-space: normal !important;
      word-break: keep-all;
    }
    .am-panel-meta {
      display: block;
      margin-top: 0.18rem;
      overflow: visible;
      color: var(--text-muted);
      font-size: 0.7rem;
      line-height: 1.35;
      white-space: normal;
    }
    .am-panel-body { padding: 0.85rem 1rem 1rem; }
    .am-table-wrap { overflow-x: auto; }
    .am-table {
      width: 100%;
      min-width: 520px;
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
      max-width: 31rem;
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
    .am-link-list { display: grid; gap: 0.4rem; }
    .am-link-item {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: center;
      gap: 0.65rem;
      min-width: 0;
      padding: 0.62rem 0.68rem;
      border-radius: 10px;
      color: var(--text-normal);
      text-decoration: none;
    }
    .am-link-item:hover { background: var(--background-primary-alt); text-decoration: none; }
    .am-item-main {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .am-item-kind, .am-item-time {
      color: var(--text-faint);
      font-size: 0.68rem;
      white-space: nowrap;
    }
    .am-item-kind { color: var(--interactive-accent); }
    .am-tag-cloud { display: flex; flex-wrap: wrap; gap: 0.42rem; }
    .am-tag {
      padding: 0.34rem 0.52rem;
      border-radius: 999px;
      background: var(--background-primary-alt);
      color: var(--text-muted);
      font-size: 0.7rem;
    }
    .am-empty {
      padding: 1.1rem 0.75rem;
      color: var(--text-faint);
      font-size: 0.8rem;
      text-align: center;
    }
    .am-modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 9999;
      display: grid;
      place-items: center;
      padding: 1rem;
      background: rgba(0, 0, 0, 0.52);
      backdrop-filter: blur(4px);
    }
    .am-modal {
      width: min(520px, calc(100vw - 2rem));
      padding: 1.1rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 18px;
      background: var(--background-primary);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
    }
    .am-modal-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
      margin-bottom: 0.85rem;
    }
    .am-modal-title { margin: 0; font-size: 1.08rem; line-height: 1.35; }
    .am-modal-note { margin: 0.25rem 0 0; color: var(--text-muted); font-size: 0.76rem; line-height: 1.5; }
    .am-modal-close {
      cursor: pointer;
      border: 0;
      background: transparent;
      color: var(--text-muted);
      font-size: 1.2rem;
    }
    .am-capture-options { display: grid; gap: 0.58rem; }
    .am-capture-option {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 0.75rem;
      align-items: center;
      width: 100%;
      padding: 0.78rem 0.85rem;
      border: 1px solid var(--background-modifier-border);
      border-radius: 13px;
      background: var(--background-secondary);
      color: var(--text-normal);
      cursor: pointer;
      font: inherit;
      text-align: left;
    }
    .am-capture-option:hover { border-color: var(--interactive-accent); background: var(--background-primary-alt); }
    .am-capture-icon { font-size: 1.25rem; }
    .am-capture-label { display: block; font-size: 0.86rem; font-weight: 800; }
    .am-capture-desc { display: block; margin-top: 0.12rem; color: var(--text-muted); font-size: 0.72rem; line-height: 1.4; }
    .am-copy-status {
      min-height: 1.2rem;
      margin: 0.8rem 0 0;
      color: var(--interactive-accent);
      font-size: 0.74rem;
    }
    @media (max-width: 800px) {
      .am-hero-top, .am-search-row { flex-direction: column; align-items: stretch; }
      .am-clock { text-align: left; }
      .am-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .am-main-grid { grid-template-columns: minmax(0, 1fr); }
    }
    @media (max-width: 480px) {
      .am-stats { grid-template-columns: minmax(0, 1fr); }
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
const escapeHtml = (value) => String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#039;');

const currentPath = String(dv.current()?.file?.path ?? '');
const memoryFolder = currentPath.split('/').slice(0, -1).join('/');
const pathInMemory = (...parts) => [memoryFolder, ...parts].filter(Boolean).join('/');
const pagesIn = (directory) => dv.pages(`"${pathInMemory(directory)}"`);
const pageType = (page) => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page, directory, expectedType) => {
  const path = String(page.file?.path ?? '');
  const name = String(page.file?.name ?? '');
  const type = pageType(page);
  return path.startsWith(`${pathInMemory(directory)}/`) && name !== '_index' && (!type || type === expectedType);
};
const isDailySummary = (page) => {
  if (!isMemoryRecord(page, 'Daily', 'agent-daily')) return false;
  return pageType(page) === 'agent-daily' || /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name ?? ''));
};
const normalizeTags = (page) => toArray(page.file?.tags ?? page.tags)
  .map(tag => String(tag).replace(/^#/, '').trim())
  .filter(Boolean);
const millis = (page) => {
  const value = page.file?.mtime;
  if (value && typeof value.toMillis === 'function') return value.toMillis();
  const parsed = Date.parse(String(value ?? ''));
  return Number.isNaN(parsed) ? 0 : parsed;
};
const formatDate = (value) => {
  if (value && typeof value.toFormat === 'function') return value.toFormat('MM-dd HH:mm');
  const parsed = new Date(String(value ?? ''));
  return Number.isNaN(parsed.getTime()) ? '—' : parsed.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
};
const displayName = (page) => String(page.file?.name ?? '')
  .replace(/^\d{4}-\d{2}-\d{2}-\d{6}-/, '')
  .replace(/^\d{4}-\d{2}-\d{2}-/, '');
const statusText = (value) => {
  const status = String(value ?? 'active').toLowerCase();
  return { active: '进行中', completed: '已完成', done: '已完成', blocked: '已阻塞', paused: '已暂停' }[status] || String(value || '进行中');
};

const tasks = pagesIn('Tasks').where(page => isMemoryRecord(page, 'Tasks', 'agent-task')).array().sort((a, b) => millis(b) - millis(a));
const knowledge = pagesIn('Knowledge').where(page => isMemoryRecord(page, 'Knowledge', 'agent-knowledge')).array().sort((a, b) => millis(b) - millis(a));
const dailies = pagesIn('Daily').where(isDailySummary).array().sort((a, b) => millis(b) - millis(a));
const allRecords = [
  ...tasks.map(page => ({ page, kind: '任务' })),
  ...knowledge.map(page => ({ page, kind: '知识' })),
  ...dailies.map(page => ({ page, kind: '总结' })),
].sort((a, b) => millis(b.page) - millis(a.page));
const tagCounts = {};
knowledge.forEach(page => normalizeTags(page).forEach(tag => { tagCounts[tag] = (tagCounts[tag] || 0) + 1; }));
const tags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
const now = new Date();
const currentTitle = String(dv.current()?.file?.name ?? '{{name}}');
const indexPath = (directory) => pathInMemory(directory, '_index.md');
const empty = '<div class="am-empty">暂无记录</div>';
const linkList = (items) => items.length ? items.map(({ page, kind }) => `
  <a href="#" class="am-link-item am-filterable" data-am-path="${escapeHtml(page.file.path)}">
    <span class="am-item-main">${escapeHtml(displayName(page))}</span>
    <span class="${kind ? 'am-item-kind' : 'am-item-time'}">${escapeHtml(kind || formatDate(page.file.mtime))}</span>
  </a>`).join('') : empty;

const captureOptions = [
  { type: 'knowledge', icon: '◇', label: '知识', description: '记录可复用的经验、原因、方案和验证。', prompt: '$agent-offline-mermory 记录一条知识：请补充场景、问题与原因、解决方案与验证、注意事项。' },
  { type: 'task', icon: '☑', label: '任务', description: '记录目标、当前进度、下一步和阻塞。', prompt: '$agent-offline-mermory 记录一个任务：请补充目标、当前进度、下一步、阻塞与风险。' },
  { type: 'daily', icon: '◷', label: '总结', description: '记录今天的完成、问题和明日计划。', prompt: '$agent-offline-mermory 记录今天的每日总结：请补充完成、问题、明日计划。' },
];
const copyText = async (value) => {
  try {
    await navigator.clipboard.writeText(value);
    return true;
  } catch (_) {
    const textarea = document.createElement('textarea');
    textarea.value = value;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    const copied = document.execCommand('copy');
    textarea.remove();
    return copied;
  }
};
const openCaptureModal = () => {
  const backdrop = document.createElement('div');
  backdrop.className = 'am-modal-backdrop';
  backdrop.innerHTML = `
    <section class="am-modal" role="dialog" aria-modal="true" aria-labelledby="am-capture-title">
      <div class="am-modal-head">
        <div>
          <h2 class="am-modal-title" id="am-capture-title">选择记录类型</h2>
          <p class="am-modal-note">选择后复制对应提示词，请粘贴给 Agent 手动触发；首页不会自动写入文件。</p>
        </div>
        <button class="am-modal-close" type="button" aria-label="关闭">×</button>
      </div>
      <div class="am-capture-options">
        ${captureOptions.map(option => `
          <button class="am-capture-option" type="button" data-am-capture-type="${option.type}">
            <span class="am-capture-icon">${option.icon}</span>
            <span><span class="am-capture-label">${option.label}</span><span class="am-capture-desc">${option.description}</span></span>
          </button>`).join('')}
      </div>
      <p class="am-copy-status" aria-live="polite"></p>
    </section>`;
  document.body.appendChild(backdrop);
  const close = () => {
    backdrop.remove();
    document.removeEventListener('keydown', onEscape);
  };
  backdrop.querySelector('.am-modal-close').addEventListener('click', close);
  backdrop.addEventListener('click', event => { if (event.target === backdrop) close(); });
  const onEscape = (event) => {
    if (event.key === 'Escape') close();
  };
  document.addEventListener('keydown', onEscape);
  backdrop.querySelectorAll('[data-am-capture-type]').forEach(button => {
    button.addEventListener('click', async () => {
      const option = captureOptions.find(item => item.type === button.dataset.amCaptureType);
      const copied = option ? await copyText(option.prompt) : false;
      backdrop.querySelector('.am-copy-status').textContent = copied
        ? `已复制“${option.label}”提示词，请粘贴给 Agent。`
        : '复制失败，请检查 Obsidian 的剪贴板权限后重试。';
      if (copied) window.setTimeout(close, 1100);
    });
  });
};

ensureStyles();
const root = dv.container;
root.classList.add('am-dashboard');
root.innerHTML = `
  <section class="am-hero">
    <div class="am-hero-top">
      <div>
        <div class="am-eyebrow">LOCAL MEMORY · OBSIDIAN</div>
        <h1 class="am-title">🏠 ${escapeHtml(currentTitle)}</h1>
        <p class="am-subtitle">任务、知识和每日总结，都从这里开始。</p>
      </div>
      <div class="am-clock"><span>现在</span><strong>${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}</strong><small>${now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}</small></div>
    </div>
    <div class="am-stats">
      <div class="am-stat"><div class="am-stat-label">📋 任务数</div><div class="am-stat-value">${tasks.length}</div><div class="am-stat-note">全部任务记录</div></div>
      <div class="am-stat"><div class="am-stat-label">📚 知识数</div><div class="am-stat-value">${knowledge.length}</div><div class="am-stat-note">可复用知识记录</div></div>
      <div class="am-stat"><div class="am-stat-label">📅 每日总结数</div><div class="am-stat-value">${dailies.length}</div><div class="am-stat-note">按日期识别的总结</div></div>
      <div class="am-stat"><div class="am-stat-label">🏷️ 标签数</div><div class="am-stat-value">${tags.length}</div><div class="am-stat-note">知识中的唯一标签</div></div>
    </div>
    <div class="am-search-row">
      <label class="am-search"><span class="am-search-icon">⌕</span><input data-am-search type="search" placeholder="搜索首页中的任务、知识和总结"><span class="am-search-hint">实时过滤</span></label>
      <button class="am-button" data-am-capture type="button">＋ 手动记录</button>
    </div>
    <div class="am-actions">
      <button class="am-action" data-am-scroll="am-tasks" type="button"><span class="am-action-icon">☑</span>任务表</button>
      <button class="am-action" data-am-path="${escapeHtml(indexPath('Knowledge'))}" type="button"><span class="am-action-icon">◇</span>知识索引</button>
      <button class="am-action" data-am-scroll="am-summaries" type="button"><span class="am-action-icon">◷</span>最近总结</button>
    </div>
  </section>
  <div class="am-main-grid">
    <section class="am-panel" id="am-tasks">
      <div class="am-panel-header"><span class="am-panel-title">任务表</span><span class="am-panel-meta">${tasks.length} 条任务 · 显示最近 ${Math.min(tasks.length, 12)} 条</span></div>
      <div class="am-table-wrap">
        ${tasks.length ? `<table class="am-table"><thead><tr><th>任务</th><th>状态</th><th>更新</th></tr></thead><tbody>
          ${tasks.slice(0, 12).map(page => `<tr class="am-filterable"><td><a href="#" data-am-path="${escapeHtml(page.file.path)}" class="am-task-name">${escapeHtml(displayName(page))}</a></td><td><span class="am-status">${escapeHtml(statusText(page.status))}</span></td><td>${formatDate(page.file.mtime)}</td></tr>`).join('')}
        </tbody></table>` : empty}
      </div>
    </section>
    <div class="am-side-stack">
      <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">最近更新</span><span class="am-panel-meta">任务、知识和总结 · 最近 ${Math.min(allRecords.length, 8)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(allRecords.slice(0, 8))}</div></div></section>
      <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">最近知识</span><span class="am-panel-meta">${knowledge.length} 条知识 · 显示最近 ${Math.min(knowledge.length, 6)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(knowledge.slice(0, 6).map(page => ({ page, kind: '' })))}</div></div></section>
      <section class="am-panel" id="am-summaries"><div class="am-panel-header"><span class="am-panel-title">最近总结</span><span class="am-panel-meta">${dailies.length} 条总结 · 显示最近 ${Math.min(dailies.length, 6)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(dailies.slice(0, 6).map(page => ({ page, kind: '' })))}</div></div></section>
      <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">标签统计</span><span class="am-panel-meta">${tags.length} 个知识标签</span></div><div class="am-panel-body">${tags.length ? `<div class="am-tag-cloud">${tags.map(([tag, count]) => `<span class="am-tag">#${escapeHtml(tag)} · ${count}</span>`).join('')}</div>` : empty}</div></section>
    </div>
  </div>`;

root.querySelectorAll('[data-am-path]').forEach(element => {
  element.addEventListener('click', event => { event.preventDefault(); app.workspace.openLinkText(element.dataset.amPath, currentPath, false); });
});
root.querySelectorAll('[data-am-scroll]').forEach(element => {
  element.addEventListener('click', () => root.querySelector(`#${element.dataset.amScroll}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
});
root.querySelector('[data-am-capture]').addEventListener('click', openCaptureModal);
const searchInput = root.querySelector('[data-am-search]');
searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLowerCase();
  root.querySelectorAll('.am-filterable').forEach(element => { element.style.display = !query || element.textContent.toLowerCase().includes(query) ? '' : 'none'; });
});
```

---

写入原则：仅显式调用 `agent-offline-mermory` 时写入，所有内容均限制在记忆根目录内。
