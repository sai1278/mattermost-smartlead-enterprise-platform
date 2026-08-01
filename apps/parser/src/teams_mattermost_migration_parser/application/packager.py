"""Packager for creating Mattermost bulk import ZIP packages containing JSONL and attachments."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def create_import_package(
    jsonl_path: Path,
    output_package_path: Path | None = None,
    compression: int = zipfile.ZIP_STORED,
) -> Path:
    """Package JSONL import file and attachments into a Mattermost bulk import ZIP archive.

    The generated archive preserves the directory structure expected by Mattermost:
      - import.jsonl (or original jsonl file name) at archive root
      - attachments/ directory at archive root containing all attachment files

    Args:
        jsonl_path: Path to the primary JSONL file.
        output_package_path: Optional explicit path for the output ZIP archive. If None,
            defaults to replacing suffix of jsonl_path with '.zip'.
        compression: Compression mode (default zipfile.ZIP_STORED).

    Returns:
        Path to the created ZIP import package.
    """
    base_dir = jsonl_path.parent
    if output_package_path is None:
        if jsonl_path.suffix.lower() == ".zip":
            output_package_path = jsonl_path
        else:
            output_package_path = jsonl_path.with_suffix(".zip")

    if not jsonl_path.exists():
        LOGGER.warning(
            "JSONL import file does not exist at %s; skipping ZIP package creation.", jsonl_path
        )
        return output_package_path

    # Find JSONL files to include (primary + chunked parts)
    files_to_pack: list[tuple[Path, str]] = []

    # Primary JSONL
    files_to_pack.append((jsonl_path, jsonl_path.name))

    # Chunked part files (e.g. import.part001.jsonl)
    stem = jsonl_path.stem
    ext = jsonl_path.suffix
    for part_file in sorted(base_dir.glob(f"{stem}.part*{ext}")):
        if part_file != jsonl_path and part_file.is_file():
            files_to_pack.append((part_file, part_file.name))

    attachments_dir = base_dir / "attachments"

    output_package_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary zip file first to ensure atomic output creation
    tmp_zip_path = output_package_path.parent / f"{output_package_path.name}.tmp"

    LOGGER.info("Creating Mattermost bulk import package: %s", output_package_path)

    with zipfile.ZipFile(tmp_zip_path, "w", compression=compression) as zip_file:
        # Add JSONL files
        for src_path, arc_name in files_to_pack:
            zip_file.write(src_path, arcname=arc_name)

        # Always ensure attachments/ directory exists in the ZIP package structure
        zip_info = zipfile.ZipInfo("attachments/")
        zip_file.writestr(zip_info, "")

        # Include all files in attachments directory
        if attachments_dir.exists() and attachments_dir.is_dir():
            for att_file in sorted(attachments_dir.rglob("*")):
                if att_file.is_file():
                    rel_path = att_file.relative_to(attachments_dir)
                    arc_name = f"attachments/{rel_path.as_posix()}"
                    zip_file.write(att_file, arcname=arc_name)

    # Atomic replace
    tmp_zip_path.replace(output_package_path)
    LOGGER.info("Successfully generated bulk import package at %s", output_package_path)
    return output_package_path
