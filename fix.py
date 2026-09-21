#!/usr/bin/env python3
# =====================================================================
# fix.py: Sanitize HTML entity leaks with Unicode in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def sanitize_entities():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for raw HTML entity leaks in JS strings, SVG text nodes, and labels
    replacements = [
        ("&rarr;", "→"),
        ("&larr;", "←"),
        ("&#8594;", "→"),
        ("&#8592;", "←"),
        ("&#8634;", "↺"),
        ("&bull;", "•"),
        ("&amp;rarr;", "→"),
        ("&amp;larr;", "←"),
        ("&amp;bull;", "•"),
    ]

    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    # In HTML attributes and button text where &rarr; was used inside innerHTML,
    # converting to literal Unicode '→' and '←' prevents double-encoding leaks.
    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("--> Replaced entity codes with native Unicode glyphs.")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Sanitize raw HTML entity codes with native Unicode characters in Module 2\n\n"
                "Replace leaky entity encodings (&rarr;, &larr;, &bull;, &#8634;) across\n"
                "SVG diagrams and JavaScript telemetry state strings with Unicode glyphs."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 02-hardware-review.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No raw entity leaks found in 02-hardware-review.html.")

if __name__ == "__main__":
    sanitize_entities()
