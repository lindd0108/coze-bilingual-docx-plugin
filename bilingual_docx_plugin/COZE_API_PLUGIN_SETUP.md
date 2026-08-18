# Coze API 插件填写清单

部署完成后，你会得到一个 HTTPS 域名，例如：

```text
https://bilingual-docx-plugin.onrender.com
```

下面所有示例里的域名都替换成你自己的部署域名。

## 1. 创建插件

创建方式：

```text
云侧插件 - 基于已有服务创建
```

插件 URL：

```text
https://你的部署域名
```

插件名称：

```text
中英文对照输出
```

插件描述：

```text
生成中英文左右两列对照的 Word 文档，返回可下载的 docx 文件链接。用于解决 Markdown 表格无法稳定写入 Word 文档的问题。
```

## 2. 创建工具

工具名称：

```text
create_bilingual_docx
```

工具介绍：

```text
根据结构化的中英文段落数据生成左右两列对照的 Word 文档。输入必须包含文档标题 title 和 rows 数组，rows 中每一项包含中文原文 source 与英文译文 target；可选输入 terms 用于术语说明，risks 用于风险提示。工具返回 file_url，智能体应把该链接提供给用户下载。
```

请求方式：

```text
POST
```

路径：

```text
/create_bilingual_docx
```

Content-Type：

```text
application/json
```

## 3. 输入参数

Body JSON：

```json
{
  "title": "杜甫评传第一章：未坠素业的家世",
  "rows": [
    {
      "source": "杜甫，字子美。",
      "target": "Du Fu, style name Zimei."
    }
  ],
  "terms": [
    {
      "term": "字子美",
      "translation": "style name Zimei",
      "note": "首次出现补注"
    }
  ],
  "risks": [
    "专名译法需与全书保持一致"
  ],
  "decision_logs": [
    {
      "item": "字子美",
      "decision": "首次出现译为 style name Zimei",
      "reason": "向英语学术读者说明“字”的称谓功能",
      "memory": "建议写入项目记忆",
      "review": "否"
    }
  ]
}
```

参数类型：

```text
title   String          必填
rows    Array<Object>   必填
terms   Array<Object>   选填
risks   Array<String>   选填
decision_logs Array<Object> 选填
```

rows 子字段：

```text
source  String  中文原文
target  String  英文译文
```

terms 子字段：

```text
term         String  中文术语
translation  String  推荐英译
note         String  说明
```

decision_logs 子字段：

```text
item      String  决策对象、术语或片段
decision  String  采用的译法或处理决定
reason    String  决策理由
memory    String  是否写入项目记忆
review    String  是否需要后续复核
```

## 4. 输出参数

```text
file_url    String   生成的 docx 下载链接
file_name   String   生成的 docx 文件名
row_count   Integer  写入 Word 主表格的中英对照行数
message     String   生成状态
```

## 5. 智能体提示词补充

```text
当用户要求生成 Word/docx 双语对照文档时，必须调用 create_bilingual_docx 工具。
调用工具时不得传 Markdown 表格或 HTML，必须传结构化 JSON：
- title: 文档标题
- rows: 中英对照段落数组，每项包含 source 和 target
- terms: 可选，术语说明
- risks: 可选，风险提示
- decision_logs: 可选，译者决策日志

工具返回 file_url 后，应直接回复用户下载链接，并说明该文档为左右两列中英对照 Word 文档。
```
