#!/usr/bin/env python3
"""
Extract experience bullet points from a .docx resume.

Outputs a JSON file mapping a stable bullet ID -> current text, plus enough
context (the section/heading each bullet falls under) for an LLM to rewrite it
intelligently. The ID is the paragraph's index in the document body, which is
stable as long as we only *edit text* and never add/remove paragraphs.

Usage:
    python extract_bullets.py <resume.docx> [--out bullets.json]
"""
import argparse
import json
import sys

from docx import Document
from docx.oxml.ns import qn


def iter_block_paragraphs(doc):
    """Yield (index, paragraph) for every paragraph in document body order."""
    for i, p in enumerate(doc.paragraphs):
        yield i, p


def is_bullet(paragraph) -> bool:
    """
    Heuristic: a paragraph is a bullet/list item if it has numbering properties
    (numPr) in its paragraph properties, OR its style name suggests a list.
    Many resumes use real Word bullets (numPr); some fake them with a leading
    dash/•. We catch both.
    """
    pPr = paragraph._p.pPr
    if pPr is not None and pPr.find(qn("w:numPr")) is not None:
        return True
    style = (paragraph.style.name or "").lower() if paragraph.style else ""
    if "list" in style or "bullet" in style:
        return True
    text = paragraph.text.strip()
    if text[:1] in {"•", "-", "–", "—", "▪", "◦", "‣", "*"}:
        return True
    return False


def looks_like_heading(paragraph) -> bool:
    style = (paragraph.style.name or "").lower() if paragraph.style else ""
    if "heading" in style or "title" in style:
        return True
    # Bold-only short lines often act as section/role headers in resumes.
    text = paragraph.text.strip()
    if not text or len(text) > 90:
        return False
    runs = [r for r in paragraph.runs if r.text.strip()]
    if runs and all(r.bold for r in runs):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--out", default="bullets.json")
    args = ap.parse_args()

    doc = Document(args.docx)

    bullets = []
    current_context = ""
    for idx, p in iter_block_paragraphs(doc):
        text = p.text.strip()
        if not text:
            continue
        if looks_like_heading(p) and not is_bullet(p):
            current_context = text
            continue
        if is_bullet(p):
            bullets.append(
                {
                    "id": idx,
                    "context": current_context,
                    "text": text,
                    "style": p.style.name if p.style else None,
                }
            )

    payload = {
        "source": args.docx,
        "bullet_count": len(bullets),
        "bullets": bullets,
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(bullets)} bullet(s) -> {args.out}", file=sys.stderr)
    for b in bullets:
        ctx = f" [{b['context']}]" if b["context"] else ""
        print(f"  #{b['id']}{ctx}: {b['text'][:80]}", file=sys.stderr)


if __name__ == "__main__":
    main()
