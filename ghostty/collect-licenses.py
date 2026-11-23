#!/usr/bin/env python3
"""Keep upstream license notices for source dependencies in the binary RPM."""
from pathlib import Path
import json
import shutil

manifest = json.loads(Path('build.zig.zon.json').read_text())
output = Path('bundled-licenses')
output.mkdir(exist_ok=True)
for key, dep in manifest.items():
    source = Path('zig-pkg')/key
    if not source.exists():
        continue
    notices = {p for glob in ('LICENSE*', 'COPYING*', 'COPYRIGHT*', 'OFL*', 'UNLICENSE*') for p in source.glob(glob)}
    if not notices:
        continue
    dest = output/(dep['name']+'-'+key)
    dest.mkdir(exist_ok=True)
    for notice in sorted(notices):
        if notice.is_dir():
            shutil.copytree(notice, dest/notice.name, symlinks=True)
        else:
            shutil.copy2(notice, dest/notice.name)
