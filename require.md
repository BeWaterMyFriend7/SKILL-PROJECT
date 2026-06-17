下面是重新优化后的方案，重点补齐你说的四块：**Skill 项目结构、示例模板、标题/卡片层级规约、图例规约**。

---

# 一、需求定位

这个 Skill 的目标不是简单生成 XML，而是生成 **风格统一、布局稳定、可编辑、可复用的 drawio 架构图/分析图/项目图**。

核心原则：

```text
逻辑结构由大模型推理
视觉风格由规约约束
布局坐标由模板和布局算法控制
最终质量由校验器兜底
```

架构图的逻辑层次不固定，但元素设计、排版、卡片层级、配色、标题、图例、连线风格必须统一。

---

# 二、推荐 Skill 项目结构

```text
xml-diagram/
├── skill.md
│
├── assets/
│   ├── design-system.md              # 全局视觉设计系统
│   ├── theme-tokens.md                # 浅色/深色/语义色 token
│   ├── typography-rules.md            # 标题、正文、标签字号规约
│   ├── component-rules.md             # 容器、卡片、标签、图例组件规约
│   ├── layout-rules.md                # 布局、间距、画布、安全区规约
│   ├── edge-rules.md                  # 连线、箭头、标签、路由规约
│   ├── legend-rules.md                # 图例生成规约
│   ├── validation-rules.md            # 重叠、颜色、画布、XML 校验规则
│   └── dsl-schema.md                  # 中间 DSL 结构定义
│
├── templates/
│   ├── architecture/
│   │   ├── business-layered.drawio     # 业务架构图模板
│   │   ├── application-pipeline.drawio # 应用架构图模板
│   │   ├── technical-layered.drawio    # 技术架构图模板
│   │   └── deployment-region.drawio    # 部署架构图模板
│   │
│   ├── project/
│   │   ├── roadmap-timeline.drawio     # 项目研发时间线模板
│   │   ├── lifecycle-flow.drawio       # 生命周期流程图模板
│   │   └── milestone-board.drawio      # 里程碑看板模板
│   │
│   ├── analysis/
│   │   ├── comparison-vs.drawio        # 对比图模板
│   │   ├── decision-matrix.drawio      # 决策矩阵模板
│   │   └── swot.drawio                 # SWOT 模板
│   │
│   └── summary/
│       ├── article-summary.drawio      # 文章总结图模板
│       ├── knowledge-map.drawio        # 知识结构图模板
│       └── card-summary.drawio         # 卡片总结图模板
│
├── examples/
│   ├── business-architecture-example.drawio
│   ├── application-architecture-example.drawio
│   ├── technical-architecture-example.drawio
│   ├── project-timeline-example.drawio
│   ├── lifecycle-example.drawio
│   └── comparison-example.drawio
│
├── output/
│   └── drawio/
│
└── scripts/
    ├── validate_drawio.py              # XML 与布局校验
    ├── check_contrast.py               # 文字可读性校验
    └── template_preview.py             # 模板预览测试
```

重点是：**templates 和 examples 必须存在**。
否则模型只看规约，还是容易自由发挥。

---

# 三、示例模板的重要性

Skill 里需要明确写：

```text
生成任何图形前，必须优先参考 templates/ 中同类型模板。
模板决定布局骨架、标题层级、卡片层级、图例位置、连线风格。
用户内容只替换模板中的文本、节点数量、关系和局部尺寸。
禁止脱离模板自由布局。
```

推荐模板映射：

| 用户需求    | 优先模板                                                 |
| ------- | ---------------------------------------------------- |
| 业务架构图   | `templates/architecture/business-layered.drawio`     |
| 应用架构图   | `templates/architecture/application-pipeline.drawio` |
| 技术架构图   | `templates/architecture/technical-layered.drawio`    |
| 部署架构图   | `templates/architecture/deployment-region.drawio`    |
| 项目研发时间线 | `templates/project/roadmap-timeline.drawio`          |
| 项目生命周期  | `templates/project/lifecycle-flow.drawio`            |
| 对比图     | `templates/analysis/comparison-vs.drawio`            |
| 文章总结图   | `templates/summary/article-summary.drawio`           |

---

# 四、标题层级规约

## 1. 页面标题 H1

用于整张图标题。

