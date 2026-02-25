from __future__ import annotations

import pymupdf
import requests
from fastmcp import FastMCP

MAX_OUTPUT_CHARS = 40_000
REQUEST_TIMEOUT_SECONDS = 30

mcp = FastMCP("pdf-tools")

fake_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.75/76 Safari/537.36"
}

@mcp.tool
def extract_pdf_from_url(url: str) -> str:
    """**USE THIS FOR URLs THAT POINT TO A PDF**. Fetch a PDF from a URL and return its content as Markdown (max 20,000 chars)."""
    response = requests.get(url, headers=fake_headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    content_type = (response.headers.get("Content-Type") or "").lower()
    if "pdf" not in content_type:# and not url.lower().endswith(".pdf"):
        raise ValueError("URL does not appear to point to a PDF.")

    doc = pymupdf.open(stream=response.content, filetype="pdf")

    markdown_parts: list[str] = []
    try:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            markdown_parts.append(f"## Page {i}\\n\\n{text}")
    finally:
        doc.close()

    markdown = "\\n\\n".join(markdown_parts).strip()

    if len(markdown) > MAX_OUTPUT_CHARS:
        markdown = markdown[:MAX_OUTPUT_CHARS] + " ... (truncated)"

    return markdown


if __name__ == "__main__":
    mcp.run()
