"""
links_to_pdf.py
---------------
Given an array of URLs, fetches each page, extracts its content,
and produces a single well-formatted PDF report.

Requirements:
    pip install requests beautifulsoup4 reportlab
"""

import sys
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, PageBreak, Table, TableStyle
)


# ── Configuration ────────────────────────────────────────────────────────────

LINKS = [
    "https://attack.mitre.org/techniques/T1657/",
    # Add your own URLs here
]

OUTPUT_PDF = "output.pdf"

REQUEST_TIMEOUT = 15          # seconds per request
MAX_PARAGRAPHS_PER_PAGE = 40  # cap content per site to keep PDF manageable


# ── Fetching & Parsing ───────────────────────────────────────────────────────

def fetch_page(url: str) -> dict:
    """
    Fetch a URL and return a dict with:
        title, url, paragraphs (list[str]), error (str|None)
    """
    result = {"url": url, "title": url, "paragraphs": [], "error": None}
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; LinkToPDF/1.0)"}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Title
        title_tag = soup.find("title")
        if title_tag and title_tag.get_text(strip=True):
            result["title"] = title_tag.get_text(strip=True)

        # Remove noisy tags
        for tag in soup(["script", "style", "nav", "footer",
                          "header", "aside", "form", "noscript"]):
            tag.decompose()

        # Collect paragraphs from <p>, <h1>–<h4>
        paragraphs = []
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p"]):
            text = el.get_text(separator=" ", strip=True)
            text = re.sub(r"\s+", " ", text)
            if len(text) > 30:   # skip very short snippets
                paragraphs.append((el.name, text))

        result["paragraphs"] = paragraphs[:MAX_PARAGRAPHS_PER_PAGE]

    except requests.exceptions.RequestException as exc:
        result["error"] = str(exc)

    return result


# ── PDF Building ─────────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#555555"),
            spaceAfter=6,
        ),
        "site_title": ParagraphStyle(
            "site_title",
            parent=base["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#16213e"),
            spaceBefore=6,
            spaceAfter=4,
        ),
        "url_label": ParagraphStyle(
            "url_label",
            parent=base["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#0f3460"),
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#16213e"),
            spaceBefore=8,
            spaceAfter=3,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontSize=11,
            textColor=colors.HexColor("#333333"),
            spaceBefore=6,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#222222"),
            spaceAfter=6,
        ),
        "error": ParagraphStyle(
            "error",
            parent=base["Normal"],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=6,
        ),
        "toc_header": ParagraphStyle(
            "toc_header",
            parent=base["Heading1"],
            fontSize=16,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=10,
        ),
        "toc_item": ParagraphStyle(
            "toc_item",
            parent=base["Normal"],
            fontSize=10,
            leading=16,
            textColor=colors.HexColor("#0f3460"),
            spaceAfter=2,
        ),
    }
    return styles


HEADING_STYLE_MAP = {
    "h1": "site_title",
    "h2": "h2",
    "h3": "h3",
    "h4": "h3",
}


def safe_paragraph(text: str, style) -> Paragraph:
    """Escape special XML chars that break ReportLab."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(text, style)


def build_pdf(pages: list[dict], output_path: str, styles: dict):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title="Web Pages Report",
        author="links_to_pdf.py",
    )

    story = []
    now = datetime.now().strftime("%B %d, %Y  %H:%M")

    # ── Cover page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5 * inch))
    story.append(safe_paragraph("Web Pages Report", styles["cover_title"]))
    story.append(HRFlowable(width="100%", thickness=2,
                             color=colors.HexColor("#0f3460")))
    story.append(Spacer(1, 0.2 * inch))
    story.append(safe_paragraph(f"Generated: {now}", styles["cover_sub"]))
    story.append(safe_paragraph(
        f"Total sources: {len(pages)}", styles["cover_sub"]))
    story.append(PageBreak())

    # ── Table of contents ───────────────────────────────────────────────────
    story.append(safe_paragraph("Table of Contents", styles["toc_header"]))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1 * inch))

    for i, page in enumerate(pages, 1):
        label = f"{i}.  {page['title']}"
        story.append(safe_paragraph(label, styles["toc_item"]))
        story.append(safe_paragraph(page["url"], styles["url_label"]))

    story.append(PageBreak())

    # ── One section per URL ─────────────────────────────────────────────────
    for i, page in enumerate(pages, 1):
        # Section header
        story.append(safe_paragraph(
            f"{i}. {page['title']}", styles["site_title"]))
        story.append(safe_paragraph(page["url"], styles["url_label"]))
        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 0.1 * inch))

        if page["error"]:
            story.append(safe_paragraph(
                f"Could not fetch page: {page['error']}", styles["error"]))
        elif not page["paragraphs"]:
            story.append(safe_paragraph(
                "No readable content found.", styles["body"]))
        else:
            for tag, text in page["paragraphs"]:
                style_key = HEADING_STYLE_MAP.get(tag, "body")
                story.append(safe_paragraph(text, styles[style_key]))

        # Don't add a page break after the last entry
        if i < len(pages):
            story.append(PageBreak())

    doc.build(story)


# ── Main ─────────────────────────────────────────────────────────────────────

def main(links: list[str] | None = None, output: str = OUTPUT_PDF):
    urls = links or LINKS
    if not urls:
        print("No URLs provided. Add them to the LINKS list or pass them as arguments.")
        sys.exit(1)

    print(f"Processing {len(urls)} URL(s)...\n")
    pages = []
    for url in urls:
        print(f"  Fetching: {url}")
        data = fetch_page(url)
        if data["error"]:
            print(f"    ⚠  Error: {data['error']}")
        else:
            print(f"    ✓  '{data['title']}' — {len(data['paragraphs'])} block(s)")
        pages.append(data)

    print(f"\nBuilding PDF → {output}")
    styles = build_styles()
    build_pdf(pages, output, styles)
    print("Done! ✔")


if __name__ == "__main__":
    # Optional: pass URLs as command-line arguments
    #   python links_to_pdf.py https://example.com https://another.com
    cli_links = sys.argv[1:] if len(sys.argv) > 1 else None
    main(links=cli_links)