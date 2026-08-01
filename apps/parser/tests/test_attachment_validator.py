"""Tests for attachment validation functionality."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from teams_mattermost_migration_parser.application.attachment_validator import (
    main as attachment_validator_main,
)
from teams_mattermost_migration_parser.application.attachment_validator import (
    validate_import_attachments,
)
from teams_mattermost_migration_parser.domain.exceptions import AttachmentMissingError


def test_validate_import_attachments_success(tmp_path: Path) -> None:
    # Set up directory structure
    attachments_dir = tmp_path / "attachments"
    attachments_dir.mkdir()
    att_file = attachments_dir / "sample.pdf"
    att_file.write_bytes(b"sample file content")

    jsonl_file = tmp_path / "import.jsonl"
    post_record = {
        "type": "post",
        "post": {
            "team": "team-a",
            "channel": "town-square",
            "user": "user1",
            "message": "Hello world",
            "create_at": 1600000000000,
            "attachments": [{"path": "attachments/sample.pdf", "file_id": "sample.pdf"}],
        },
    }
    jsonl_file.write_text(json.dumps(post_record) + "\n", encoding="utf-8")

    total, missing = validate_import_attachments(jsonl_file, raise_on_error=True)
    assert total == 1
    assert missing == []


def test_validate_import_attachments_missing_file(tmp_path: Path) -> None:
    attachments_dir = tmp_path / "attachments"
    attachments_dir.mkdir()

    jsonl_file = tmp_path / "import.jsonl"
    post_record = {
        "type": "post",
        "post": {
            "team": "team-a",
            "channel": "town-square",
            "user": "user1",
            "message": "Hello world",
            "create_at": 1600000000000,
            "attachments": [{"path": "attachments/missing_doc.pdf", "file_id": "missing_doc.pdf"}],
        },
    }
    jsonl_file.write_text(json.dumps(post_record) + "\n", encoding="utf-8")

    with pytest.raises(AttachmentMissingError) as exc_info:
        validate_import_attachments(jsonl_file, raise_on_error=True)

    assert "missing_doc.pdf" in str(exc_info.value)

    # Test raise_on_error=False
    total, missing = validate_import_attachments(jsonl_file, raise_on_error=False)
    assert total == 1
    assert missing == ["attachments/missing_doc.pdf"]


def test_validate_import_attachments_empty_file(tmp_path: Path) -> None:
    attachments_dir = tmp_path / "attachments"
    attachments_dir.mkdir()
    empty_file = attachments_dir / "empty.txt"
    empty_file.write_bytes(b"")  # 0 bytes

    jsonl_file = tmp_path / "import.jsonl"
    post_record = {
        "type": "post",
        "post": {
            "team": "team-a",
            "channel": "town-square",
            "user": "user1",
            "message": "Check file",
            "create_at": 1600000000000,
            "attachments": [{"path": "attachments/empty.txt", "file_id": "empty.txt"}],
        },
    }
    jsonl_file.write_text(json.dumps(post_record) + "\n", encoding="utf-8")

    with pytest.raises(AttachmentMissingError) as exc_info:
        validate_import_attachments(jsonl_file, raise_on_error=True)

    assert "empty.txt" in str(exc_info.value)


def test_attachment_validator_cli_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    attachments_dir = tmp_path / "attachments"
    attachments_dir.mkdir()
    att_file = attachments_dir / "doc.pdf"
    att_file.write_bytes(b"content")

    jsonl_file = tmp_path / "import.jsonl"
    post_record = {
        "type": "post",
        "post": {
            "team": "t1",
            "channel": "c1",
            "user": "u1",
            "message": "msg",
            "attachments": [{"path": "attachments/doc.pdf"}],
        },
    }
    jsonl_file.write_text(json.dumps(post_record) + "\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["attachment_validator", str(jsonl_file)])
    ret = attachment_validator_main()
    assert ret == 0


def test_attachment_validator_cli_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    jsonl_file = tmp_path / "import.jsonl"
    post_record = {
        "type": "post",
        "post": {
            "team": "t1",
            "channel": "c1",
            "user": "u1",
            "message": "msg",
            "attachments": [{"path": "attachments/nonexistent.png"}],
        },
    }
    jsonl_file.write_text(json.dumps(post_record) + "\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["attachment_validator", str(jsonl_file)])
    ret = attachment_validator_main()
    assert ret == 1
