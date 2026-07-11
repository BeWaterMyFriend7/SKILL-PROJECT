# Draw.io 质量契约 v1.0

## 硬性门槛

- 文件为严格 UTF-8；XML 可解析；根节点为 `mxfile` 或 `mxGraphModel`。
- `mxCell` id 唯一；每个 `mxGeometry` 都有 `as="geometry"`。
- source/target 引用存在；所有可见元素位于画布内。
- 页面边距至少 30；画布利用率 50%-85%，目标 60%-80%。
- 正文不小于 12，辅助文字不小于 11；普通正文对比度至少 4.5:1。
- 区域标题安全区至少 44；节点不得进入标题区。
- 同级元素不重叠；卡片间距至少 28；区域间距至少 36。
- 连线优先正交，不得穿过无关节点；错误路径红色实线；异步路径紫色虚线。
- 架构图三级信息必须是独立可编辑小标签。
- 模板是中性骨架，示例是业务完成品；不同意图不得使用相同 blob 冒充。

## 交付命令

```bash
python -X utf8 scripts/validate_drawio.py <file> --fail-on-warning
python -X utf8 scripts/check_contrast.py <file> --fail-on-warning
python -X utf8 scripts/render_drawio_preview.py <file> <preview.png> --scale 1
```

五类架构基准各保存 100% 与 25% PNG 到 `examples/previews/`；必须由固定版本 Draw.io Desktop 官方 CLI 导出。`examples/previews/manifest.json` 固定版本、尺寸和 SHA-256，任何变化都必须显式重审。
