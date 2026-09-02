#!/usr/bin/env python3
"""Deterministic checks and tracker helpers for Obsidian reading notes.

Usage:
    python3 note_tools.py tags
    python3 note_tools.py check-dup <doi>
    python3 note_tools.py check-tags <tag> [<tag> ...]
    python3 note_tools.py tick <doi>
    python3 note_tools.py skip <doi-or-zotero-key> [reason...]

`check-dup` and `check-tags` return 1 when they find a duplicate or collision.
All read-only commands work without a reading tracker. `tick` and `skip` are
safe no-ops when `04.Reading/Reading-tracker.md` is absent.
"""

import os
import re
import sys
from pathlib import Path


VAULT = Path(os.environ.get("READING_NOTES_VAULT", Path.cwd())).expanduser().resolve()
NOTES_DIR = VAULT / "04.Reading" / "Notes"
TRACKER_PATH = VAULT / "04.Reading" / "Reading-tracker.md"
DOI_RE = re.compile(r'(?m)^doi:\s*["\']?([^"\'\n]+)')
FRONTMATTER_RE = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)


def normalize_doi(raw):
    doi = (raw or "").strip().strip("\"'").lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi if doi.startswith("10.") else None


def frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    return match.group(1) if match else ""


def parse_tags(block):
    tags = []
    in_tags = False
    for line in block.splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags = True
            continue
        if not in_tags:
            continue
        match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if match:
            tags.append(match.group(1).strip().strip("\"'"))
        elif line.strip() == "" or line.startswith(" "):
            continue
        else:
            break
    return tags


def scan_notes():
    notes = []
    if not NOTES_DIR.is_dir():
        return notes
    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        block = frontmatter(text)
        match = DOI_RE.search(block)
        doi = normalize_doi(match.group(1)) if match else None
        notes.append((path.stem, doi, parse_tags(block)))
    return notes


def tag_counts():
    counts = {}
    for _, _, tags in scan_notes():
        for tag in tags:
            counts[tag] = counts.get(tag, 0) + 1
    return counts


def _singularize_token(token):
    """Normalize common tag plurals without corrupting -ics/-is vocabulary."""
    if len(token) <= 3 or token in {"news"}:
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith(("ss", "us", "is", "ics", "ous", "sis")):
        return token
    if token.endswith("s"):
        return token[:-1]
    return token


def norm_tag(tag):
    normalized = re.sub(r"[ _]+", "-", tag.lower().strip())
    return "-".join(_singularize_token(token) for token in normalized.split("-"))


def cmd_tags():
    counts = tag_counts()
    if not counts:
        print("(no tags found)")
        return 0
    print(f"# existing tag vocabulary ({len(counts)} unique)")
    for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{count:>4}  {tag}")
    return 0


def cmd_check_dup(raw_doi):
    target = normalize_doi(raw_doi)
    if not target:
        print(f"! not a valid DOI: {raw_doi!r}")
        return 2
    hits = [name for name, doi, _ in scan_notes() if doi == target]
    if hits:
        print(f"DUPLICATE: a note for DOI {target} already exists:")
        for name in hits:
            print(f"  - {name}")
        print("Do not create a second note without user direction.")
        return 1
    print(f"OK: no existing note for DOI {target}.")
    return 0


def cmd_check_tags(proposed):
    counts = tag_counts()
    exact = set(counts)
    normalized_index = {}
    for tag in exact:
        normalized_index.setdefault(norm_tag(tag), set()).add(tag)

    problems = 0
    for tag in proposed:
        if tag in exact:
            print(f"OK    {tag}  (existing, used {counts[tag]}x)")
            continue
        collisions = normalized_index.get(norm_tag(tag), set())
        if collisions:
            problems += 1
            print(f"FIX   {tag}  -> reuse existing variant: {', '.join(sorted(collisions))}")
        else:
            print(f"NEW   {tag}  (no existing match; use only if genuinely new)")
    if problems:
        print(f"\n{problems} tag(s) collide with the live vocabulary.")
    return 1 if problems else 0


def _identifier_in(line, identifier):
    normalized = normalize_doi(identifier)
    if normalized:
        return normalized in line.lower()
    return f"key:{identifier}".lower() in line.lower()


def _recount_tracker(lines):
    checkbox = re.compile(r"^- \[([ x-])\] ")
    heading = re.compile(r"^## (.+?)(?:\s{2,}\(.*\))?\s*$")
    progress = re.compile(r"^\*\*Progress:.*\*\*\s*$")
    current = None
    section_pending = {}
    section_total = {}

    for index, line in enumerate(lines):
        heading_match = heading.match(line)
        if heading_match:
            current = index
            section_pending.setdefault(current, 0)
            section_total.setdefault(current, 0)
            continue
        box_match = checkbox.match(line)
        if box_match and current is not None:
            section_total[current] += 1
            if box_match.group(1) == " ":
                section_pending[current] += 1

    done = sum(line.startswith("- [x] ") for line in lines)
    skipped = sum(line.startswith("- [-] ") for line in lines)
    total = sum(bool(checkbox.match(line)) for line in lines)
    pending = total - done - skipped
    skip_segment = f" · {skipped} skipped" if skipped else ""

    for index, line in enumerate(lines):
        if progress.match(line):
            lines[index] = (
                f"**Progress: {done} done{skip_segment} / {total} total"
                f"  ·  {pending} pending**\n"
            )
        heading_match = heading.match(line)
        if heading_match and index in section_total:
            name = heading_match.group(1).rstrip()
            lines[index] = (
                f"## {name}  ({section_pending[index]} pending / "
                f"{section_total[index]} total)\n"
            )
    return done, total, pending


def _flip_tracker(kind, identifier, reason=""):
    verb = "ticked" if kind == "x" else "skipped"
    if not TRACKER_PATH.exists():
        print(f"! tracker not found: {TRACKER_PATH} ({verb} nothing)")
        return 0

    lines = TRACKER_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    hit = False
    for index, line in enumerate(lines):
        if line.startswith("- [ ] ") and _identifier_in(line, identifier):
            body = line[6:].rstrip("\n")
            if kind == "-" and reason and "<!-- skip:" not in body:
                body = f"{body.rstrip()}  <!-- skip: {reason} -->"
            lines[index] = f"- [{kind}] {body}\n"
            hit = True
        elif line.startswith(("- [x] ", "- [-] ")) and _identifier_in(
            line, identifier
        ):
            print(f"already processed: {identifier}")
            return 0

    if not hit:
        print(f"no pending tracker row for {identifier}; nothing changed")
        return 0

    done, total, pending = _recount_tracker(lines)
    TRACKER_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"{verb} {identifier}. Progress: {done}/{total} done, {pending} pending.")
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    command, rest = args[0], args[1:]
    if command == "tags":
        return cmd_tags()
    if command == "check-dup" and rest:
        return cmd_check_dup(rest[0])
    if command == "check-tags" and rest:
        return cmd_check_tags(rest)
    if command == "tick" and rest:
        return _flip_tracker("x", rest[0])
    if command == "skip" and rest:
        reason = " ".join(rest[1:]).strip() or "unprocessable"
        return _flip_tracker("-", rest[0], reason)

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
