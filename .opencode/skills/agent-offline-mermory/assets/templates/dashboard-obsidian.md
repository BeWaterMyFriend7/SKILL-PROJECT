---
type: agent-memory-index
dashboard_version: 2
created: "{{timestamp}}"
updated: "{{timestamp}}"
---

# {{name}}

> 仪表盘数据由 Obsidian 社区插件 **Dataview** 渲染，请在设置 → 第三方插件中启用（含 JS 查询）。未启用时，可查看 [任务索引](Tasks/_index.md) 与 [知识索引](Knowledge/_index.md)。

## 概览

```dataviewjs
const card = (icon, label, value) =>
  `<div style="flex:1;min-width:110px;padding:12px 8px;border-radius:10px;background:#f4f6f8;border:1px solid #e3e6ea;text-align:center">
     <div style="font-size:13px;color:#8a919c">${icon} ${label}</div>
     <div style="font-size:26px;font-weight:700;margin-top:2px;color:#2f343d">${value}</div>
   </div>`;

const tasks = dv.pages('"Tasks"').where(p => p.type === 'agent-task');
const knowledge = dv.pages('"Knowledge"').where(p => p.type === 'agent-knowledge');
const dailies = dv.pages('"Daily"');
const tagSet = new Set(
  knowledge.flatMap(p => (p.tags || []).map(t => String(t).replace(/^#/, '')))
);

dv.paragraph(
  '<div style="display:flex;gap:10px;flex-wrap:wrap">' +
    card('📋', '任务数', tasks.length) +
    card('📚', '知识数', knowledge.length) +
    card('📅', '日记天数', dailies.length) +
    card('🏷️', '标签数', tagSet.size) +
  '</div>'
);
```

```dataviewjs
const lines = [];
for (let i = 6; i >= 0; i--) {
  const day = dv.date('today').minus({ days: i });
  const key = day.toFormat('yyyy-MM-dd');
  const count = dv.pages('"Daily"')
    .where(p => p.file.day && p.file.day.toFormat('yyyy-MM-dd') === key).length;
  lines.push(`${day.toFormat('MM-dd')} ${'█'.repeat(Math.min(count, 12))} ${count}`);
}
dv.paragraph('**近 7 天每日总结**\n\n' + lines.join('\n'));
```

## 任务与动态

<div style="display:flex;gap:20px;flex-wrap:wrap">

<div style="flex:1 1 300px;min-width:280px">

### 任务表

```dataview
TABLE WITHOUT ID file.link AS 任务, status AS 状态, file.mtime AS 更新时间
FROM "Tasks"
WHERE type = "agent-task"
SORT file.mtime DESC
LIMIT 15
```

</div>

<div style="flex:1 1 300px;min-width:280px">

### 最近知识

```dataview
TABLE WITHOUT ID file.link AS 知识, file.mtime AS 更新时间
FROM "Knowledge"
WHERE type = "agent-knowledge"
SORT file.mtime DESC
LIMIT 8
```

### 最近总结

```dataview
TABLE WITHOUT ID file.link AS 日期
FROM "Daily"
SORT file.name DESC
LIMIT 8
```

### 标签统计

```dataviewjs
const counts = {};
dv.pages('"Knowledge"')
  .where(p => p.type === 'agent-knowledge')
  .flatMap(p => p.tags || [])
  .forEach(t => {
    const key = String(t).replace(/^#/, '');
    counts[key] = (counts[key] || 0) + 1;
  });
const top = Object.entries(counts).sort((a, b) => b[1] - a[1]);
dv.paragraph(top.length ? top.map(([k, n]) => `#${k} × ${n}`).join('　') : '（暂无标签）');
```

</div>

</div>

---

写入原则：仅显式调用 `agent-offline-mermory` 时写入，所有内容均限制在记忆根目录内。
