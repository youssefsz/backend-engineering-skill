"""Mutation tests for protections the repository validator/package builder claims."""

import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from package import build_archive, verify_archive
from validate import ROOT, check_links, frontmatter, validate_core, validate_repo


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.skill = self.root / "backend-engineering"
        shutil.copytree(ROOT / "skills/backend-engineering", self.skill)

    def change(self, relative, old, new):
        path = self.skill / relative
        content = path.read_text()
        self.assertIn(old, content)
        path.write_text(content.replace(old, new))

    def assert_invalid(self, phrase):
        errors = validate_core(self.skill)
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_canonical_core(self):
        self.assertEqual(validate_core(self.skill), [])

    def test_missing_resource(self):
        (self.skill / "references/api-and-security.md").unlink()
        self.assert_invalid("missing core file")

    def test_case_sensitive_links_on_any_filesystem(self):
        self.change("SKILL.md", "references/database-design.md", "references/Database-design.md")
        self.assert_invalid("case-mismatched")

    def test_broken_anchor(self):
        self.change("references/database-design.md", "sources.md#s54", "sources.md#absent")
        self.assert_invalid("missing local anchor")

    def test_external_local_dependency(self):
        outside = self.root / "outside.md"
        outside.write_text("# Outside\n")
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text() + "\n[dependency](../outside.md)\n")
        self.assert_invalid("escapes package boundary")

    def test_symlink_resource(self):
        path = self.skill / "references/api-and-security.md"
        path.unlink()
        path.symlink_to(ROOT / "skills/backend-engineering/references/api-and-security.md")
        self.assert_invalid("symlinks")

    def test_unexpected_secret_file(self):
        (self.skill / ".env").write_text("SYNTHETIC=not-a-real-secret\n")
        self.assert_invalid("unexpected installable file")

    def test_disabled_invocation_metadata(self):
        self.change("SKILL.md", "name: backend-engineering", "name: backend-engineering\ndisable-model-invocation: true")
        self.assert_invalid("frontmatter")

    def test_duplicate_yaml_keys(self):
        with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
            frontmatter("---\nname: a\nname: b\n---\n# Example")

    def test_wrong_directory_name(self):
        renamed = self.root / "wrong-name"
        self.skill.rename(renamed)
        self.assertIn("skill directory must be named backend-engineering", validate_core(renamed))

    def test_unknown_source(self):
        self.change("references/database-design.md", "[S54]", "[S99]")
        self.assert_invalid("unknown source")

    def test_placeholder(self):
        path = self.skill / "assets/implementation-checklist.md"
        path.write_text(path.read_text() + "\nTODO\n")
        self.assert_invalid("unfinished placeholder")

    def test_reference_style_links_are_checked(self):
        path = self.skill / "assets/implementation-checklist.md"
        path.write_text("# Checklist\n\n[missing][resource]\n\n[resource]: nowhere.md\n")
        self.assert_invalid("case-mismatched")

    def test_duplicate_heading_anchor_resolution(self):
        path = self.skill / "assets/implementation-checklist.md"
        path.write_text("# Repeated\n\n## Repeated\n\n[second](#repeated-1)\n")
        self.assertEqual(check_links([path], self.skill, self.skill), [])

    def test_archive_extraction_and_reproducible_bytes(self):
        first, second = self.root / "a.zip", self.root / "b.zip"
        build_archive(first, self.skill)
        build_archive(second, self.skill)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(verify_archive(first, self.skill), 15)

    def test_archive_rejects_extra_and_traversal_entries(self):
        target = self.root / "archive.zip"
        build_archive(target, self.skill)
        with zipfile.ZipFile(target, "a") as bundle:
            bundle.writestr("../outside.txt", "untrusted")
        with self.assertRaisesRegex(ValueError, "unexpected paths"):
            verify_archive(target, self.skill)

    def test_archive_rejects_modified_content(self):
        target = self.root / "archive.zip"
        build_archive(target, self.skill)
        (self.skill / "assets/implementation-checklist.md").write_text("# Changed\n")
        with self.assertRaisesRegex(ValueError, "differs from canonical"):
            verify_archive(target, self.skill)

    def test_license_mismatch_is_rejected(self):
        (self.skill / "LICENSE").write_text("different license")
        with self.assertRaisesRegex(ValueError, "licenses differ"):
            build_archive(self.root / "invalid.zip", self.skill)

    def test_repository_missing_deliverable(self):
        empty = self.root / "empty"
        empty.mkdir()
        self.assertTrue(any("missing repository file" in e for e in validate_repo(empty)))


if __name__ == "__main__":
    unittest.main()
