from pathlib import Path

from docx_builder import build_docx


payload = {
    "title": "杜甫评传第一章：未坠素业的家世",
    "rows": [
        {
            "source": "杜甫，字子美。",
            "target": "Du Fu, style name Zimei.",
        },
        {
            "source": "杜甫的十三世祖是晋代的名将当阳侯杜预。",
            "target": "Du Fu's thirteenth-generation ancestor was Du Yu, Marquis of Dangyang.",
        },
    ],
    "terms": [
        {
            "term": "杜甫",
            "translation": "Du Fu",
            "note": "首次出现可补充 style name Zimei。",
        }
    ],
    "risks": ["杜预官爵译法需复核。"],
}


if __name__ == "__main__":
    result = build_docx(payload, Path(__file__).resolve().parent / "generated")
    print(result)
