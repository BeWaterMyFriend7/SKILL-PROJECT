# prototype-design-html 测试示例

测试环境：Codex Desktop，本地 Chromium 浏览器；红包运营原型使用 1440×810 和 1280×720，消息聊天原型使用 1440×900。

## 示例一：红包运营后台

> 现在有一个抢红包系统，请使用 prototype-design-html 绘制红包运营后台原型，包含运营概览、红包活动列表、创建红包和领取记录。要求页面之间可以切换，活动可以查询，详情弹窗可以打开和关闭，创建红包需要表单校验；整体采用简约浅色原型风格，不使用阴影、渐变和背景网格。

### 浏览器截图

#### 运营概览

![运营概览](images/red-packet-overview.png)

#### 红包活动列表

![红包活动列表](images/red-packet-activities.png)

#### 创建红包

![创建红包](images/red-packet-create.png)

## 示例二：消息聊天

> 请使用 prototype-design-html 绘制桌面端消息聊天原型，包含联系人列表、联系人搜索、会话切换、消息历史、在线状态、消息输入和发送操作；整体使用简约浅色布局，不使用阴影、渐变和背景网格。

### 浏览器截图

![消息聊天原型](images/chat-prototype.png)

## 文件索引

| 原型 | 文件 |
| --- | --- |
| 红包运营后台 HTML 原型 | [red-packet-prototype.html](html/red-packet-prototype.html) |
| 消息聊天 HTML 原型 | [chat-prototype.html](html/chat-prototype.html) |

## 验证范围

- 概览、活动、创建和领取记录四个页面可以切换。
- 活动名称与状态查询、重置和空结果状态可用。
- 活动详情弹窗可以打开、关闭并点击遮罩关闭。
- 创建表单可以显示必填错误，填写有效内容后可以提交。
- 消息聊天原型支持联系人搜索、会话切换和消息发送，发送后会同步更新会话预览。
- 浏览器控制台无错误，页面无外部资源依赖。
- 对应测试视口下无元素重叠、文字截断和异常大面积空白。
