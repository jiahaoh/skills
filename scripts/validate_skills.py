#!/usr/bin/env python3
"""Validate repository skill structure without third-party dependencies."""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^]]*]\(([^)]+)\)")
VENDORED_SKILL_SHA256 = {
    "unslop": "2789ab80477b7e382292e4d7acca1057784df19713fffb74622ff0f83b2f3733",
}


def frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: SKILL.md must start with YAML frontmatter")
    try:
        block, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc

    values: dict[str, str] = {}
    for key in ("name", "description", "license", "disable-model-invocation"):
        match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", block)
        if match:
            values[key] = match.group(1).strip().strip("\"'")
    return values


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for raw_target in LINK_RE.findall(text):
        target = raw_target.split("#", 1)[0]
        if (
            not target
            or target == "link"
            or "://" in target
            or target.startswith(("#", "mailto:", "<"))
        ):
            continue
        if not (path.parent / target).resolve().exists():
            errors.append(f"{path}: broken relative link {raw_target!r}")


def validate_skill(skill_dir: Path, readme: str, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"

    if not skill_md.is_file():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return
    if not metadata_path.is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
        return

    text = skill_md.read_text(encoding="utf-8")
    metadata = metadata_path.read_text(encoding="utf-8")
    try:
        fields = frontmatter(text, skill_md)
    except ValueError as exc:
        errors.append(str(exc))
        return

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME_RE.fullmatch(name):
        errors.append(f"{skill_md}: invalid or missing name {name!r}")
    if name != skill_dir.name:
        errors.append(f"{skill_md}: name {name!r} must match directory")
    if not description:
        errors.append(f"{skill_md}: missing description")
    if len(name) > 64:
        errors.append(f"{skill_md}: name exceeds 64 characters")
    expected_sha256 = VENDORED_SKILL_SHA256.get(name)
    if expected_sha256:
        actual_sha256 = hashlib.sha256(skill_md.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            errors.append(
                f"{skill_md}: vendored source hash is {actual_sha256}, "
                f"expected {expected_sha256}"
            )
    if "TODO" in text or "TODO" in metadata:
        errors.append(f"{skill_dir}: unfinished TODO marker")
    if "/Users/" in text or "/Users/" in metadata:
        errors.append(f"{skill_dir}: machine-specific absolute path")
    if "LICENSE.txt" in fields.get("license", "") and not (
        skill_dir / "LICENSE.txt"
    ).is_file():
        errors.append(f"{skill_dir}: frontmatter references missing LICENSE.txt")

    for key in ("display_name", "short_description"):
        if not re.search(rf"(?m)^\s{{2}}{key}:\s*['\"].+['\"]\s*$", metadata):
            errors.append(f"{metadata_path}: missing quoted interface.{key}")

    short_match = re.search(
        r"(?m)^\s{2}short_description:\s*['\"](.+)['\"]\s*$", metadata
    )
    if short_match and not 25 <= len(short_match.group(1)) <= 64:
        errors.append(
            f"{metadata_path}: short_description must be 25-64 characters"
        )

    prompt_match = re.search(
        r"(?m)^\s{2}default_prompt:\s*['\"](.+)['\"]\s*$", metadata
    )
    if prompt_match and f"${name}" not in prompt_match.group(1):
        errors.append(f"{metadata_path}: default_prompt must mention ${name}")

    source_explicit = fields.get("disable-model-invocation", "").lower() == "true"
    codex_explicit = bool(
        re.search(
            r"(?m)^\s{2}allow_implicit_invocation:\s*false\s*$", metadata
        )
    )
    if source_explicit and not codex_explicit:
        errors.append(
            f"{skill_dir}: disable-model-invocation: true must be mirrored by "
            "agents/openai.yaml policy.allow_implicit_invocation: false"
        )

    if f"skills/{name}/SKILL.md" not in readme:
        errors.append(f"README.md: missing catalog link for {name}")

    validate_links(skill_md, text, errors)

    for path in skill_dir.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}: Python syntax error: {exc}")

    for path in skill_dir.rglob("*.sh"):
        result = subprocess.run(
            ["bash", "-n", str(path)], capture_output=True, text=True, check=False
        )
        if result.returncode:
            errors.append(f"{path}: shell syntax error: {result.stderr.strip()}")


def main() -> int:
    errors: list[str] = []
    if not SKILLS.is_dir():
        print("ERROR: skills/ directory is missing")
        return 1

    readme = README.read_text(encoding="utf-8") if README.is_file() else ""
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("skills/: no skills found")

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, readme, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"\n{len(errors)} validation error(s)")
        return 1

    print(f"Validated {len(skill_dirs)} skill(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
