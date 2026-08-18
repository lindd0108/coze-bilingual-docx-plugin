from __future__ import annotations

import json
import urllib.request


payload = {
    "title": "杜甫评传第一章：未坠素业的家世",
    "rows": [
        {
            "source": "杜甫，字子美。",
            "target": "Du Fu, style name Zimei.",
        },
        {
            "source": "杜甫的十三世祖是晋代的名将当阳侯杜预。",
            "target": "Du Fu's thirteenth-generation ancestor was Du Yu, Marquis of Dangyang, a celebrated general of the Jin dynasty.",
        },
    ],
    "terms": [
        {
            "term": "杜甫",
            "translation": "Du Fu",
            "note": "首次出现可补充 style name Zimei。",
        }
    ],
    "risks": ["杜预官爵译法需按项目术语库复核。"],
    "decision_logs": [
        {
            "item": "字子美",
            "decision": "译为 style name Zimei",
            "reason": "首次出现时说明“字”的称谓功能，便于英语学术读者理解。",
            "memory": "建议写入项目记忆",
            "review": "否",
        },
        {
            "item": "当阳侯",
            "decision": "暂译为 Marquis of Dangyang",
            "reason": "保留爵号与封地信息，但爵位系统对应关系仍需复核。",
            "memory": "暂不写入",
            "review": "是",
        },
    ],
}


request = urllib.request.Request(
    "http://127.0.0.1:8000/create_bilingual_docx",
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
with opener.open(request) as response:
    print(response.read().decode("utf-8"))
