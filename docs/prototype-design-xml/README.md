# prototype-design-xml 使用说明

## 适用场景

- 在 Draw.io 中评审、移动和修改页面组件。
- 使用多个 Draw.io 页面表达页面清单和状态。
- 需要真实按钮、表单和弹窗交互时使用 `prototype-design-html`。

## 输入输出

- 输入：原型目的、用户角色、页面范围、核心任务、设备类型和可选主题。
- 输出：未压缩、UTF-8、可编辑的 `.drawio` 文件。
- 未指定目录时默认输出到项目根目录 `output/prototype/drawio`。

## 快速使用

```text
请使用 prototype-design-xml 生成包含概览、列表和创建表单的后台页面原型。
```

- 示例和验证记录：[examples.md](examples.md)
- Draw.io 示例：[drawio/](drawio/)
- 渲染截图：[images/](images/)

## 核心流程

1. 分析用户、页面范围和核心任务。
2. 规划页面清单、导航和页面关系。
3. 明确画框、区域、组件、状态和布局。
4. 生成 Draw.io XML。
5. 检查 XML、ID、页面、父级、尺寸和可编辑性。
6. 在 Draw.io 中真实渲染并修正布局问题。
