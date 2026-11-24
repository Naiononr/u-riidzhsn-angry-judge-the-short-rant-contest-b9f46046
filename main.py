#!/usr/bin/env python3
"""Write the Angry Judge rant to /output/entry.txt.

Stdlib only. Deterministic: the same bytes on every run.
The text is a short, funny rant about a delivery photo showing the
wrong door -- a concrete everyday annoyance, told in short angry
sentences with no throat-clearing.
"""
import os
import tempfile

RANT = (
    "My parcel was delivered. The photo proves it. It shows a door. "
    "Not my door. A door I have never seen, on a street I do not live on, "
    "holding my parcel like a hostage. The app says 'delivered with a smile'. "
    "Whose smile? Not mine. I am now a detective in a case about a door."
)

# Gate: /output/entry.txt must be UTF-8 text of 1 to 400 characters,
# not only whitespace; one short text, no trailing newline.
assert 1 <= len(RANT) <= 400, "rant must fit the 1-400 character gate"
assert RANT.strip() == RANT, "rant must not start or end with whitespace"
assert "\n" not in RANT, "rant is a single short text, no line breaks"


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = RANT.encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, os.path.join(out_dir, "entry.txt"))
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


if __name__ == "__main__":
    main()
