"""Unit tests for the bulk import packager module."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from teams_mattermost_migration_parser.application.packager import create_import_package


def test_create_import_package_with_attachments(tmp_path: Path) -> None:
    jsonl_file = tmp_path / "import.jsonl"
    jsonl_file.write_text(
        json.dumps({"type": "version", "version": 1})
        + "\n"
        + json.dumps(
            {
                "type": "post",
                "post": {
                    "team": "team-a",
                    "channel": "chan-1",
                    "user": "user-1",
                    "message": "Hello world",
                    "create_at": 1000,
                    "attachments": [{"path": "attachments/file1.pdf"}],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    attachments_dir = tmp_path / "attachments"
    attachments_dir.mkdir()
    att_file1 = attachments_dir / "file1.pdf"
    att_file1.write_bytes(b"%PDF-1.4 test content")

    sub_dir = attachments_dir / "sub"
    sub_dir.mkdir()
    att_file2 = sub_dir / "file2.png"
    att_file2.write_bytes(b"\x89PNG test content")

    zip_path = create_import_package(jsonl_file)

    assert zip_path.exists()
    assert zip_path.name == "import.zip"

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "import.jsonl" in namelist
        assert "attachments/" in namelist
        assert "attachments/file1.pdf" in namelist
        assert "attachments/sub/file2.png" in namelist

        content_jsonl = zf.read("import.jsonl").decode("utf-8")
        assert "version" in content_jsonl
        assert "file1.pdf" in content_jsonl

        assert zf.read("attachments/file1.pdf") == b"%PDF-1.4 test content"
        assert zf.read("attachments/sub/file2.png") == b"\x89PNG test content"


def test_create_import_package_empty_attachments(tmp_path: Path) -> None:
    jsonl_file = tmp_path / "custom-import.jsonl"
    jsonl_file.write_text(
        json.dumps({"type": "version", "version": 1}) + "\n",
        encoding="utf-8",
    )

    zip_path = create_import_package(jsonl_file)

    assert zip_path.exists()
    assert zip_path.name == "custom-import.zip"

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "custom-import.jsonl" in namelist
        assert "attachments/" in namelist


def test_create_import_package_with_parts(tmp_path: Path) -> None:
    jsonl_file = tmp_path / "export.jsonl"
    jsonl_file.write_text(json.dumps({"type": "version", "version": 1}) + "\n", encoding="utf-8")

    part1 = tmp_path / "export.part001.jsonl"
    part1.write_text(json.dumps({"type": "team", "team": {"name": "t1"}}) + "\n", encoding="utf-8")

    part2 = tmp_path / "export.part002.jsonl"
    part2.write_text(
        json.dumps({"type": "user", "user": {"username": "u1"}}) + "\n", encoding="utf-8"
    )

    zip_path = create_import_package(jsonl_file)

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "export.jsonl" in namelist
        assert "export.part001.jsonl" in namelist
        assert "export.part002.jsonl" in namelist
        assert "attachments/" in namelist


def test_create_import_package_missing_jsonl_handled(caplog: pytest.LogCaptureFixture) -> None:
    nonexistent = Path("/nonexistent/file.jsonl")
    res = create_import_package(nonexistent)
    assert res == Path("/nonexistent/file.zip")
    assert "skipping ZIP package creation" in caplog.text
