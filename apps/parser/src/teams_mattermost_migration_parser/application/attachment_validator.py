"""Validator for verifying that all attachments referenced in JSONL export exist on disk."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ..domain.exceptions import AttachmentMissingError

LOGGER = logging.getLogger(__name__)


def validate_import_attachments(
    jsonl_path: Path, raise_on_error: bool = True
) -> tuple[int, list[str]]:
    """Scan JSONL export files and verify every referenced post attachment exists and is non-empty.

    Args:
        jsonl_path: Path to the primary JSONL file.
        raise_on_error: If True, raises AttachmentMissingError if any attachment is missing or
            empty.

    Returns:
        A tuple of (total_attachments_checked, missing_attachment_relative_paths).
    """
    if not jsonl_path.exists():
        LOGGER.warning("Import JSONL file does not exist: %s", jsonl_path)
        return 0, []

    base_dir = jsonl_path.parent
    files_to_scan: list[Path] = [jsonl_path]

    # Include any chunked part files (e.g. import.part0001.jsonl)
    stem = jsonl_path.stem
    ext = jsonl_path.suffix
    for part_file in sorted(base_dir.glob(f"{stem}.part*{ext}")):
        if part_file not in files_to_scan:
            files_to_scan.append(part_file)

    total_attachments = 0
    missing: list[str] = []
    seen: set[str] = set()

    for file_path in files_to_scan:
        with file_path.open("r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    record = json.loads(line_str)
                except json.JSONDecodeError as err:
                    LOGGER.warning(
                        "Skipping malformed JSON line in %s:%d: %s", file_path.name, line_idx, err
                    )
                    continue

                if record.get("type") != "post":
                    continue

                post = record.get("post", {})
                attachments = post.get("attachments", [])
                if not isinstance(attachments, list):
                    continue

                for att in attachments:
                    if not isinstance(att, dict):
                        continue
                    rel_path_str = att.get("path")
                    if not rel_path_str or rel_path_str in seen:
                        continue

                    seen.add(rel_path_str)
                    total_attachments += 1

                    resolved = base_dir / rel_path_str
                    if (
                        not resolved.exists()
                        or not resolved.is_file()
                        or resolved.stat().st_size == 0
                    ):
                        missing.append(rel_path_str)

    if missing and raise_on_error:
        missing_fmt = "\n  - ".join(missing)
        raise AttachmentMissingError(
            f"Validation failed: {len(missing)} referenced attachment(s) are missing or 0 bytes:\n"
            f"  - {missing_fmt}"
        )

    LOGGER.info(
        "Attachment validation completed: %d referenced attachment(s) verified, %d missing.",
        total_attachments,
        len(missing),
    )
    return total_attachments, missing


def main() -> int:
    """CLI runner for attachment validation."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Validate that all attachments referenced in Mattermost JSONL export exist."
    )
    parser.add_argument(
        "jsonl_path",
        type=Path,
        help="Path to the JSONL export file.",
    )
    args = parser.parse_args()

    try:
        total, missing = validate_import_attachments(args.jsonl_path, raise_on_error=True)
        print(f"OK: Verified {total} attachment(s). 0 missing.")
        return 0
    except AttachmentMissingError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