```yaml
H1:
  fontSize: 24
  fontStyle: bold
  align: center
  color: title
  marginTop: 20
  marginBottom: 8
```

示例：

```text
业务架构图设计案例
应用架构图设计案例
项目研发生命周期流程图
```

---

## 2. 页面副标题 H2

用于英文说明或补充说明。

```yaml
H2:
  fontSize: 12
  color: subtext
  align: center
  marginBottom: 24
```

示例：

```text
Business Architecture Design
Software Development Life Cycle
```

---

## 3. 区域标题 Section Title

用于大容器标题。

```yaml
SectionTitle:
  fontSize: 18
  fontStyle: bold
  color: sectionColor
  align: left
  height: 44
```

示例：

```text
业务场景层（Business Scenario Layer）
业务能力层（Business Capability Layer）
业务对象层（Business Object Layer）
```

强制规则：

```text
区域标题必须拥有独立 Header 安全区
节点不得覆盖区域标题
Header 高度不得小于 44px
```

---

## 4. 卡片标题 Card Title

用于一级卡片标题。

```yaml
CardTitle:
  fontSize: 14
  fontStyle: bold
  color: "#ffffff"
  align: center
  height: 34
```

---

## 5. 内容标签 Item Tag

用于卡片内部的小能力点。

```yaml
ItemTag:
  fontSize: 10
  color: text
  height: 22
  borderRadius: 6
  paddingX: 8
```

---

# 五、卡片层级规约

必须明确几级卡片，否则模型会乱摆。

## Level 0：Page

整张图。

```text
Page = Title + Content + Footer/Legend
```

---

## Level 1：Section Container

大区域容器。

用于：

```text
业务场景层
业务能力层
业务对象层
前端应用层
后端服务层
外部系统层
关键里程碑
各阶段角色与交付物
```

规约：

```yaml
SectionContainer:
  rounded: 1
  arcSize: 12
  strokeWidth: 2
  fillColor: container_bg
  paddingX: 28
  paddingY: 24
  headerHeight: 44
```

禁止：

```text
节点进入 Section Header 区域
Section 内部没有 padding
多个 Section 间距小于 32px
```

---

## Level 2：Group Card

中型卡片，用于领域、模块、阶段、系统。

例如：

```text
用户管理域
商品管理域
API 网关
用户中心
设计阶段
开发阶段
```

规约：

```yaml
GroupCard:
  width: 180-260
  height: auto
  minHeight: 86
  rounded: 1
  arcSize: 10
  strokeWidth: 2
  headerHeight: 34
  bodyPadding: 12
```

---

## Level 3：Item Tag

小标签，用于能力点、技术点、属性。

例如：

```text
注册登录
信息管理
Spring Boot
Redis
Prometheus
```

规约：

```yaml
ItemTag:
  width: auto
  minWidth: 54
  height: 22
  gapX: 8
  gapY: 8
  rounded: 1
  arcSize: 6
```

---

## Level 4：Annotation

说明、脚注、备注。

```yaml
Annotation:
  fontSize: 11
  color: subtext
  align: center
```

---

# 六、图例规约

图例不是可选项，满足以下任一条件必须生成：

```text
使用了 4 种以上语义色
存在虚线/实线/主链路区别
存在阶段颜色
存在角色颜色
存在系统边界颜色
```

## 图例位置

优先级：

```text
右侧独立图例区
底部横向图例区
右下角悬浮图例
```

禁止：

```text
图例覆盖主内容
图例放在主流程中间
图例与节点间距小于 24px
```

## 图例类型

### 1. 颜色图例

```text
蓝色 = 用户/前端/需求
绿色 = 服务/能力/通过
橙色 = 外部系统/设计/警告
红色 = 错误/风险/开发重点
紫色 = 测试/异步/对比对象
青色 = 部署/发布/通信
```

### 2. 线型图例

```text
实线箭头 = 同步调用/主流程
虚线箭头 = 异步消息/回调
粗箭头 = 主链路
红色实线 = 异常/失败路径
```

### 3. 阶段图例

适用于项目周期图：

```text
需求
立项
设计
开发
测试
部署
运维
迭代
```

---

# 七、统一风格规约

## 浅色模式

```yaml
bg: "#f8fafc"
container_bg: "#f1f5f9"
card_bg: "#ffffff"
border: "#cbd5e1"
title: "#0f172a"
text: "#334155"
subtext: "#64748b"
line: "#94a3b8"
```

