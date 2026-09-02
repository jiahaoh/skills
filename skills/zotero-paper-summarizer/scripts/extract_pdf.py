#!/usr/bin/env python3
"""Extract a Zotero PDF to cleaned Markdown with a quality-gated image fallback.

Usage:
    python3 extract_pdf.py <zotero-item-key | /path/to.pdf>

Exit codes:
    0  good text extracted; read OUTPUT
    3  poor text layer; inspect IMAGES
    2  PDF resolution or extraction failed; inspect NOTE
"""

import glob
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile


ZOTERO_DIR = os.path.expanduser(os.environ.get("ZOTERO_DATA_DIR", "~/Zotero"))
STORAGE_DIR = os.path.join(ZOTERO_DIR, "storage")
DB_PATH = os.path.join(ZOTERO_DIR, "zotero.sqlite")

MIN_CHARS_PER_PAGE = 120
MAX_GARBLED_RATIO = 0.03
RENDER_DPI = 150
MAX_RENDER_PAGES = 30


def resolve_pdf(arg):
    """Return an absolute PDF path for a path or a Zotero parent/attachment key."""
    if os.path.isfile(arg) and arg.lower().endswith(".pdf"):
        return os.path.abspath(arg)
    if not os.path.exists(DB_PATH):
        return None

    fd, tmp_db = tempfile.mkstemp(prefix="zotero_read_", suffix=".sqlite")
    os.close(fd)
    rows = []
    try:
        shutil.copyfile(DB_PATH, tmp_db)
        con = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        try:
            cur = con.cursor()
            rows = list(
                cur.execute(
                    """SELECT ai.key, ia.path FROM items pi
                       JOIN itemAttachments ia ON ia.parentItemID = pi.itemID
                       JOIN items ai ON ai.itemID = ia.itemID
                       WHERE pi.key = ? AND ia.contentType = 'application/pdf'""",
                    (arg,),
                )
            )
            if not rows:
                rows = list(
                    cur.execute(
                        """SELECT i.key, ia.path FROM items i
                           JOIN itemAttachments ia ON ia.itemID = i.itemID
                           WHERE i.key = ? AND ia.contentType = 'application/pdf'""",
                        (arg,),
                    )
                )
        finally:
            con.close()
    finally:
        try:
            os.remove(tmp_db)
        except OSError:
            pass

    for attachment_key, stored_path in rows:
        if not stored_path:
            continue
        if stored_path.startswith("storage:"):
            candidate = os.path.join(
                STORAGE_DIR, attachment_key, stored_path[len("storage:") :]
            )
        else:
            candidate = os.path.expanduser(stored_path.replace("attachments:", ""))
        if os.path.isfile(candidate):
            return candidate

        attachment_dir = os.path.join(STORAGE_DIR, attachment_key)
        hits = sorted(glob.glob(os.path.join(attachment_dir, "*.pdf")))
        if hits:
            return hits[0]
    return None


