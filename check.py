"""Run the checks of the three parts.

    python check.py

A part has passed if its script ends with status 0 and its last line says that all its checks passed,
and the number of checks is the number that the part is known to run (so that a part that runs fewer
checks than it should, or none, does not pass).  Exit status 0 only if all three parts pass.
Standard library only.
"""

import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTS = [
    ("document 449", ["doc449", "code", "decode.py"], 47),
    ("Bauman's key", ["bauman", "code", "check.py"], 141),
    ("document 15", ["doc15", "code", "decode.py"], 113),
]


def main():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    failed = []
    for name, path, expected in PARTS:
        print("== %s" % name, flush=True)
        script = os.path.join(ROOT, *path)
        run = subprocess.run(
            [sys.executable, script, "--check"],
            cwd=os.path.dirname(script),
            stdout=subprocess.PIPE,
            encoding="utf-8",
            check=False,
        )
        out = run.stdout.replace("\r\n", "\n")
        print(out, end="", flush=True)
        lines = out.strip().split("\n")
        if run.returncode != 0 or lines[-1] != "%d of %d checks passed" % (expected, expected):
            failed.append(name)
        print(flush=True)
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        readme = " ".join(f.read().split())
    if "such as `%d of %d checks passed`" % (PARTS[0][2], PARTS[0][2]) not in readme:
        print("README.md does not give the number of checks of the first part")
        failed.append("README.md")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("all three parts passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
