"""Build/check an installable archive from the canonical skill, without publishing."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from datetime import date
from pathlib import Path

from validate import CORE_FILES, ROOT, validate_core

SKILL = ROOT / "skills/backend-engineering"


def release_metadata(root=ROOT, tag=None):
    """Read the current version and, for a release, require dated highlights."""
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## \[(\d+\.\d+\.\d+)\] - (.+)$", changelog, re.M)
    if not match:
        raise ValueError("no current version entry in CHANGELOG.md")
    version = match[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    if project["project"]["version"] != version:
        raise ValueError("pyproject.toml version must match the first CHANGELOG.md version")
    if tag is None:
        return version, None
    if not re.fullmatch(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", tag):
        raise ValueError("release tag must use stable vMAJOR.MINOR.PATCH format")
    if tag != f"v{version}":
        raise ValueError("release tag must match pyproject.toml and CHANGELOG.md versions")
    try:
        release_date = date.fromisoformat(match[2])
    except ValueError as exc:
        raise ValueError("release changelog entry must have a YYYY-MM-DD date instead of Unreleased") from exc
    if release_date.isoformat() != match[2]:
        raise ValueError("release changelog date must use YYYY-MM-DD format")
    highlights = re.split(r"^## ", changelog[match.end():], maxsplit=1, flags=re.M)[0].strip()
    if not highlights:
        raise ValueError("release changelog entry must contain highlights")
    notes = (
        f"## Highlights\n\n{highlights}\n\n"
        f"## Download\n\n"
        f"Download `backend-engineering-{tag}.zip` and extract the complete "
        "`backend-engineering/` directory. The ZIP contains the skill, references, "
        "assets, and license. No Python or uv is required to use it.\n\n"
        "The matching `.zip.sha256` file contains its SHA-256 checksum.\n\n"
    )
    return version, notes


def write_release_files(archive, notes=None):
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(archive.suffix + ".sha256").write_text(
        f"{digest}  {archive.name}\n", encoding="utf-8"
    )
    if notes is not None:
        (archive.parent / "release-notes.md").write_text(notes, encoding="utf-8")
    return digest


def verify_archive(archive, skill=SKILL):
    expected = {f"backend-engineering/{name}" for name in CORE_FILES}
    with zipfile.ZipFile(archive) as bundle:
        infos = bundle.infolist()
        if len(infos) != len(expected) or {i.filename for i in infos} != expected:
            raise ValueError("archive contains missing, duplicate, or unexpected paths")
        with tempfile.TemporaryDirectory(prefix="backend-skill-check-") as directory:
            extracted = Path(directory)
            for info in infos:
                relative = info.filename.removeprefix("backend-engineering/")
                original = (skill / relative).read_bytes()
                if info.file_size != len(original) or bundle.read(info) != original:
                    raise ValueError(f"archive content differs from canonical skill: {relative}")
                if info.external_attr >> 16 & 0o170000 == 0o120000:
                    raise ValueError("archive contains a symlink")
                target = extracted / info.filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(original)
            installed = extracted / "backend-engineering"
            errors = validate_core(installed)
            if errors:
                raise ValueError("extracted validation failed: " + "; ".join(errors))
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/validate.py"), "--skill", str(installed)
            ], capture_output=True, text=True)
            if result.returncode:
                raise ValueError(result.stdout + result.stderr)
    return len(expected)


def build_archive(output, skill=SKILL):
    errors = validate_core(skill)
    if errors:
        raise ValueError("cannot package invalid skill: " + "; ".join(errors))
    if (ROOT / "LICENSE").read_bytes() != (skill / "LICENSE").read_bytes():
        raise ValueError("root and installable licenses differ")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".backend-skill-", suffix=".zip", dir=output.parent)
    os.close(descriptor)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for name in sorted(CORE_FILES):
                info = zipfile.ZipInfo(f"backend-engineering/{name}", date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, (skill / name).read_bytes())
        verify_archive(Path(temporary), skill)
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", type=Path, help="check an existing archive against current canonical contents")
    mode.add_argument("--tag", help="require matching stable tag/version, dated highlights, and prepare release notes")
    args = parser.parse_args()
    try:
        version, notes = release_metadata(tag=args.tag)
        target = args.check or ROOT / f"dist/backend-engineering-v{version}.zip"
        if args.check:
            count = verify_archive(target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
        else:
            build_archive(target)
            count = len(CORE_FILES)
            digest = write_release_files(target, notes)
        print(f"PASS: archive extracted, {count} files match canonical source, package validation passed")
        print(f"{digest}  {target}")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
