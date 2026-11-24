#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers — make.fun entry.

Writes one original fortune-cookie line for a software developer to
entry.txt in the output directory (MAKEFUN_OUTPUT_DIR, default /output).
"""

import os

TEXT = "A legacy system holds no grudges; it simply remembers every shortcut you took."

MAX_CHARS = 120  # the gate: entry.txt is UTF-8 text of 1..120 characters


def validated_text() -> str:
    """Return the full file content, checked against the gate before writing.

    The content is the fortune line plus one trailing newline. It must be
    UTF-8 encodable, 1..MAX_CHARS characters, exactly one line, and not
    only white space.
    """
    content = TEXT + "\n"
    content.encode("utf-8")  # raises if not encodable
    assert 1 <= len(content) <= MAX_CHARS, f"entry is {len(content)} chars"
    assert content.strip(), "entry is only white space"
    assert content.count("\n") == 1 and content.endswith("\n"), "must be one line"
    return content


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = validated_text().encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Read back what landed on disk and prove it is byte-for-byte the
    # validated content, so a partial write can never slip through.
    with open(path, "rb") as fh:
        assert fh.read() == data, "written bytes differ from validated text"


if __name__ == "__main__":
    main()