## 深色模式

```yaml
bg: "#0f172a"
container_bg: "#111827"
card_bg: "#1e293b"
border: "#334155"
title: "#f8fafc"
text: "#cbd5e1"
subtext: "#94a3b8"
line: "#64748b"
```

## 强制规则

```text
深色模式禁止 shadow
浅色模式允许轻微 shadow
同一张图颜色不超过 8 种
正文文字必须满足对比度
标题条可使用语义色
大面积背景禁止高饱和色
```

---

# 八、布局规约

## 1. 统一安全区

```yaml
pageMargin: 32
sectionGapY: 36
sectionGapX: 36
containerHeaderHeight: 44
containerPaddingX: 28
containerPaddingY: 24
cardGapX: 28
cardGapY: 28
tagGapX: 8
tagGapY: 8
```

---

## 2. 防重叠规则

必须校验：

```text
Section Title 与 Card 不重叠
Card 与 Card 不重叠
Tag 与 Tag 不重叠
Card 不超出 Section
箭头标签不遮挡节点
图例不遮挡主图
```

---

## 3. 画布利用率

```text
目标利用率：60%-80%
低于 50%：缩小画布
高于 85%：扩展画布或换行
```

---

# 九、不同图类型的模板规约

## 1. 业务架构图

参考你的业务架构图示例。

结构：

```text
H1 标题
H2 副标题 optional
Section 1：业务场景层
Section 2：业务能力层
Section 3：业务对象层
Footer：分层说明
```

布局：

```text
自上而下
每层一个大容器
容器内为横向卡片网格
卡片内为标签矩阵
```

适合：

```text
业务域
能力地图
对象模型
业务蓝图
```

---

## 2. 应用架构图

参考你的应用架构图示例。

结构：

```text
左：前端/入口
中：网关/核心服务/数据存储
右：外部系统
```

布局：

```text
Left - Center - Right
```

规约：

```text
左侧入口区、中间核心区、右侧外部区必须视觉分区明确
核心系统可以上下分为服务区和数据区
连线从左到右
外部系统连线从核心区向右
```

---

## 3. 技术架构图

参考你的技术分层图示例。

结构不固定，但建议：

```text
展示/接入
网关/协议
业务/服务
基础能力
存储
设备/外部资源
```

规约：

```text
以层为主
层与层之间用横向分隔线或大容器区分
复杂组件可使用嵌套容器
```

---

## 4. 部署架构图

结构：

```text
Region
  VPC
    Subnet
      Cluster
        Node
          Pod / Service
    DB / Cache / MQ
```

规约：

```text
区域嵌套必须清楚
网络边界用虚线或浅色区域
节点需要标注 IP / Port / Protocol
```

---

## 5. 项目时间线图

参考你的项目研发时间线示例。

结构：

```text
H1
H2
主时间线
阶段条
里程碑
右侧说明卡片
底部图例
```

规约：

```text
阶段条必须与时间刻度对齐
颜色代表阶段
右侧说明卡片不能遮挡主时间线
```

---

## 6. 生命周期流程图

参考你的项目研发生命周期图。

结构：

```text
阶段卡片 + 箭头流转 + 里程碑图例 + 交付物区域
```

规约：

```text
主流程优先使用蛇形或网格流转
每个阶段卡片编号
右侧放里程碑图例
底部放角色与交付物
```

---

## 7. 对比图

参考 OpenCode vs OpenClaw 示例。

结构：

```text
H1
H2
左对象卡片
中间 VS
右对象卡片
详细对比表
推荐结论
```

规约：

```text
左右严格对称
两个对象各自拥有独立主色
中间 VS 居中
表格列宽统一
推荐结论放底部
```

---

# 十、核心伪代码