def strip_noise(pages):
    """Remove recurring short boilerplate and standalone page/line numbers."""
    page_count = len(pages)
    frequency = {}
    for page in pages:
        seen = set()
        for line in page.splitlines():
            stripped = line.strip()
            if stripped and len(stripped) < 80:
                key = re.sub(r"\s+", " ", stripped.lower())
                if key not in seen:
                    seen.add(key)
                    frequency[key] = frequency.get(key, 0) + 1

    boilerplate = {
        key
        for key, count in frequency.items()
        if count >= max(3, int(0.5 * page_count))
    }
    kept = []
    for page in pages:
        for line in page.splitlines():
            stripped = line.strip()
            key = re.sub(r"\s+", " ", stripped.lower())
            if stripped and key in boilerplate:
                continue
            if re.fullmatch(r"[-–—\s]*\d{1,4}[-–—\s]*", stripped):
                continue
            kept.append(line)

    text = "\n".join(kept)
    if len(re.findall(r"(?m)^\s*\d{1,4}\s*$", text)) > 20:
        text = re.sub(r"(?m)^\s*\d{1,4}\s*$\n?", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def garbled_ratio(text):
    if not text:
        return 1.0
    bad = sum(
        1
        for char in text
        if char == "�" or (ord(char) < 32 and char not in "\n\r\t")
    )
    return bad / len(text)


def safe_key(arg):
    base = arg if os.path.sep not in arg else os.path.splitext(os.path.basename(arg))[0]
    return re.sub(r"[^A-Za-z0-9._-]", "_", base) or "paper"


def poppler_page_count(pdf_path, fallback):
    if not shutil.which("pdfinfo"):
        return fallback
    result = subprocess.run(
        ["pdfinfo", pdf_path], capture_output=True, text=True, check=False
    )
    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", result.stdout)
    return int(match.group(1)) if match else fallback


def extract_with_poppler(pdf_path):
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext is not installed")
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", pdf_path, "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    pages = result.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages or [result.stdout]


def render_images(pdf_path, key, total_hint):
    output_dir = tempfile.mkdtemp(prefix=f"zotero_pages_{key}_")
    try:
        import fitz

        doc = fitz.open(pdf_path)
        try:
            total = len(doc)
            paths = []
            for index in range(min(total, MAX_RENDER_PAGES)):
                pixmap = doc[index].get_pixmap(dpi=RENDER_DPI)
                path = os.path.join(output_dir, f"p{index + 1:03d}.png")
                pixmap.save(path)
                paths.append(path)
        finally:
            doc.close()
        return output_dir, len(paths), total
    except ImportError:
        if not shutil.which("pdftoppm"):
            raise RuntimeError("neither PyMuPDF nor pdftoppm is installed")
        total = poppler_page_count(pdf_path, total_hint)
        last_page = min(total, MAX_RENDER_PAGES)
        prefix = os.path.join(output_dir, "page")
        subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-r",
                str(RENDER_DPI),
                "-f",
                "1",
                "-l",
                str(last_page),
                pdf_path,
                prefix,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        paths = sorted(glob.glob(f"{prefix}-*.png"))
        return output_dir, len(paths), total


def report(**values):
    for key in (
        "STATUS",
        "OUTPUT",
        "PDF",
        "PAGES",
        "CHARS",
        "CHARS_PER_PAGE",
        "GARBLED_RATIO",
        "IMAGES",
        "NOTE",
    ):
        if key in values:
            print(f"{key}: {values[key]}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    arg = sys.argv[1]
    try:
        pdf_path = resolve_pdf(arg)
    except Exception as exc:
        report(STATUS="ERROR", NOTE=f"failed to query Zotero attachments: {exc}")
        return 2
    if not pdf_path:
        report(STATUS="ERROR", NOTE=f"no PDF attachment found for {arg!r}")
        return 2

    extraction_note = ""
    try:
        import pymupdf4llm

        chunks = pymupdf4llm.to_markdown(
            pdf_path, page_chunks=True, show_progress=False
        )
        pages = [chunk.get("text", "") for chunk in chunks]
    except Exception as primary_error:
        try:
            import fitz

            doc = fitz.open(pdf_path)
            try:
                pages = [page.get_text() for page in doc]
            finally:
                doc.close()
            extraction_note = (
                f" Plain PyMuPDF fallback used because pymupdf4llm failed: "
                f"{primary_error}."
            )
        except Exception as pymupdf_error:
            try:
                pages = extract_with_poppler(pdf_path)
                extraction_note = (
                    " Poppler plain-text fallback used; install pymupdf4llm for "
                    "better Markdown structure."
                )
            except Exception as poppler_error:
                report(
                    STATUS="ERROR",
                    PDF=pdf_path,
                    NOTE=(
                        "extraction failed in pymupdf4llm, PyMuPDF, and Poppler: "
                        f"{primary_error} / {pymupdf_error} / {poppler_error}"
                    ),
                )
                return 2

    page_count = max(1, len(pages))
    text = strip_noise(pages)
    chars_per_page = len(text) / page_count
    ratio = garbled_ratio(text)
    key = safe_key(arg)
    output_path = os.path.join(tempfile.gettempdir(), f"zotero_extract_{key}.md")
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)

    if chars_per_page < MIN_CHARS_PER_PAGE or ratio > MAX_GARBLED_RATIO:
        reason = (
            "too few chars/page (likely scanned or image-only PDF)"
            if chars_per_page < MIN_CHARS_PER_PAGE
            else "high garbled-character ratio (broken text layer)"
        )
        try:
            image_dir, rendered, total = render_images(pdf_path, key, page_count)
            coverage = f"rendered {rendered} of {total} pages"
            truncation = (
                "; fallback is partial, so do not summarize unrendered pages"
                if rendered < total
                else ""
            )
            report(
                STATUS="ESCALATE",
                OUTPUT=output_path,
                PDF=pdf_path,
                PAGES=page_count,
                CHARS=len(text),
                CHARS_PER_PAGE=f"{chars_per_page:.0f}",
                GARBLED_RATIO=f"{ratio:.3f}",
                IMAGES=f"{image_dir} ({coverage})",
                NOTE=f"{reason}; read IMAGES instead of OUTPUT{truncation}.",
            )
        except Exception as exc:
            report(
                STATUS="ESCALATE",
                OUTPUT=output_path,
                PDF=pdf_path,
                PAGES=page_count,
                CHARS=len(text),
                CHARS_PER_PAGE=f"{chars_per_page:.0f}",
                GARBLED_RATIO=f"{ratio:.3f}",
                NOTE=f"{reason}; image rendering failed: {exc}",
            )
        return 3

    report(
        STATUS="OK",
        OUTPUT=output_path,
        PDF=pdf_path,
        PAGES=page_count,
        CHARS=len(text),
        CHARS_PER_PAGE=f"{chars_per_page:.0f}",
        GARBLED_RATIO=f"{ratio:.3f}",
        NOTE=f"Read OUTPUT for the full text.{extraction_note}",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
