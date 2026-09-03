---
type: agent-memory-index
dashboard_version: 14
dashboard_limit: 10
created: "{{timestamp}}"
updated: "{{timestamp}}"
---

# {{name}}

> 需要启用 Obsidian 社区插件 **Dataview** 及其 JavaScript 查询。可通过顶部 `dashboard_limit` 调整每区显示数量，有效范围为 1–100。

```dataviewjs
const STYLE_ID = 'agent-memory-dashboard-styles-v14';
['agent-memory-dashboard-styles', 'agent-memory-dashboard-styles-v9', 'agent-memory-dashboard-styles-v10', 'agent-memory-dashboard-styles-v11', 'agent-memory-dashboard-styles-v12', 'agent-memory-dashboard-styles-v13', STYLE_ID].forEach(id => document.getElementById(id)?.remove());
const ensureStyles = () => {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement('style');
  style.id = STYLE_ID;
  style.textContent = `
    .markdown-preview-sizer.am-dashboard-sizer { --file-line-width:1520px; width:min(1520px,calc(100% - 2rem)) !important; max-width:min(1520px,calc(100% - 2rem)) !important; }
    .am-dashboard { width: 100%; max-width: 1480px; margin: .5rem auto 1.5rem; color: var(--text-normal); }
    .am-hero { padding: clamp(1.2rem, 2.4vw, 2rem); border: 1px solid var(--background-modifier-border); border-radius: 24px; background: radial-gradient(circle at 100% 0%, rgba(124,92,255,.18), transparent 34%), linear-gradient(135deg,var(--background-secondary),var(--background-primary)); box-shadow: 0 18px 40px rgba(0,0,0,.12); }
    .am-hero-top { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; }
    .am-eyebrow { color:var(--text-muted); font-size:.72rem; font-weight:700; letter-spacing:.16em; }
    .am-title { margin:.35rem 0 0; color:var(--text-normal); font-size:clamp(2rem,4vw,3.5rem); letter-spacing:-.045em; line-height:1.05; white-space:normal; }
    .am-subtitle { max-width:42rem; margin:.85rem 0 0; color:var(--text-muted); font-size:.95rem; }
    .am-clock { min-width:9rem; padding:.8rem 1rem; border:1px solid var(--background-modifier-border); border-radius:16px; background:var(--background-primary-alt); text-align:right; }
    .am-clock span,.am-clock small { display:block; color:var(--text-muted); font-size:.72rem; }
    .am-clock strong { display:block; margin:.15rem 0; color:var(--text-normal); font-size:1.8rem; letter-spacing:-.05em; line-height:1; }
    .am-stats { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.85rem; margin-top:1.35rem; }
    .am-stat { box-sizing:border-box; display:flex; min-width:0; min-height:112px; flex-direction:column; justify-content:center; padding:1rem 1.1rem; border:1px solid var(--background-modifier-border); border-radius:17px; background:var(--background-primary); color:var(--text-normal); text-align:left; }
    .am-stat-link { cursor:pointer; outline:0; transition:transform 120ms,border-color 120ms,background 120ms,box-shadow 120ms; }
    .am-stat-link:hover,.am-stat-link:focus-visible { transform:translateY(-2px); border-color:var(--interactive-accent); background:var(--background-primary-alt); box-shadow:0 10px 24px rgba(0,0,0,.08); }
    .am-stat-label { color:var(--text-muted); font-size:.78rem; line-height:1.35; }
    .am-stat-value { margin-top:.2rem; color:var(--text-normal); font-size:1.9rem; font-weight:800; letter-spacing:-.05em; }
    .am-stat-note { margin-top:.1rem; color:var(--text-faint); font-size:.68rem; line-height:1.35; }
    .am-search-row { display:flex; align-items:center; gap:.7rem; margin-top:.9rem; }
    .am-search { display:flex; flex:1; align-items:center; gap:.65rem; min-width:0; padding:.75rem 1rem; border:1px solid var(--background-modifier-border); border-radius:14px; background:var(--background-primary); }
    .am-search-icon { color:var(--text-muted); font-size:1.1rem; }
    .am-search input { width:100%; min-width:0; border:0; outline:0; background:transparent; color:var(--text-normal); font:inherit; }
    .am-search-hint { flex:0 0 auto; color:var(--text-faint); font-size:.7rem; white-space:nowrap; }
    .am-button { flex:0 0 auto; padding:.78rem 1rem; cursor:pointer; border:1px solid var(--background-modifier-border); border-radius:12px; background:var(--background-primary); color:var(--text-normal); font:inherit; font-weight:700; white-space:nowrap; }
    .am-button:hover { border-color:var(--interactive-accent); background:var(--background-primary-alt); }
    .am-main-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.9rem; margin-top:1.3rem; align-items:stretch; }
    .am-panel { display:flex; flex-direction:column; height:390px; min-width:0; overflow:hidden; border:1px solid var(--background-modifier-border); border-radius:18px; background:var(--background-secondary); }
    .am-panel-header { flex:0 0 auto; min-width:0; padding:.85rem 1rem .72rem; border-bottom:1px solid var(--background-modifier-border); }
    .am-panel-title { display:block; color:var(--text-normal); font-size:.98rem; font-weight:800; line-height:1.35; white-space:nowrap; }
    .am-panel-meta { display:block; margin-top:.16rem; color:var(--text-muted); font-size:.7rem; line-height:1.35; white-space:normal; }
    .am-panel-body,.am-table-wrap { flex:1 1 auto; min-height:0; overflow-x:hidden; overflow-y:auto; scrollbar-gutter:stable; }
    .am-panel-body { padding:.7rem .8rem .85rem; }
    .am-table { width:100%; table-layout:fixed; border-collapse:collapse; font-size:.8rem; }
    .am-table th { position:sticky; top:0; z-index:1; padding:.5rem .62rem; background:var(--background-secondary); color:var(--text-faint); font-size:.68rem; text-align:left; white-space:nowrap; }
    .am-table th:nth-child(2),.am-table td:nth-child(2) { width:5.2rem; }
    .am-table th:nth-child(3),.am-table td:nth-child(3) { width:6.4rem; }
    .am-table td { padding:.46rem .62rem; border-top:1px solid var(--background-modifier-border); vertical-align:middle; }
    .am-table a { color:var(--text-normal); text-decoration:none; }
    .am-table a:hover { color:var(--interactive-accent); }
    .am-task-name,.am-item-main { display:block; width:100%; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .am-status { display:inline-block; max-width:100%; overflow:hidden; padding:.16rem .4rem; border-radius:999px; background:var(--background-primary-alt); color:var(--text-muted); font-size:.66rem; text-overflow:ellipsis; white-space:nowrap; }
    .am-link-list { display:grid; gap:.3rem; }
    .am-link-item { display:grid; grid-template-columns:minmax(0,1fr) 5.5rem; align-items:center; gap:.65rem; min-width:0; padding:.52rem .62rem; border-radius:10px; color:var(--text-normal); text-decoration:none; }
    .am-link-item:hover { background:var(--background-primary-alt); text-decoration:none; }
    .am-item-kind,.am-item-time { overflow:hidden; color:var(--text-faint); font-size:.68rem; text-align:right; text-overflow:ellipsis; white-space:nowrap; }
    .am-item-kind { color:var(--interactive-accent); }
    .am-empty { padding:1.1rem .75rem; color:var(--text-faint); font-size:.8rem; text-align:center; }
    .am-modal-backdrop { position:fixed; inset:0; z-index:9999; display:grid; place-items:center; padding:1rem; background:rgba(0,0,0,.52); backdrop-filter:blur(4px); }
    .am-modal { width:min(540px,calc(100vw - 2rem)); padding:1.15rem; border:1px solid var(--background-modifier-border); border-radius:18px; background:var(--background-primary); color:var(--text-normal); box-shadow:0 24px 80px rgba(0,0,0,.32); font-family:var(--font-interface); }
    .am-modal * { box-sizing:border-box; }
    .am-modal-head { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin-bottom:1rem; }
    .am-modal-title { margin:0; color:var(--text-normal); font-size:1.08rem; line-height:1.35; }
    .am-modal-note { margin:.28rem 0 0; color:var(--text-muted); font-size:.76rem; line-height:1.55; }
    .am-modal-close { flex:0 0 auto; padding:.1rem .35rem; cursor:pointer; border:0; background:transparent; color:var(--text-muted); font-size:1.25rem; line-height:1.2; }
    .am-capture-options { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.55rem; }
    .am-capture-option { display:flex; min-width:0; align-items:center; justify-content:center; gap:.42rem; padding:.68rem .55rem; border:1px solid var(--background-modifier-border); border-radius:12px; background:var(--background-secondary); color:var(--text-normal); cursor:pointer; font:inherit; font-size:.82rem; font-weight:700; line-height:1.3; white-space:nowrap; }
    .am-capture-option.is-active { border-color:var(--interactive-accent); background:var(--background-primary-alt); }
    .am-capture-form { display:grid; gap:.48rem; margin-top:.9rem; }
    .am-capture-form label { color:var(--text-muted); font-size:.76rem; font-weight:700; }
    .am-capture-title-input { width:100%; padding:.72rem .8rem; border:1px solid var(--background-modifier-border); border-radius:11px; outline:0; background:var(--background-secondary); color:var(--text-normal); font:inherit; font-size:.86rem; }
    .am-capture-title-input:focus { border-color:var(--interactive-accent); }
    .am-capture-help { min-height:2.3rem; margin:0; color:var(--text-muted); font-size:.72rem; line-height:1.5; }
    .am-modal-footer { display:flex; align-items:center; justify-content:space-between; gap:.75rem; margin-top:.95rem; }
    .am-capture-status { min-height:1.2rem; margin:0; color:var(--interactive-accent); font-size:.73rem; line-height:1.4; }
    .am-create-button { flex:0 0 auto; padding:.68rem .95rem; border:0; border-radius:10px; background:var(--interactive-accent); color:var(--text-on-accent); cursor:pointer; font:inherit; font-size:.82rem; font-weight:800; white-space:nowrap; }
    .am-create-button:disabled { cursor:wait; opacity:.65; }
    @media (max-width:900px) { .am-hero-top,.am-search-row { flex-direction:column; align-items:stretch; } .am-clock { text-align:left; } .am-stats { grid-template-columns:repeat(2,minmax(0,1fr)); } .am-main-grid { grid-template-columns:minmax(0,1fr); } .am-panel { height:360px; } }
    @media (max-width:520px) { .am-stats,.am-capture-options { grid-template-columns:minmax(0,1fr); } .am-search-hint { display:none; } .am-modal-footer { align-items:stretch; flex-direction:column; } .am-create-button { width:100%; } }
  `;
  document.head.appendChild(style);
};

const escapeHtml = value => String(value ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
const pad = value => String(value).padStart(2,'0');
const localDateKey = (value = new Date()) => `${value.getFullYear()}-${pad(value.getMonth()+1)}-${pad(value.getDate())}`;
const localTimeKey = (value = new Date()) => `${pad(value.getHours())}${pad(value.getMinutes())}${pad(value.getSeconds())}`;
const currentPath = String(dv.current()?.file?.path ?? '');
const memoryFolder = currentPath.split('/').slice(0,-1).join('/');
const pathInMemory = (...parts) => [memoryFolder,...parts].filter(Boolean).join('/');
const pagesIn = directory => dv.pages(`"${pathInMemory(directory)}"`);
const pageType = page => String(page.type ?? '').toLowerCase();
const isMemoryRecord = (page,directory,expectedType) => { const path=String(page.file?.path??''); const name=String(page.file?.name??''); const type=pageType(page); return path.startsWith(`${pathInMemory(directory)}/`) && name !== '_index' && (!type || type === expectedType); };
const isDailySummary = page => isMemoryRecord(page,'Daily','agent-daily') && (pageType(page)==='agent-daily' || /^\d{4}-\d{2}-\d{2}$/.test(String(page.file?.name??'')));
const millis = page => { const value=page.file?.mtime; if (value && typeof value.toMillis==='function') return value.toMillis(); const parsed=Date.parse(String(value??'')); return Number.isNaN(parsed)?0:parsed; };
const formatDate = value => { if (value && typeof value.toFormat==='function') return value.toFormat('MM-dd HH:mm'); const parsed=new Date(String(value??'')); return Number.isNaN(parsed.getTime())?'—':parsed.toLocaleString('zh-CN',{month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}); };
const displayName = page => String(page.file?.name??'').replace(/^\d{4}-\d{2}-\d{2}-\d{6}-/,'').replace(/^\d{4}-\d{2}-\d{2}-/,'');
const statusText = value => ({active:'进行中',completed:'已完成',done:'已完成',blocked:'已阻塞',paused:'已暂停'}[String(value??'active').toLowerCase()] || String(value||'进行中'));
const rawLimit = Number(dv.current()?.dashboard_limit ?? 10);
const listLimit = Math.min(100,Math.max(1,Number.isFinite(rawLimit)?Math.floor(rawLimit):10));
const tasks = pagesIn('Tasks').where(page=>isMemoryRecord(page,'Tasks','agent-task')).array().sort((a,b)=>millis(b)-millis(a));
const knowledge = pagesIn('Knowledge').where(page=>isMemoryRecord(page,'Knowledge','agent-knowledge')).array().sort((a,b)=>millis(b)-millis(a));
const dailies = pagesIn('Daily').where(isDailySummary).array().sort((a,b)=>millis(b)-millis(a));
const allRecords = [...tasks.map(page=>({page,kind:'任务'})),...knowledge.map(page=>({page,kind:'知识'})),...dailies.map(page=>({page,kind:'总结'}))].sort((a,b)=>millis(b.page)-millis(a.page));
const now = new Date();
const currentTitle = String(dv.current()?.file?.name ?? '{{name}}');
const indexPath = directory => pathInMemory(directory,'_index.md');
const empty = '<div class="am-empty">暂无记录</div>';
const linkList = items => items.length ? items.map(({page,kind})=>{ const title=displayName(page); return `<a href="#" class="am-link-item am-filterable" data-am-path="${escapeHtml(page.file.path)}" title="${escapeHtml(title)}"><span class="am-item-main">${escapeHtml(title)}</span><span class="${kind?'am-item-kind':'am-item-time'}">${escapeHtml(kind||formatDate(page.file.mtime))}</span></a>`; }).join('') : empty;

const captureOptions = {
  task:{directory:'Tasks',icon:'☑',label:'任务',placeholder:'例如：完成首页布局优化',help:'在 Tasks 中新建任务文件，并预置目标、进度、风险和关键文件章节。'},
  knowledge:{directory:'Knowledge',icon:'◇',label:'知识',placeholder:'例如：Obsidian Dataview 布局经验',help:'在 Knowledge 中新建知识文件，并预置场景、原因、方案和注意事项章节。'},
  daily:{directory:'Daily',icon:'◷',label:'总结',placeholder:'',help:`使用今天的日期 ${localDateKey()} 建档；如果文件已存在，将直接打开且不会覆盖。`}
};
const safeFileTitle = value => { let clean=String(value??'').trim().replace(/[<>:"/\\|?*\x00-\x1f]/g,'-').replace(/\s+/g,'-').replace(/-+/g,'-').replace(/^[ .-]+|[ .-]+$/g,''); if(!clean) clean='未命名记录'; if(/^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/i.test(clean)) clean=`_${clean}`; return clean.slice(0,72).replace(/[ .-]+$/g,'')||'未命名记录'; };
const uniqueNotePath = (directory,title,createdAt) => { const base=`${localDateKey(createdAt)}-${localTimeKey(createdAt)}-${safeFileTitle(title)}`; let candidate=pathInMemory(directory,`${base}.md`); let suffix=2; while(app.vault.getAbstractFileByPath(candidate)){ candidate=pathInMemory(directory,`${base}-${suffix}.md`); suffix+=1; } return candidate; };
const noteTemplate = (type,title,createdAt) => {
  const timestamp=createdAt.toISOString();
  if(type==='task') return `---
type: agent-task
status: active
tags: []
created: "${timestamp}"
updated: "${timestamp}"
---

# ${title}

## 目标

## 进度与下一步

## 阻塞与风险

## 关键文件与命令
`;
  if(type==='knowledge') return `---
type: agent-knowledge
tags: []
created: "${timestamp}"
updated: "${timestamp}"
---

# ${title}

## 场景

## 问题与原因

## 解决方案与验证

## 注意事项
`;
  const date=localDateKey(createdAt);
  return `---
type: agent-daily
date: "${date}"
created: "${timestamp}"
updated: "${timestamp}"
---

# ${date}

## 完成

## 问题

## 待办
`;
};
const refreshIndex = async directory => {
  const prefix=`${pathInMemory(directory)}/`;
  const files=app.vault.getMarkdownFiles().filter(file=>file.path.startsWith(prefix)&&file.name!=='_index.md');
  const records=(await Promise.all(files.map(async file=>{
    const content=await app.vault.cachedRead(file);
    const cache=app.metadataCache.getFileCache(file);
    const frontmatterBlock=content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1]??'';
    const frontmatterValue=key=>frontmatterBlock.match(new RegExp(`^${key}:\\s*[\"']?([^\"'\\r\\n]+)`,'mi'))?.[1]?.trim();
    const frontmatter=cache?.frontmatter??{};
    const type=String(frontmatter.type??frontmatterValue('type')??'').toLowerCase();
    if(directory==='Daily'&&type!=='agent-daily'&&!/^\d{4}-\d{2}-\d{2}$/.test(file.basename)) return null;
    const heading=cache?.headings?.find(item=>item.level===1)?.heading??content.match(/^#\s+(.+)$/m)?.[1]?.trim();
    const title=String(heading||file.basename).replace(/\|/g,'／').replace(/\]/g,'］');
    const status=String(frontmatter.status??frontmatterValue('status')??'active').toLowerCase();
    return {file,title,status,modified:file.stat.mtime};
  }))).filter(Boolean).sort((a,b)=>b.modified-a.modified);
  const includeStatus=directory==='Tasks';
  const header=includeStatus?'| 状态 | 标题 | 更新时间 | 文件 |\n| --- | --- | --- | --- |':'| 标题 | 更新时间 | 文件 |\n| --- | --- | --- |';
  const rows=records.map(record=>{ const modified=new Date(record.modified).toLocaleString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}); const link=`[[${record.file.path}|${record.title}]]`; return includeStatus?`| ${record.status} | ${record.title} | ${modified} | ${link} |`:`| ${record.title} | ${modified} | ${link} |`; });
  const titles={Tasks:'任务索引',Knowledge:'知识索引',Daily:'每日总结索引'};
  const timestamp=new Date().toISOString();
  const content=`---\ntype: agent-memory-index\nupdated: "${timestamp}"\n---\n\n# ${titles[directory]}\n\n${rows.length?`${header}\n${rows.join('\n')}`:'（暂无记录）'}\n`;
  const indexFile=app.vault.getAbstractFileByPath(pathInMemory(directory,'_index.md'));
  if(indexFile) await app.vault.modify(indexFile,content); else await app.vault.create(pathInMemory(directory,'_index.md'),content);
};
const openCaptureModal = () => {
  let selectedType='task';
  const backdrop=document.createElement('div');
  backdrop.className='am-modal-backdrop';
  backdrop.innerHTML=`<section class="am-modal" role="dialog" aria-modal="true" aria-labelledby="am-capture-title"><div class="am-modal-head"><div><h2 class="am-modal-title" id="am-capture-title">新建记录</h2><p class="am-modal-note">选择类型并填写标题，首页会直接按对应模板创建 Markdown 文件并打开。</p></div><button class="am-modal-close" type="button" aria-label="关闭">×</button></div><div class="am-capture-options">${Object.entries(captureOptions).map(([type,option])=>`<button class="am-capture-option${type===selectedType?' is-active':''}" type="button" data-am-capture-type="${type}"><span>${option.icon}</span><span>${option.label}</span></button>`).join('')}</div><div class="am-capture-form"><label for="am-note-title">记录标题</label><input class="am-capture-title-input" id="am-note-title" type="text" maxlength="120" autocomplete="off"><p class="am-capture-help"></p></div><div class="am-modal-footer"><p class="am-capture-status" aria-live="polite"></p><button class="am-create-button" type="button">创建并打开</button></div></section>`;
  document.body.appendChild(backdrop);
  const titleInput=backdrop.querySelector('.am-capture-title-input'); const help=backdrop.querySelector('.am-capture-help'); const status=backdrop.querySelector('.am-capture-status'); const createButton=backdrop.querySelector('.am-create-button'); const titleLabel=backdrop.querySelector('label[for="am-note-title"]');
  const close=()=>{backdrop.remove();document.removeEventListener('keydown',onEscape);};
  const syncType=()=>{ const option=captureOptions[selectedType]; backdrop.querySelectorAll('[data-am-capture-type]').forEach(button=>button.classList.toggle('is-active',button.dataset.amCaptureType===selectedType)); const isDaily=selectedType==='daily'; titleInput.disabled=isDaily; titleInput.hidden=isDaily; titleLabel.hidden=isDaily; titleInput.placeholder=option.placeholder; help.textContent=option.help; createButton.textContent=isDaily?'打开今日总结':'创建并打开'; status.textContent=''; if(!isDaily) titleInput.focus(); };
  const createNote=async()=>{ const option=captureOptions[selectedType]; const title=titleInput.value.trim(); if(selectedType!=='daily'&&!title){status.textContent='请先填写记录标题。';titleInput.focus();return;} createButton.disabled=true; status.textContent='正在创建…'; try { const directoryPath=pathInMemory(option.directory); if(!app.vault.getAbstractFileByPath(directoryPath)) await app.vault.createFolder(directoryPath); const createdAt=new Date(); const notePath=selectedType==='daily'?pathInMemory(option.directory,`${localDateKey(createdAt)}.md`):uniqueNotePath(option.directory,title,createdAt); let file=app.vault.getAbstractFileByPath(notePath); const existed=Boolean(file); if(!file) file=await app.vault.create(notePath,noteTemplate(selectedType,title,createdAt)); await refreshIndex(option.directory); status.textContent=existed?'记录已存在，正在打开…':'创建成功，正在打开…'; await app.workspace.getLeaf(false).openFile(file); close(); } catch(error) { status.textContent=`创建失败：${error?.message||error}`; createButton.disabled=false; } };
  backdrop.querySelector('.am-modal-close').addEventListener('click',close); backdrop.addEventListener('click',event=>{if(event.target===backdrop)close();}); const onEscape=event=>{if(event.key==='Escape')close();}; document.addEventListener('keydown',onEscape); backdrop.querySelectorAll('[data-am-capture-type]').forEach(button=>button.addEventListener('click',()=>{selectedType=button.dataset.amCaptureType;syncType();})); titleInput.addEventListener('keydown',event=>{if(event.key==='Enter')createNote();}); createButton.addEventListener('click',createNote); syncType();
};