```python
def generate_diagram(user_input):
    intent = parse_intent(user_input)

    template = select_template(intent.diagram_type)

    dsl = plan_structure(
        user_input=user_input,
        template=template,
        rules=[
            "logic_is_model_generated",
            "style_must_follow_template",
            "layout_must_follow_archetype"
        ]
    )

    styled_dsl = resolve_style(
        dsl=dsl,
        theme=intent.theme,
        tokens=load_theme_tokens()
    )

    layout = compute_layout(
        dsl=styled_dsl,
        template=template,
        box_model=load_box_model_rules()
    )

    layout = route_edges(
        layout=layout,
        edge_rules=load_edge_rules()
    )

    layout = validate_and_fix(
        layout=layout,
        checks=[
            "title_overlap",
            "node_overlap",
            "container_bounds",
            "edge_crossing",
            "contrast",
            "canvas_usage",
            "legend_position"
        ]
    )

    xml = render_drawio_xml(layout)

    validate_xml(xml)

    return xml
```

---

# 十一、专门解决前面问题的规约

## 1. 防止标题被遮挡

```text
每个 Section 必须有 Header 区域
Header 高度 >= 44px
节点 y 坐标必须大于 section.y + headerHeight + paddingY
```

---

## 2. 防止元素重叠

```text
任意两个元素之间最小间距 >= 24px
GroupCard 间距 >= 28px
Section 间距 >= 36px
```

---

## 3. 防止颜色看不清

```text
所有文字颜色必须通过 contrast check
深色模式正文禁止使用 #666666 以下灰度
标签背景和文字必须成对生成
```

---

## 4. 防止连线混乱

```text
默认正交线
优先 source/target
禁止穿过 GroupCard
跨 Section 连线必须从容器边缘连接
```

---

## 5. 防止画布空白过大

```text
根据内容 bounding box 自动计算画布
图例、脚注计入内容范围
内容整体居中
```

---

# 十二、最终补充：模板生成要求

你可以把这句话直接写进 `skill.md`：

```markdown
## 模板优先原则

生成图形时，必须先选择最接近的 templates/*.drawio 作为视觉骨架。

- 模板决定：画布比例、标题位置、容器层级、卡片风格、图例位置、箭头风格
- 大模型决定：图形逻辑、分层名称、节点内容、关系说明
- 布局引擎决定：坐标、尺寸、换行、间距
- 校验器决定：是否需要修复重叠、遮挡、空白和颜色对比度

禁止完全脱离模板直接生成 XML。
```

这版方案会比之前更稳，尤其能解决：**标题遮挡、元素重叠、卡片层级混乱、图例缺失、模板缺失导致的自由发挥**。


下面是重新优化后的方案，重点补齐你说的四块：**Skill 项目结构、示例模板、标题/卡片层级规约、图例规约**。

---

# 一、需求定位

这个 Skill 的目标不是简单生成 XML，而是生成 **风格统一、布局稳定、可编辑、可复用的 drawio 架构图/分析图/项目图**。

核心原则：

```text
逻辑结构由大模型推理
视觉风格由规约约束
布局坐标由模板和布局算法控制
最终质量由校验器兜底
```

架构图的逻辑层次不固定，但元素设计、排版、卡片层级、配色、标题、图例、连线风格必须统一。

---

# 二、推荐 Skill 项目结构

```text
xml-diagram/
├── skill.md
│
├── assets/
│   ├── design-system.md              # 全局视觉设计系统
│   ├── theme-tokens.md                # 浅色/深色/语义色 token
│   ├── typography-rules.md            # 标题、正文、标签字号规约
│   ├── component-rules.md             # 容器、卡片、标签、图例组件规约
│   ├── layout-rules.md                # 布局、间距、画布、安全区规约
│   ├── edge-rules.md                  # 连线、箭头、标签、路由规约
│   ├── legend-rules.md                # 图例生成规约
│   ├── validation-rules.md            # 重叠、颜色、画布、XML 校验规则
│   └── dsl-schema.md                  # 中间 DSL 结构定义
│
├── templates/
│   ├── architecture/
│   │   ├── business-layered.drawio     # 业务架构图模板
│   │   ├── application-pipeline.drawio # 应用架构图模板
│   │   ├── technical-layered.drawio    # 技术架构图模板
│   │   └── deployment-region.drawio    # 部署架构图模板
│   │
│   ├── project/
│   │   ├── roadmap-timeline.drawio     # 项目研发时间线模板
│   │   ├── lifecycle-flow.drawio       # 生命周期流程图模板
│   │   └── milestone-board.drawio      # 里程碑看板模板
│   │
│   ├── analysis/
│   │   ├── comparison-vs.drawio        # 对比图模板
│   │   ├── decision-matrix.drawio      # 决策矩阵模板
│   │   └── swot.drawio                 # SWOT 模板
│   │
│   └── summary/
│       ├── article-summary.drawio      # 文章总结图模板
│       ├── knowledge-map.drawio        # 知识结构图模板
│       └── card-summary.drawio         # 卡片总结图模板
│
├── examples/
│   ├── business-architecture-example.drawio
│   ├── application-architecture-example.drawio
│   ├── technical-architecture-example.drawio
│   ├── project-timeline-example.drawio
│   ├── lifecycle-example.drawio
│   └── comparison-example.drawio
│
├── output/
│   └── drawio/
│
└── scripts/
    ├── validate_drawio.py              # XML 与布局校验
    ├── check_contrast.py               # 文字可读性校验
    └── template_preview.py             # 模板预览测试
```

