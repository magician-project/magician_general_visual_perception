#!/usr/bin/env python3
"""Install a private glibc loader for the local TensorFlow wheel.

This extracts an Ubuntu package into this project. It never runs dpkg -i or
changes system libraries or Python environments.
"""

import hashlib
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from urllib.request import urlopen


PACKAGE_DIR = Path(__file__).resolve().parent.parent
RUNTIME_DIR = PACKAGE_DIR / ".runtime" / "glibc-2.39"
URL = (
    "https://archive.ubuntu.com/ubuntu/pool/main/g/glibc/"
    "libc6_2.39-0ubuntu8.9_amd64.deb"
)
SHA256 = "ff5557d99b51f761c4b7c92368b9cc45565eda17df9bf9eb4b134d09825008be"


def main():
    if (RUNTIME_DIR / "usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2").is_file():
        print(f"Local glibc runtime already present: {RUNTIME_DIR}")
        return
    if RUNTIME_DIR.exists():
        raise RuntimeError(f"Incomplete local glibc runtime: {RUNTIME_DIR}")

    with TemporaryDirectory(prefix="magician-glibc-") as temporary:
        archive = Path(temporary) / "libc6.deb"
        digest = hashlib.sha256()
        with urlopen(URL, timeout=30) as response, archive.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)
                output.write(chunk)
        if digest.hexdigest() != SHA256:
            raise RuntimeError("Ubuntu libc6 package checksum mismatch")

        extracted = Path(temporary) / "glibc-2.39"
        subprocess.run(["dpkg-deb", "-x", str(archive), str(extracted)], check=True)
        libdir = extracted / "usr/lib/x86_64-linux-gnu"
        if not all((libdir / name).is_file() for name in
                   ("ld-linux-x86-64.so.2", "libc.so.6", "libm.so.6")):
            raise RuntimeError("Ubuntu libc6 package lacks the expected libraries")

        RUNTIME_DIR.parent.mkdir(exist_ok=True)
        shutil.move(str(extracted), str(RUNTIME_DIR))
    print(f"Installed local glibc runtime: {RUNTIME_DIR}")


if __name__ == "__main__":
    main()
