from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

from docx_builder import build_docx


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated"


class Handler(BaseHTTPRequestHandler):
    server_version = "BilingualDocxPlugin/1.0"

    def send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"status": "ok"})
            return
        if parsed.path.startswith("/files/"):
            file_name = unquote(parsed.path.removeprefix("/files/"))
            path = OUTPUT_DIR / file_name
            resolved_output_dir = OUTPUT_DIR.resolve()
            resolved_path = path.resolve()
            if (
                resolved_output_dir not in resolved_path.parents
                or not path.exists()
                or path.suffix.lower() != ".docx"
            ):
                self.send_json(404, {"detail": "file not found"})
                return
            data = path.read_bytes()
            self.send_response(200)
            self.send_header(
                "Content-Type",
                mimetypes.guess_type(path.name)[0]
                or "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            encoded_name = quote(path.name)
            self.send_header(
                "Content-Disposition",
                f"attachment; filename*=UTF-8''{encoded_name}",
            )
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_json(404, {"detail": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/create_bilingual_docx":
            self.send_json(404, {"detail": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            result = build_docx(payload, OUTPUT_DIR)
            host = self.headers.get("X-Forwarded-Host") or self.headers.get("Host", "")
            proto = self.headers.get("X-Forwarded-Proto") or "http"
            base_url = f"{proto}://{host}".rstrip("/")
            self.send_json(
                200,
                {
                    "file_url": f"{base_url}/files/{quote(result['file_name'])}",
                    "file_name": result["file_name"],
                    "row_count": result["row_count"],
                    "message": "created",
                },
            )
        except ValueError as exc:
            self.send_json(400, {"detail": str(exc)})
        except Exception as exc:
            self.send_json(500, {"detail": str(exc)})


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