重点是：**templates 和 examples 必须存在**。
否则模型只看规约，还是容易自由发挥。

---

# 三、示例模板的重要性

Skill 里需要明确写：

```text
生成任何图形前，必须优先参考 templates/ 中同类型模板。
模板决定布局骨架、标题层级、卡片层级、图例位置、连线风格。
用户内容只替换模板中的文本、节点数量、关系和局部尺寸。
禁止脱离模板自由布局。
```

推荐模板映射：

| 用户需求    | 优先模板                                                 |
| ------- | ---------------------------------------------------- |
| 业务架构图   | `templates/architecture/business-layered.drawio`     |
| 应用架构图   | `templates/architecture/application-pipeline.drawio` |
| 技术架构图   | `templates/architecture/technical-layered.drawio`    |
| 部署架构图   | `templates/architecture/deployment-region.drawio`    |
| 项目研发时间线 | `templates/project/roadmap-timeline.drawio`          |
| 项目生命周期  | `templates/project/lifecycle-flow.drawio`            |
| 对比图     | `templates/analysis/comparison-vs.drawio`            |
| 文章总结图   | `templates/summary/article-summary.drawio`           |

---

# 四、标题层级规约

## 1. 页面标题 H1

用于整张图标题。

```yaml
H1:
  fontSize: 24
  fontStyle: bold
  align: center
  color: title
  marginTop: 20
  marginBottom: 8
```

示例：

```text
业务架构图设计案例
应用架构图设计案例
项目研发生命周期流程图
```

---

## 2. 页面副标题 H2

用于英文说明或补充说明。

```yaml
H2:
  fontSize: 12
  color: subtext
  align: center
  marginBottom: 24
```

示例：

```text
Business Architecture Design
Software Development Life Cycle
```

---

## 3. 区域标题 Section Title

用于大容器标题。

```yaml
SectionTitle:
  fontSize: 18
  fontStyle: bold
  color: sectionColor
  align: left
  height: 44
```

示例：

```text
业务场景层（Business Scenario Layer）
业务能力层（Business Capability Layer）
业务对象层（Business Object Layer）
```

强制规则：

```text
区域标题必须拥有独立 Header 安全区
节点不得覆盖区域标题
Header 高度不得小于 44px
```

---

## 4. 卡片标题 Card Title

用于一级卡片标题。

```yaml
CardTitle:
  fontSize: 14
  fontStyle: bold
  color: "#ffffff"
  align: center
  height: 34
```

---

## 5. 内容标签 Item Tag

用于卡片内部的小能力点。

```yaml
ItemTag:
  fontSize: 10
  color: text
  height: 22
  borderRadius: 6
  paddingX: 8
```

---

# 五、卡片层级规约

必须明确几级卡片，否则模型会乱摆。

## Level 0：Page

整张图。

```text
Page = Title + Content + Footer/Legend
```

---

## Level 1：Section Container

大区域容器。

用于：

```text
业务场景层
业务能力层
业务对象层
前端应用层
后端服务层
外部系统层
关键里程碑
各阶段角色与交付物
```

规约：

```yaml
SectionContainer:
  rounded: 1
  arcSize: 12
  strokeWidth: 2
  fillColor: container_bg
  paddingX: 28
  paddingY: 24
  headerHeight: 44
```

禁止：

```text
节点进入 Section Header 区域
Section 内部没有 padding
多个 Section 间距小于 32px
```

---

## Level 2：Group Card

中型卡片，用于领域、模块、阶段、系统。

