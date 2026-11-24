"""Write linear-a-lexicon-chatgpt.zip, the plugin folder as ChatGPT takes it.

    python3 package/pack_chatgpt.py OUT_DIR

Reads `linear-a-lexicon/` and writes one file into OUT_DIR, which it creates and which must lie outside the plugin
folder. An existing zip there is replaced. Every file or folder whose name begins with a dot is left out: that is
Claude's manifest folder and its `.mcp.json`, and any editor or system file. The same files give the same bytes: each
entry carries one fixed date and mode.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

NAME = "linear-a-lexicon"
PLUGIN = Path(__file__).resolve().parents[1] / NAME
EPOCH = (1980, 1, 1, 0, 0, 0)  # the earliest date a zip entry can carry


def pack(out: Path) -> Path:
    """Write the zip into `out` and return its path. Every entry sits under `linear-a-lexicon/`."""
    out = out.resolve()
    if out == PLUGIN or PLUGIN in out.parents:
        raise ValueError(f"{out} is inside the plugin folder; the zip would pack itself")
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"{NAME}-chatgpt.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PLUGIN.rglob("*")):
            inside = path.relative_to(PLUGIN)
            if path.is_file() and not any(part.startswith(".") for part in inside.parts):
                entry = zipfile.ZipInfo(f"{NAME}/{inside.as_posix()}", date_time=EPOCH)
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o644 << 16
                archive.writestr(entry, path.read_bytes())
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out_dir", type=Path, help="the folder the zip is written into")
    print(f"Wrote {pack(parser.parse_args().out_dir)}")
