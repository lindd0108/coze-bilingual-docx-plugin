# create_bilingual_docx 插件服务

这个服务用于给 Coze 自定义插件提供一个稳定的双语对照 Word 生成 API。

它不依赖 Markdown 表格解析，而是接收结构化 `rows`，用 `python-docx` 直接生成真正的 Word 两列表格。

## API

`POST /create_bilingual_docx`

输入：

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
      "term": "杜甫",
      "translation": "Du Fu",
      "note": "首次出现可补充 style name Zimei"
    }
  ],
  "risks": ["杜预官爵译法需复核"]
}
```

输出：

```json
{
  "file_url": "https://your-domain/files/xxx.docx",
  "file_name": "杜甫评传第一章：未坠素业的家世.docx",
  "row_count": 1,
  "message": "created"
}
```

## 本地运行（无 FastAPI 版本）

```powershell
cd D:\lwq\projects\cozeProject\bilingual_docx_plugin
python stdlib_server.py
```

本地测试：

```powershell
python test_client.py
```

## Coze 插件配置

Coze 基于 API 创建插件时，插件 URL 必须是域名，不能是 IP。需要先把这个服务部署到公网域名，例如：

- 云服务器 + Nginx + HTTPS 域名
- Render / Railway / Fly.io 等托管平台
- Cloudflare Tunnel 绑定域名

然后在 Coze 中：

1. 资源库 -> +资源 -> 插件。
2. 插件工具创建方式选择：云侧插件 - 基于已有服务创建。
3. 插件 URL 填写你的公网域名，例如 `https://docx.example.com`。
4. 创建工具：
   - 名称：`create_bilingual_docx`
   - 路径：`/create_bilingual_docx`
   - 方法：`POST`
5. 输入参数选择 Body，按 `openapi.yaml` 中的 schema 配置。
6. 输出参数配置：
   - `file_url`: String
   - `file_name`: String
   - `row_count`: Integer
   - `message`: String
7. 试运行成功后发布插件，再添加到“诗史译衡”智能体。

## 智能体调用要求

提示词中应要求模型调用插件时传结构化 rows，不要传 Markdown 表格：

```text
生成 Word 双语对照文档时，必须调用 create_bilingual_docx。
rows 中每个元素对应一个自然段：
- source: 中文原文
- target: 英文译文
不得把 Markdown 表格传给插件。
```
