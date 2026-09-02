#!/usr/bin/env python3
"""Refresh in-vault citation links among reading notes using OpenAlex.

Scans 04.Reading/Notes/*.md, reads each note's DOI, queries the OpenAlex open
citation graph for its referenced works, and rewrites a marker-delimited
"References in this vault" section (outgoing edges only) in each citing note.
Only edges where BOTH papers exist in the vault are kept. Idempotent: re-running
strips and rebuilds the marked block, so it also handles renamed/removed notes.

Usage:
    python3 refresh_citations.py --confirm-whole-vault
    python3 refresh_citations.py --confirm-whole-vault --apply
    python3 refresh_citations.py --confirm-whole-vault --apply --force

The confirmation flag is mandatory because the script sends every vault DOI to
OpenAlex. Without `--apply`, it reports note changes without writing them. No
third-party dependencies are required, and OpenAlex needs no API key.
"""
import os, re, sys, json, time, glob, urllib.request, urllib.error

VAULT = os.path.abspath(os.path.expanduser(
    os.environ.get("READING_NOTES_VAULT", os.getcwd())
))
NOTES_DIR = os.path.join(VAULT, "04.Reading", "Notes")
CACHE_PATH = os.path.abspath(os.path.expanduser(os.environ.get(
    "READING_NOTES_CACHE",
    os.path.join(VAULT, ".cache", "reading-notes", "openalex_cache.json"),
)))
MAILTO = os.environ.get("OPENALEX_MAILTO", "").strip()

START = "<!-- citations-start: auto-generated from OpenAlex -->"
END = "<!-- citations-end -->"
# Capture the leading "---" separator too, so strip/rebuild is byte-identical.
BLOCK_RE = re.compile(r"\n*---\n+" + re.escape(START) + r".*?" + re.escape(END) + r"\n*", re.S)
DOI_RE = re.compile(r"(?m)^doi:\s*\"?([^\"\n]+)\"?")


def normalize_doi(raw):
    d = (raw or "").strip().strip('"\'').lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d if d.startswith("10.") else None


def fetch_openalex(doi):
    url = f"https://api.openalex.org/works/doi:{doi}?select=id,referenced_works"
    if MAILTO:
        url += f"&mailto={MAILTO}"
    for attempt in range(2):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                j = json.load(r)
            return {"oid": j.get("id"), "refs": list(j.get("referenced_works", []))}
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt == 0:
                time.sleep(1.0); continue
            print(f"  ! OpenAlex error for {doi}: {str(e)[:60]}")
            return None


def build_block(ref_names):
    links = "\n".join(f"- [[{n}]]" for n in ref_names)
    return f"\n\n---\n\n{START}\n## References in this vault\n\n{links}\n\n{END}\n"


def main():
    if "--confirm-whole-vault" not in sys.argv:
        print("Refusing to scan: pass --confirm-whole-vault after authorizing ")
        print("disclosure of the vault DOI set to OpenAlex.")
        return 2

    dry = "--apply" not in sys.argv
    force = "--force" in sys.argv

    cache = {}
    if os.path.exists(CACHE_PATH) and not force:
        try:
            cache = json.load(open(CACHE_PATH))
        except Exception:
            cache = {}

    # 1. scan notes
    notes = []  # (path, name, doi|None)
    for p in sorted(glob.glob(os.path.join(NOTES_DIR, "*.md"))):
        fm = re.match(r"---\n(.*?)\n---", open(p, encoding="utf-8").read(), re.S)
        doi = None
        if fm:
            m = DOI_RE.search(fm.group(1))
            if m:
                doi = normalize_doi(m.group(1))
        notes.append((p, os.path.basename(p)[:-3], doi))

    # 2. resolve DOIs via cache + OpenAlex
    dois = sorted({d for _, _, d in notes if d})
    fetched = 0
    for doi in dois:
        if doi in cache and not force:
            continue
        res = fetch_openalex(doi)
        if res:
            cache[doi] = res; fetched += 1
            time.sleep(0.25)
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    json.dump(cache, open(CACHE_PATH, "w"), indent=1)

    oid2name = {cache[d]["oid"]: name
                for p, name, d in notes if d and d in cache and cache[d].get("oid")}

    # 3. rewrite each note's marked block
    changed, edges = [], 0
    for p, name, doi in notes:
        self_oid = cache.get(doi, {}).get("oid") if doi else None
        refs = cache.get(doi, {}).get("refs", []) if doi else []
        ref_names = sorted({oid2name[r] for r in refs
                            if r in oid2name and r != self_oid})
        edges += len(ref_names)
        txt = open(p, encoding="utf-8").read()
        has_block = BLOCK_RE.search(txt)
        if ref_names:
            new = BLOCK_RE.sub("", txt).rstrip() + build_block(ref_names)
        elif has_block:                       # block became stale -> remove it
            new = BLOCK_RE.sub("", txt).rstrip() + "\n"
        else:                                 # no block, no refs -> leave untouched
            continue
        if new != txt:
            changed.append(name)
            if not dry:
                open(p, "w", encoding="utf-8").write(new)

    # 4. report
    tag = "[dry-run] would change" if dry else "updated"
    print(f"notes scanned: {len(notes)}  |  with DOI: {len(dois)}  |  "
          f"newly fetched: {fetched}  |  internal edges: {edges}")
    print(f"{tag}: {len(changed)} notes")
    for n in changed:
        print(f"  - {n}")


if __name__ == "__main__":
    sys.exit(main())