例如：

```text
用户管理域
商品管理域
API 网关
用户中心
设计阶段
开发阶段
```

规约：

```yaml
GroupCard:
  width: 180-260
  height: auto
  minHeight: 86
  rounded: 1
  arcSize: 10
  strokeWidth: 2
  headerHeight: 34
  bodyPadding: 12
```

---

## Level 3：Item Tag

小标签，用于能力点、技术点、属性。

例如：

```text
注册登录
信息管理
Spring Boot
Redis
Prometheus
```

规约：

```yaml
ItemTag:
  width: auto
  minWidth: 54
  height: 22
  gapX: 8
  gapY: 8
  rounded: 1
  arcSize: 6
```

---

## Level 4：Annotation

说明、脚注、备注。

```yaml
Annotation:
  fontSize: 11
  color: subtext
  align: center
```

---

# 六、图例规约

图例不是可选项，满足以下任一条件必须生成：

```text
使用了 4 种以上语义色
存在虚线/实线/主链路区别
存在阶段颜色
存在角色颜色
存在系统边界颜色
```

## 图例位置

优先级：

```text
右侧独立图例区
底部横向图例区
右下角悬浮图例
```

禁止：

```text
图例覆盖主内容
图例放在主流程中间
图例与节点间距小于 24px
```

## 图例类型

### 1. 颜色图例

```text
蓝色 = 用户/前端/需求
绿色 = 服务/能力/通过
橙色 = 外部系统/设计/警告
红色 = 错误/风险/开发重点
紫色 = 测试/异步/对比对象
青色 = 部署/发布/通信
```

### 2. 线型图例

```text
实线箭头 = 同步调用/主流程
虚线箭头 = 异步消息/回调
粗箭头 = 主链路
红色实线 = 异常/失败路径
```

### 3. 阶段图例

适用于项目周期图：

```text
需求
立项
设计
开发
测试
部署
运维
迭代
```

---

# 七、统一风格规约

## 浅色模式

```yaml
bg: "#f8fafc"
container_bg: "#f1f5f9"
card_bg: "#ffffff"
border: "#cbd5e1"
title: "#0f172a"
text: "#334155"
subtext: "#64748b"
line: "#94a3b8"
```

## 深色模式

```yaml
bg: "#0f172a"
container_bg: "#111827"
card_bg: "#1e293b"
border: "#334155"
title: "#f8fafc"
text: "#cbd5e1"
subtext: "#94a3b8"
line: "#64748b"
```

## 强制规则

```text
深色模式禁止 shadow
浅色模式允许轻微 shadow
同一张图颜色不超过 8 种
正文文字必须满足对比度
标题条可使用语义色
大面积背景禁止高饱和色
```

---

# 八、布局规约

## 1. 统一安全区

```yaml
pageMargin: 32
sectionGapY: 36
sectionGapX: 36
containerHeaderHeight: 44
containerPaddingX: 28
containerPaddingY: 24
cardGapX: 28
cardGapY: 28
tagGapX: 8
tagGapY: 8
```

---

## 2. 防重叠规则

必须校验：

```text
Section Title 与 Card 不重叠
Card 与 Card 不重叠
Tag 与 Tag 不重叠
Card 不超出 Section
箭头标签不遮挡节点
图例不遮挡主图
```

---

## 3. 画布利用率

```text
目标利用率：60%-80%
低于 50%：缩小画布
高于 85%：扩展画布或换行
```

---

# 九、不同图类型的模板规约

## 1. 业务架构图

参考你的业务架构图示例。

结构：

```text
H1 标题
H2 副标题 optional
Section 1：业务场景层
Section 2：业务能力层
Section 3：业务对象层
Footer：分层说明
```

布局：

```text
自上而下
每层一个大容器
容器内为横向卡片网格
卡片内为标签矩阵
```

适合：

```text
业务域
能力地图
对象模型
业务蓝图
```

---

## 2. 应用架构图

参考你的应用架构图示例。

结构：

```text
左：前端/入口
中：网关/核心服务/数据存储
右：外部系统
```

布局：

```text
Left - Center - Right
```

规约：

```text
左侧入口区、中间核心区、右侧外部区必须视觉分区明确
核心系统可以上下分为服务区和数据区
连线从左到右
外部系统连线从核心区向右
```

---

