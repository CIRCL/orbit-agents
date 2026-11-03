#!/usr/bin/env python3
"""Render the download page and checksums from the three built installers."""

import argparse
from datetime import datetime, timezone
import hashlib
import html
from pathlib import Path
import shlex
from string import Template
from urllib.parse import quote


def build(directory):
    values = {"build_date": datetime.now(timezone.utc).strftime("%d %B %Y").lstrip("0")}
    checksums = []
    for platform, extension in (("macos", "pkg"), ("windows", "msi"), ("linux", "deb")):
        files = sorted(directory.glob("*." + extension))
        if len(files) != 1 or not files[0].is_file() or files[0].is_symlink():
            raise ValueError(f"Expected exactly one regular .{extension} installer in {directory}")
        package = files[0]
        if not package.stat().st_size or any(c in package.name for c in "\r\n\\"):
            raise ValueError(f"Empty installer or unsupported filename: {package.name!r}")
        with package.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        checksums.append(f"{digest}  {package.name}\n")
        values.update({
            platform + "_url": html.escape(quote(package.name, safe=""), quote=True),
            platform + "_filename": html.escape(package.name, quote=True),
            platform + "_size": f"{package.stat().st_size / 1000 / 1000:.1f} MB",
            platform + "_sha256": digest,
        })
        if platform == "linux":
            values["linux_command"] = html.escape("sudo apt install " + shlex.quote("./" + package.name))
    template = Path(__file__).resolve().parents[1] / "site/index.html"
    rendered = Template(template.read_text(encoding="utf-8")).substitute(values)
    (directory / "index.html").write_text(rendered, encoding="utf-8")
    (directory / "SHA256SUMS").write_text("".join(checksums), encoding="utf-8")
    print("Generated download page and SHA256SUMS for all three installers")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing one .pkg, .msi and .deb")
    args = parser.parse_args()
    try:
        build(args.directory)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Download-site build failed: {error}\n")


if __name__ == "__main__":
    main()
