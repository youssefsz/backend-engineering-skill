"""Release metadata, checksum, and publication-boundary checks, without GitHub writes."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from package import release_metadata, write_release_files
from validate import ROOT, UniqueLoader, check_workflows


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "pyproject.toml").write_text('[project]\nversion = "0.2.0"\n')
        self.changelog = self.root / "CHANGELOG.md"
        self.changelog.write_text(
            "# Changelog\n\n## [0.2.0] - 2026-10-16\n\n- Improve retries.\n\n"
            "## [0.1.0] - 2026-09-01\n\n- Old highlights.\n"
        )

    def test_release_uses_only_matching_version_highlights(self):
        version, notes = release_metadata(self.root, "v0.2.0")
        self.assertEqual(version, "0.2.0")
        self.assertIn("Improve retries.", notes)
        self.assertNotIn("Old highlights.", notes)
        self.assertIn("backend-engineering-v0.2.0.zip", notes)

    def test_tag_must_match_version(self):
        with self.assertRaisesRegex(ValueError, "tag must match"):
            release_metadata(self.root, "v0.3.0")

    def test_project_and_changelog_versions_must_match(self):
        (self.root / "pyproject.toml").write_text('[project]\nversion = "0.3.0"\n')
        with self.assertRaisesRegex(ValueError, "first CHANGELOG"):
            release_metadata(self.root, "v0.2.0")

    def test_unreleased_build_allowed_but_publication_rejected(self):
        self.changelog.write_text("# Changelog\n\n## [0.2.0] - Unreleased\n\n- Pending.\n")
        self.assertEqual(release_metadata(self.root), ("0.2.0", None))
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            release_metadata(self.root, "v0.2.0")

    def test_invalid_release_tags(self):
        for tag in ("0.2.0", "v00.2.0", "v0.2.0-rc.1", "v0.2.0+build", "v0.2.0; echo injected"):
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, "stable"):
                release_metadata(self.root, tag)

    def test_invalid_date_and_missing_highlights(self):
        for entry in ("## [0.2.0] - 2026-02-30\n\n- Invalid date.\n", "## [0.2.0] - 2026-10-16\n\n"):
            self.changelog.write_text("# Changelog\n\n" + entry)
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                release_metadata(self.root, "v0.2.0")

    def test_checksum_and_release_notes_match_built_file(self):
        archive = self.root / "backend-engineering-v0.2.0.zip"
        archive.write_bytes(b"controlled artifact bytes")
        _, notes = release_metadata(self.root, "v0.2.0")
        digest = write_release_files(archive, notes)
        checksum = archive.with_suffix(".zip.sha256").read_text()
        self.assertEqual(checksum, f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
        self.assertEqual(digest, checksum.split()[0])
        self.assertEqual((self.root / "release-notes.md").read_text(), notes)

    def workflow_fixture(self):
        directory = self.root / ".github/workflows"
        directory.mkdir(parents=True)
        source = ROOT / ".github/workflows/release.yml"
        content = yaml.load(source.read_text(), Loader=UniqueLoader)
        target = directory / "release.yml"
        target.write_text(yaml.safe_dump(content))
        return content, target

    def test_release_workflow_tag_boundary_and_action_pins(self):
        self.workflow_fixture()
        self.assertEqual(check_workflows(self.root), [])

    def test_release_workflow_rejects_pull_request_publication(self):
        content, target = self.workflow_fixture()
        content["on"] = {"pull_request": None}
        target.write_text(yaml.safe_dump(content))
        self.assertTrue(any("only by pushed version tags" in e for e in check_workflows(self.root)))

    def test_release_workflow_rejects_broad_write_permissions(self):
        content, target = self.workflow_fixture()
        content["permissions"] = {"contents": "write"}
        target.write_text(yaml.safe_dump(content))
        self.assertTrue(any("default" in e for e in check_workflows(self.root)))

    def test_publish_command_passes_only_zip_and_checksum_to_cli(self):
        workflow = yaml.load((ROOT / ".github/workflows/release.yml").read_text(), Loader=UniqueLoader)
        publish = workflow["jobs"]["release"]["steps"][-1]["run"]
        dist = self.root / "dist"
        dist.mkdir()
        archive = dist / "backend-engineering-v0.2.0.zip"
        archive.write_bytes(b"controlled artifact bytes")
        _, notes = release_metadata(self.root, "v0.2.0")
        write_release_files(archive, notes)
        stub = self.root / "gh"
        stub.write_text(
            f"#!{sys.executable}\nimport json, sys\nfrom pathlib import Path\n"
            "Path('arguments.json').write_text(json.dumps(sys.argv[1:]))\n"
        )
        stub.chmod(0o755)
        env = dict(os.environ, RELEASE_TAG="v0.2.0", PATH=str(self.root) + os.pathsep + os.environ["PATH"])
        subprocess.run(["bash", "-euo", "pipefail", "-c", publish], cwd=self.root, env=env, check=True, timeout=10)
        arguments = json.loads((self.root / "arguments.json").read_text())
        self.assertEqual(arguments[:5], ["release", "create", "v0.2.0", str(archive.relative_to(self.root)), str(archive.relative_to(self.root)) + ".sha256"])
        for flag in ("--verify-tag", "--generate-notes"):
            self.assertIn(flag, arguments)
        notes_path = self.root / arguments[arguments.index("--notes-file") + 1]
        self.assertEqual(notes_path.read_text(), notes)


if __name__ == "__main__":
    unittest.main()