## 3. 技术架构图

参考你的技术分层图示例。

结构不固定，但建议：

```text
展示/接入
网关/协议
业务/服务
基础能力
存储
设备/外部资源
```

规约：

```text
以层为主
层与层之间用横向分隔线或大容器区分
复杂组件可使用嵌套容器
```

---

## 4. 部署架构图

结构：

```text
Region
  VPC
    Subnet
      Cluster
        Node
          Pod / Service
    DB / Cache / MQ
```

规约：

```text
区域嵌套必须清楚
网络边界用虚线或浅色区域
节点需要标注 IP / Port / Protocol
```

---

## 5. 项目时间线图

参考你的项目研发时间线示例。

结构：

```text
H1
H2
主时间线
阶段条
里程碑
右侧说明卡片
底部图例
```

规约：

```text
阶段条必须与时间刻度对齐
颜色代表阶段
右侧说明卡片不能遮挡主时间线
```

---

## 6. 生命周期流程图

参考你的项目研发生命周期图。

结构：

```text
阶段卡片 + 箭头流转 + 里程碑图例 + 交付物区域
```

规约：

```text
主流程优先使用蛇形或网格流转
每个阶段卡片编号
右侧放里程碑图例
底部放角色与交付物
```

---

## 7. 对比图

参考 OpenCode vs OpenClaw 示例。

结构：

```text
H1
H2
左对象卡片
中间 VS
右对象卡片
详细对比表
推荐结论
```

规约：

```text
左右严格对称
两个对象各自拥有独立主色
中间 VS 居中
表格列宽统一
推荐结论放底部
```

---

# 十、核心伪代码

```python
def generate_diagram(user_input):
    intent = parse_intent(user_input)

    template = select_template(intent.diagram_type)

    dsl = plan_structure(
        user_input=user_input,
        template=template,
        rules=[
            "logic_is_model_generated",
            "style_must_follow_template",
            "layout_must_follow_archetype"
        ]
    )

    styled_dsl = resolve_style(
        dsl=dsl,
        theme=intent.theme,
        tokens=load_theme_tokens()
    )

    layout = compute_layout(
        dsl=styled_dsl,
        template=template,
        box_model=load_box_model_rules()
    )

    layout = route_edges(
        layout=layout,
        edge_rules=load_edge_rules()
    )

    layout = validate_and_fix(
        layout=layout,
        checks=[
            "title_overlap",
            "node_overlap",
            "container_bounds",
            "edge_crossing",
            "contrast",
            "canvas_usage",
            "legend_position"
        ]
    )

    xml = render_drawio_xml(layout)

    validate_xml(xml)

    return xml
```

---

# 十一、专门解决前面问题的规约

## 1. 防止标题被遮挡

```text
每个 Section 必须有 Header 区域
Header 高度 >= 44px
节点 y 坐标必须大于 section.y + headerHeight + paddingY
```

---

## 2. 防止元素重叠

```text
任意两个元素之间最小间距 >= 24px
GroupCard 间距 >= 28px
Section 间距 >= 36px
```

---

## 3. 防止颜色看不清

```text
所有文字颜色必须通过 contrast check
深色模式正文禁止使用 #666666 以下灰度
标签背景和文字必须成对生成
```

---

## 4. 防止连线混乱

```text
默认正交线
优先 source/target
禁止穿过 GroupCard
跨 Section 连线必须从容器边缘连接
```

---

## 5. 防止画布空白过大

```text
根据内容 bounding box 自动计算画布
图例、脚注计入内容范围
内容整体居中
```

---

# 十二、最终补充：模板生成要求

你可以把这句话直接写进 `skill.md`：

```markdown
## 模板优先原则

生成图形时，必须先选择最接近的 templates/*.drawio 作为视觉骨架。

- 模板决定：画布比例、标题位置、容器层级、卡片风格、图例位置、箭头风格
- 大模型决定：图形逻辑、分层名称、节点内容、关系说明
- 布局引擎决定：坐标、尺寸、换行、间距
- 校验器决定：是否需要修复重叠、遮挡、空白和颜色对比度

禁止完全脱离模板直接生成 XML。
```

这版方案会比之前更稳，尤其能解决：**标题遮挡、元素重叠、卡片层级混乱、图例缺失、模板缺失导致的自由发挥**。