ensureStyles();
const root=dv.container; root.classList.add('am-dashboard');
const previewSizer=root.closest('.markdown-preview-sizer');
previewSizer?.classList.add('am-dashboard-sizer');
previewSizer?.style.setProperty('--file-line-width','1520px');
previewSizer?.style.setProperty('width','min(1520px, calc(100% - 2rem))','important');
previewSizer?.style.setProperty('max-width','min(1520px, calc(100% - 2rem))','important');
root.innerHTML=`
  <section class="am-hero">
    <div class="am-hero-top">
      <div><div class="am-eyebrow">LOCAL MEMORY · OBSIDIAN</div><h1 class="am-title">🏠 ${escapeHtml(currentTitle)}</h1><p class="am-subtitle">任务、知识和每日总结，都从这里开始。</p></div>
      <div class="am-clock"><span>现在</span><strong>${now.toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'})}</strong><small>${now.toLocaleDateString('zh-CN',{year:'numeric',month:'long',day:'numeric',weekday:'long'})}</small></div>
    </div>
    <div class="am-stats">
      <div class="am-stat am-stat-link" data-am-path="${escapeHtml(indexPath('Tasks'))}" role="link" tabindex="0" title="打开任务索引"><div class="am-stat-label">📋 任务数</div><div class="am-stat-value">${tasks.length}</div><div class="am-stat-note">点击打开任务索引</div></div>
      <div class="am-stat am-stat-link" data-am-path="${escapeHtml(indexPath('Knowledge'))}" role="link" tabindex="0" title="打开知识索引"><div class="am-stat-label">📚 知识数</div><div class="am-stat-value">${knowledge.length}</div><div class="am-stat-note">点击打开知识索引</div></div>
      <div class="am-stat am-stat-link" data-am-path="${escapeHtml(indexPath('Daily'))}" role="link" tabindex="0" title="打开每日总结索引"><div class="am-stat-label">📅 每日总结数</div><div class="am-stat-value">${dailies.length}</div><div class="am-stat-note">点击打开总结索引</div></div>
    </div>
    <div class="am-search-row"><label class="am-search"><span class="am-search-icon">⌕</span><input data-am-search type="search" placeholder="搜索首页中的任务、知识和总结"><span class="am-search-hint">实时过滤</span></label><button class="am-button" data-am-capture type="button">＋ 手动记录</button></div>
  </section>
  <div class="am-main-grid">
    <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">任务表</span><span class="am-panel-meta">${tasks.length} 条任务 · 显示最近 ${Math.min(tasks.length,listLimit)} 条</span></div><div class="am-table-wrap">${tasks.length?`<table class="am-table"><thead><tr><th>任务</th><th>状态</th><th>更新</th></tr></thead><tbody>${tasks.slice(0,listLimit).map(page=>{const title=displayName(page);return `<tr class="am-filterable"><td><a href="#" data-am-path="${escapeHtml(page.file.path)}" class="am-task-name" title="${escapeHtml(title)}">${escapeHtml(title)}</a></td><td><span class="am-status">${escapeHtml(statusText(page.status))}</span></td><td>${formatDate(page.file.mtime)}</td></tr>`;}).join('')}</tbody></table>`:empty}</div></section>
    <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">最近更新</span><span class="am-panel-meta">任务、知识和总结 · 显示最近 ${Math.min(allRecords.length,listLimit)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(allRecords.slice(0,listLimit))}</div></div></section>
    <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">最近知识</span><span class="am-panel-meta">${knowledge.length} 条知识 · 显示最近 ${Math.min(knowledge.length,listLimit)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(knowledge.slice(0,listLimit).map(page=>({page,kind:''})))}</div></div></section>
    <section class="am-panel"><div class="am-panel-header"><span class="am-panel-title">最近总结</span><span class="am-panel-meta">${dailies.length} 条总结 · 显示最近 ${Math.min(dailies.length,listLimit)} 条</span></div><div class="am-panel-body"><div class="am-link-list">${linkList(dailies.slice(0,listLimit).map(page=>({page,kind:''})))}</div></div></section>
  </div>`;
root.querySelectorAll('[data-am-path]').forEach(element=>element.addEventListener('click',event=>{event.preventDefault();app.workspace.openLinkText(element.dataset.amPath,currentPath,false);}));
root.querySelectorAll('.am-stat-link').forEach(element=>element.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();element.click();}}));
root.querySelector('[data-am-capture]').addEventListener('click',openCaptureModal);
const searchInput=root.querySelector('[data-am-search]'); searchInput.addEventListener('input',()=>{const query=searchInput.value.trim().toLowerCase();root.querySelectorAll('.am-filterable').forEach(element=>{element.style.display=!query||element.textContent.toLowerCase().includes(query)?'':'none';});});
```

---

写入原则：Agent 仅在明确触发 `agent-offline-mermory` 时通过写入器写入；首页“手动记录”仅在用户点击并确认后，按内置模板在当前记忆根目录的 `Daily`、`Tasks` 或 `Knowledge` 中创建文件。
