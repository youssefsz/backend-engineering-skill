"""Validate repository/package invariants; never execute backend/application code."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = (
    "architecture-and-design", "database-design", "queries-and-indexes",
    "transactions-and-concurrency", "migrations-and-recovery", "api-and-security",
    "reliability-and-background-jobs", "performance-and-observability",
    "code-and-testing", "research-policy", "sources",
)
CORE_FILES = frozenset(
    ["SKILL.md", "LICENSE"]
    + [f"references/{name}.md" for name in REFERENCES]
    + ["assets/implementation-checklist.md", "assets/verification-report-template.md"]
)
REPO_FILES = (
    "README.md", "AGENTS.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md",
    ".gitignore", ".github/workflows/validate.yml", "pyproject.toml", "uv.lock",
    ".pymarkdown.json", "integrations/codex.md", "integrations/claude-code.md",
    "integrations/generic-agent.md", "evals/README.md", "evals/activation-cases.md",
    "evals/engineering-cases.md", "evals/results-template.md", "scripts/validate.py",
    "scripts/package.py", "scripts/check_external_links.py", "tests/test_validation.py",
    ".github/workflows/release.yml", ".github/release.yml",
    ".github/pull_request_template.md", "tests/test_release.py",
)
MARKDOWN = MarkdownIt("commonmark").enable("table")
IGNORED = {".git", ".venv", "node_modules", "dist", "__pycache__"}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently keeping the last value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unclosed YAML frontmatter") from exc
    data = yaml.load("\n".join(lines[1:end]), Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, "\n".join(lines[end + 1:])


def markdown_body(path):
    text = path.read_text(encoding="utf-8")
    return frontmatter(text)[1] if path.name == "SKILL.md" else text


def markdown_paths(root):
    return sorted(
        p for p in root.rglob("*.md")
        if not IGNORED.intersection(p.relative_to(root).parts)
        and p.relative_to(root).parts[:2] != ("evals", "runs")
    )


def heading_anchors(text):
    """GitHub-style slugs for the Markdown headings used by this package."""
    tokens = MARKDOWN.parse(text)
    anchors, used = set(), set()
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        children = tokens[i + 1].children or []
        label = "".join(c.content for c in children if c.type in {"text", "code_inline"})
        slug = re.sub(r"[^\w\- ]", "", label.lower()).replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
        anchors.add(candidate)
    return anchors


def markdown_links(text):
    for token in MARKDOWN.parse(text):
        for child in token.children or []:
            if child.type == "link_open":
                yield child.attrGet("href")
            elif child.type == "image":
                yield child.attrGet("src")


def exact_case_exists(path, root):
    """Check each component explicitly, even on a case-insensitive filesystem."""
    current = root
    for part in path.relative_to(root).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current = current / part
    return current.exists()


def check_links(paths, root, skill_root):
    errors = []
    for path in paths:
        for href in markdown_links(markdown_body(path)):
            parsed = urlsplit(href)
            if parsed.scheme in {"https", "http", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc or parsed.path.startswith(("/", "~")):
                errors.append(f"{path.name}: nonportable local link {href}")
                continue
            target = (path.parent / unquote(parsed.path)).absolute() if parsed.path else path.absolute()
            # Resolve lexical '..' without losing the original component casing.
            target = Path(os.path.normpath(target))
            boundary = skill_root if path.is_relative_to(skill_root) else root
            if not target.is_relative_to(boundary):
                errors.append(f"{path.name}: link escapes package boundary: {href}")
                continue
            if not exact_case_exists(target, boundary):
                errors.append(f"{path.name}: missing or case-mismatched link: {href}")
                continue
            if not target.resolve().is_relative_to(boundary.resolve()):
                errors.append(f"{path.name}: symlink escapes package: {href}")
            if parsed.fragment:
                if target.suffix != ".md" or unquote(parsed.fragment) not in heading_anchors(markdown_body(target)):
                    errors.append(f"{path.name}: missing local anchor: {href}")
    return errors


def validate_core(skill):
    errors = []
    if skill.name != "backend-engineering":
        errors.append("skill directory must be named backend-engineering")
    files = {p.relative_to(skill).as_posix() for p in skill.rglob("*") if p.is_file()}
    for missing in sorted(CORE_FILES - files):
        errors.append(f"missing core file: {missing}")
    for extra in sorted(files - CORE_FILES):
        errors.append(f"unexpected installable file: {extra}")
    if any(p.is_symlink() for p in skill.rglob("*")):
        errors.append("installable package must not contain symlinks")
    if errors:
        return errors
    text = (skill / "SKILL.md").read_text()
    try:
        data, body = frontmatter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"SKILL.md: {exc}"]
    if set(data) != {"name", "description"}:
        errors.append("portable core permits only name and description frontmatter")
    if data.get("name") != skill.name:
        errors.append("frontmatter name does not match directory")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append("description must be a nonempty string of at most 1024 characters")
    if not 150 <= len(text.splitlines()) <= 250:
        errors.append("SKILL.md must meet the project's 150–250-line target")
    linked = {urlsplit(link).path for link in markdown_links(body)}
    for name in REFERENCES:
        if f"references/{name}.md" not in linked:
            errors.append(f"main skill must directly link reference: {name}")
    paths = markdown_paths(skill)
    try:
        errors.extend(check_links(paths, skill, skill))
    except (ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    registry = (skill / "references/sources.md").read_text()
    ids = re.findall(r"^## (S\d{2})$", registry, re.M)
    if len(ids) != len(set(ids)) or set(ids) != {f"S{i:02}" for i in range(1, 56)}:
        errors.append("source registry must contain distinct S01–S55 entries")
    for path in paths:
        content = path.read_text()
        for identifier in set(re.findall(r"\bS\d{2}\b", content)) - set(ids):
            errors.append(f"{path.name}: unknown source identifier {identifier}")
        if re.search(r"/Users/|/home/|file://|disable-model-invocation|allow_implicit_invocation", content):
            errors.append(f"{path.name}: machine path or invocation setting in portable core")
        if re.search(r"\b(?:TODO|FIXME|TBD)\b|\[INSERT\b|lorem ipsum", content, re.I):
            errors.append(f"{path.name}: unfinished placeholder")
    return errors


def check_workflows(root):
    errors = []
    for path in sorted((root / ".github/workflows").glob("*.yml")):
        workflow = yaml.load(path.read_text(), Loader=UniqueLoader)
        if workflow.get("permissions") != {"contents": "read"}:
            errors.append(f"{path.name}: workflow default must have contents: read only")
        release = path.name == "release.yml"
        if release:
            trigger = workflow.get("on", {})
            push = trigger.get("push", {}) if isinstance(trigger, dict) else {}
            if set(trigger) != {"push"} or set(push) != {"tags"} or not push.get("tags"):
                errors.append("release.yml: publication must be triggered only by pushed version tags")
            if "release" not in workflow.get("jobs", {}):
                errors.append("release.yml: missing release job")
        for name, job in workflow.get("jobs", {}).items():
            expected = {"contents": "write" if release and name == "release" else "read"}
            if job.get("permissions", workflow.get("permissions")) != expected:
                errors.append(f"{path.name}/{name}: only the tag-release job may have contents: write")
            for step in job.get("steps", []):
                if "uses" in step and not re.fullmatch(r"[^@]+@[0-9a-f]{40}", step["uses"]):
                    errors.append(f"{path.name}: CI actions must use immutable 40-character commits")
    return errors


def validate_repo(root):
    errors = [f"missing repository file: {name}" for name in REPO_FILES if not (root / name).is_file()]
    skill = root / "skills/backend-engineering"
    errors.extend(validate_core(skill))
    if errors:
        return errors
    if (root / "LICENSE").read_bytes() != (skill / "LICENSE").read_bytes():
        errors.append("repository and installable licenses differ")
    paths = markdown_paths(root)
    errors.extend(check_links(paths, root, skill))
    ids = {f"S{i:02}" for i in range(1, 56)}
    cited = set()
    for path in paths:
        text = path.read_text()
        if path.name != "sources.md":
            cited.update(re.findall(r"sources\.md#(s\d{2})", text))
        for unknown in set(re.findall(r"\bS\d{2}\b", text)) - ids:
            errors.append(f"{path.name}: unknown source identifier {unknown}")
        if re.search(r"\b(?:TODO|FIXME|TBD)\b|\[INSERT\b|lorem ipsum", text, re.I):
            errors.append(f"{path.name}: unfinished placeholder")
    for unused in sorted(ids - {s.upper() for s in cited}):
        errors.append(f"source not linked from guidance/documentation: {unused}")
    errors.extend(check_workflows(root))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", type=Path, help="validate an extracted installable directory only")
    parser.add_argument("--skip-lint", action="store_true", help="run structural checks only")
    args = parser.parse_args()
    scope = args.skill.resolve() if args.skill else ROOT
    errors = validate_core(scope) if args.skill else validate_repo(scope)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    skill = scope if args.skill else scope / "skills/backend-engineering"
    from skills_ref import validate as reference_validate
    problems = reference_validate(skill)
    if problems:
        print("ERROR: skills-ref: " + "; ".join(problems), file=sys.stderr)
        return 1
    if not args.skip_lint:
        command = [sys.executable, "-m", "pymarkdown", "--config", str(ROOT / ".pymarkdown.json"), "scan"]
        command.extend(str(p) for p in markdown_paths(scope))
        if subprocess.run(command).returncode:
            return 1
    print(f"PASS: {'installable package' if args.skill else 'repository'} structure, sources, links, anchors, and frontmatter")
    if not args.skip_lint:
        print("PASS: Markdown lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
