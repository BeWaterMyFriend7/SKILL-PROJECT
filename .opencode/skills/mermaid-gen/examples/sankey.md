# 用户转化流向

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Noto Sans SC, Microsoft YaHei, sans-serif","primaryColor":"#FFFFFF","primaryBorderColor":"#2563EB","primaryTextColor":"#172033","lineColor":"#64748B","background":"#F6F8FB"}}}%%
sankey-beta
Visit,Product View,1000
Product View,Add to Cart,420
Product View,Exit,580
Add to Cart,Submit Order,260
Add to Cart,Exit,160
Submit Order,Payment Success,210
Submit Order,Payment Failed,50
```

## 说明

- 数值表示“访问—浏览商品—加购—下单—支付”各阶段间的用户数量。
- Sankey 当前解析器对非 ASCII 标签兼容性不稳定，示例用英文标签保证跨版本渲染。
