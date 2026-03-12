# 软件台账管理平台原型设计

## 概述
本原型为软件台账管理平台的交互式HTML原型，包含软件台账、软件使用关系台账、可观测大屏等主要功能模块的界面设计。

## 文件结构
```
design-output/
├── index.html              # 导航首页
├── css/
│   └── style.css          # 自定义样式
├── js/
│   └── main.js            # 交互逻辑
├── pages/
│   ├── software-list.html          # 软件台账列表页
│   ├── software-detail.html        # 软件详情页
│   ├── terminal-usage.html         # 终端使用关系列表页
│   ├── app-usage.html              # 应用系统使用关系列表页
│   ├── server-usage.html           # 服务器使用关系列表页
│   ├── statistics-dashboard.html   # 数据统计大屏
│   └── sync-monitor.html           # 同步监控大屏
├── data/
│   └── mock-data.json     # 模拟数据（可选）
└── assets/                # 图片等静态资源
```

## 设计规范
- **颜色**：主色天蓝色 (#1E90FF)，辅助色浅灰色 (#F5F5F5)，强调色浅红色 (#FF6B6B)
- **字体**：系统默认字体（-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto等）
- **布局**：16:9宽屏布局，内容居中，两侧留白，元素间距均匀
- **交互**：按钮、链接有悬停反馈，表格支持排序、筛选、分页

## 使用说明
1. 直接在浏览器中打开 `index.html` 即可访问导航页。
2. 点击导航菜单进入各功能页面。
3. 各页面已包含基本的交互元素（搜索框、筛选器、表格、图表等），数据为静态模拟。
4. 可通过修改 `data/mock-data.json` 或直接编辑HTML来调整模拟数据。

## 注意事项
- 本原型为静态HTML，不依赖后端服务。
- 图表使用ECharts库（通过CDN引入），需网络连接。
- 权限控制仅通过界面元素（如显示/隐藏）模拟，实际需后端实现。
- 大数据量表格已做分页模拟，实际开发需结合后端分页接口。