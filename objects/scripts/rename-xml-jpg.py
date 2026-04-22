"""
rename_newspaper_files.py

Renames XML and image files under objects/newspapers/ to the convention:
  {newspaper_name}_{date}_P{NN}.xml
  {newspaper_name}_{date}_P{NN}.jpg

Structure expected:
  objects/newspapers/
  └── {newspaper_name}/
      └── {date}/          ← DD-MM-YYYY or YYYY
          ├── 001.xml
          ├── 002.xml
          └── images/
              ├── 001.jpg
              └── 002.jpg

Usage:
  python rename_newspaper_files.py                        # defaults to objects/newspapers
  python rename_newspaper_files.py --root path/to/newspapers
  python rename_newspaper_files.py --dry-run             # preview without renaming
"""

import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_number(filename: str) -> int:
    """
    Extract the page number from a filename, trying patterns in order:

      1. Separator + p/page + digits:  _p001, -p001, _page001, 0001_p001
         (handles filenames like "0001_p001.xml" where the scan number comes first)
      2. Standalone page marker:       P03, page-5, page_13
         (handles "P01.xml", "page-3.xml")
      3. Fallback: last run of digits in the stem
         (handles bare "005.xml")
    """
    stem = Path(filename).stem

    # 1. Separator before p-marker: covers 0001_p001, 0001-p001, etc.
    match = re.search(r"[-_][Pp](?:age)?[-_]?(\d+)", stem)
    if match:
        return int(match.group(1))

    # 2. p-marker at start or after non-separator: P03, page-5, page_13
    match = re.search(r"(?<![a-zA-Z])[Pp](?:age)?[-_]?(\d+)", stem)
    if match:
        return int(match.group(1))

    # 3. Fallback: last run of digits in the stem
    matches = re.findall(r"\d+", stem)
    return int(matches[-1]) if matches else 0


def is_valid_date_folder(name: str) -> bool:
    """Accept DD-MM-YYYY or YYYY folder names."""
    return bool(re.fullmatch(r"\d{4}", name) or re.fullmatch(r"\d{2}-\d{2}-\d{4}", name))


def collect_files(folder: Path, extension: str) -> list[Path]:
    """Return files with the given extension, sorted by embedded number."""
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == extension]
    return sorted(files, key=lambda f: extract_number(f.name))


# ---------------------------------------------------------------------------
# Core renaming logic
# ---------------------------------------------------------------------------

def rename_issue(newspaper_name: str, date: str, issue_dir: Path, dry_run: bool) -> dict:
    """
    Rename XMLs in issue_dir and JPGs in issue_dir/images/.
    Returns a summary dict with counts and warnings.
    """
    summary = {"xmls": 0, "imgs": 0, "warnings": [], "skipped": False}

    xml_files = collect_files(issue_dir, ".xml")
    images_dir = issue_dir / "images"
    img_files = collect_files(images_dir, ".jpg") if images_dir.is_dir() else []

    # Warn if counts differ but rename each set independently
    if xml_files and img_files and len(xml_files) != len(img_files):
        msg = (
            f"  ⚠  Count mismatch in {issue_dir.relative_to(issue_dir.parent.parent)}: "
            f"{len(xml_files)} XMLs vs {len(img_files)} images — renaming each set independently."
        )
        summary["warnings"].append(msg)
        print(msg)

    base = f"{newspaper_name}_{date}"

    # Rename XMLs
    for xml_path in xml_files:
        page_num = extract_number(xml_path.name)
        new_name = f"{base}_P{page_num:02d}.xml"
        new_path = xml_path.parent / new_name
        if xml_path.name == new_name:
            print(f"  [skip] {xml_path.name} already correctly named")
            continue
        print(f"  {'[dry-run] ' if dry_run else ''}XML  {xml_path.name}  →  {new_name}")
        if not dry_run:
            xml_path.rename(new_path)
        summary["xmls"] += 1

    # Rename images
    for img_path in img_files:
        page_num = extract_number(img_path.name)
        new_name = f"{base}_P{page_num:02d}.jpg"
        new_path = img_path.parent / new_name
        if img_path.name == new_name:
            print(f"  [skip] {img_path.name} already correctly named")
            continue
        print(f"  {'[dry-run] ' if dry_run else ''}IMG  {img_path.name}  →  {new_name}")
        if not dry_run:
            img_path.rename(new_path)
        summary["imgs"] += 1

    return summary


# ---------------------------------------------------------------------------
# Main walker
# ---------------------------------------------------------------------------

def process_newspapers(root: Path, dry_run: bool):
    if not root.is_dir():
        print(f"Error: '{root}' is not a valid directory.")
        return

    total_xmls = total_imgs = total_warnings = 0

    for newspaper_dir in sorted(root.iterdir()):
        if not newspaper_dir.is_dir():
            continue
        newspaper_name = newspaper_dir.name
        print(f"\n{newspaper_name}")

        for issue_dir in sorted(newspaper_dir.iterdir()):
            if not issue_dir.is_dir():
                continue
            date = issue_dir.name

            if not is_valid_date_folder(date):
                print(f"  [skip] '{date}' doesn't look like a date folder (expected YYYY or DD-MM-YYYY)")
                continue

            print(f"  {date}")
            summary = rename_issue(newspaper_name, date, issue_dir, dry_run)
            total_xmls += summary["xmls"]
            total_imgs += summary["imgs"]
            total_warnings += len(summary["warnings"])

    print("\n" + "─" * 50)
    label = "Would rename" if dry_run else "Renamed"
    print(f"Done. {label}: {total_xmls} XMLs, {total_imgs} images.  Warnings: {total_warnings}")
    if dry_run:
        print("   (dry-run mode — no files were changed. Remove --dry-run to apply.)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename newspaper XML and image files.")
    parser.add_argument(
        "--root",
        default="objects/newspapers",
        help="Path to the newspapers root folder (default: objects/newspapers)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview renames without making any changes",
    )
    args = parser.parse_args()

    process_newspapers(Path(args.root), dry_run=args.dry_run)